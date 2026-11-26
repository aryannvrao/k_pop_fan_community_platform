import os
import uuid
from datetime import date, timedelta
from fastapi.testclient import TestClient

# Start with a fresh SQLite DB in CI; skip if locked by a local server on Windows
if os.path.exists("kpop.db"):
    try:
        os.remove("kpop.db")
    except PermissionError:
        pass

from main import app  # noqa: E402

client = TestClient(app)


def test_full_prd_api_flow():
    uid = uuid.uuid4().hex[:6]
    fan1_user, fan1_email = f"fan1_{uid}", f"fan1_{uid}@kpop.com"
    fan2_user, fan2_email = f"fan2_{uid}", f"fan2_{uid}@kpop.com"
    org_user, org_email = f"org1_{uid}", f"org1_{uid}@kpop.com"

    # ---------- Root ----------
    res = client.get("/")
    assert res.status_code == 200

    # ---------- A1: Register fans ----------
    res = client.post("/auth/register", json={
        "username": fan1_user,
        "email": fan1_email,
        "password": "password123"
    })
    assert res.status_code == 200

    res = client.post("/auth/register", json={
        "username": fan2_user,
        "email": fan2_email,
        "password": "password123"
    })
    assert res.status_code == 200

    # Duplicate registration -> 400
    res = client.post("/auth/register", json={
        "username": fan1_user,
        "email": fan1_email,
        "password": "password123"
    })
    assert res.status_code == 400

    # ---------- A2: Login (Admin & Fan) ----------
    # Seeded admin from functions.py
    res = client.post("/auth/login", json={
        "email": "admin@kpop.com",
        "password": "123456"
    })
    assert res.status_code == 200
    admin_tokens = res.json()
    admin_headers = {"token": admin_tokens["access_token"]}

    res = client.post("/auth/login", json={
        "email": fan1_email,
        "password": "password123"
    })
    assert res.status_code == 200
    fan1_tokens = res.json()
    fan1_headers = {"token": fan1_tokens["access_token"]}

    res = client.post("/auth/login", json={
        "email": fan2_email,
        "password": "password123"
    })
    assert res.status_code == 200
    fan2_headers = {"token": res.json()["access_token"]}

    # Invalid login -> 401
    res = client.post("/auth/login", json={
        "email": fan1_email,
        "password": "wrongpassword"
    })
    assert res.status_code == 401

    # ---------- A3: Refresh Token ----------
    res = client.post("/auth/refresh", json={
        "refresh_token": fan1_tokens["refresh_token"]
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

    res = client.post("/auth/refresh", json={"refresh_token": "invalid-token"})
    assert res.status_code == 401

    # ---------- E1: Create Organizer (Admin only) ----------
    # Fan cannot create organizer -> 403
    res = client.post("/admin/organizers", headers=fan1_headers, json={
        "username": org_user,
        "email": org_email,
        "password": "password123"
    })
    assert res.status_code == 403

    # Missing token -> 401
    res = client.post("/admin/organizers", json={
        "username": org_user,
        "email": org_email,
        "password": "password123"
    })
    assert res.status_code == 401

    # Admin creates organizer -> 200
    res = client.post("/admin/organizers", headers=admin_headers, json={
        "username": org_user,
        "email": org_email,
        "password": "password123"
    })
    assert res.status_code == 200

    # Login as organizer
    res = client.post("/auth/login", json={
        "email": org_email,
        "password": "password123"
    })
    assert res.status_code == 200
    org_headers = {"token": res.json()["access_token"]}

    # ---------- E2: Add Artist (Organizer only) ----------
    res = client.post("/artists", headers=fan1_headers, json={
        "name": "BTS",
        "description": "Global K-Pop group",
        "category": "Boy Group"
    })
    assert res.status_code == 403

    res = client.post("/artists", headers=org_headers, json={
        "name": "BTS",
        "description": "Global K-Pop group",
        "category": "Boy Group"
    })
    assert res.status_code == 200
    artist_id = res.json()["id"]

    # ---------- E3 & E4: Get Artists & Artist Details ----------
    res = client.get("/artists")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    res = client.get(f"/artists/{artist_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "BTS"

    res = client.get("/artists/99999")
    assert res.status_code == 404

    # ---------- E5: Create Fan Club (Fan only) ----------
    res = client.post("/fanclubs", headers=org_headers, json={
        "name": "ARMY",
        "artist_id": artist_id
    })
    assert res.status_code == 403

    res = client.post("/fanclubs", headers=fan1_headers, json={
        "name": "ARMY",
        "artist_id": artist_id
    })
    assert res.status_code == 200
    club_id = res.json()["id"]

    # ---------- E6: Get Fan Clubs ----------
    res = client.get("/fanclubs")
    assert res.status_code == 200
    assert any(c["id"] == club_id for c in res.json())

    # ---------- E7: Join Fan Club (Fan only) ----------
    res = client.post(f"/fanclubs/{club_id}/join", headers=fan1_headers)
    assert res.status_code == 200

    # Joining twice -> 409
    res = client.post(f"/fanclubs/{club_id}/join", headers=fan1_headers)
    assert res.status_code == 409

    # Non-existent club -> 404
    res = client.post("/fanclubs/99999/join", headers=fan1_headers)
    assert res.status_code == 404

    # ---------- E8: Create Post (Fan only) ----------
    res = client.post("/posts", headers=fan1_headers, json={
        "text": "Excited for the comeback!",
        "image_url": "https://example.com/comeback.jpg"
    })
    assert res.status_code == 201
    post_id = res.json()["id"]

    # ---------- E9: Get Posts ----------
    res = client.get("/posts")
    assert res.status_code == 200
    assert any(p["id"] == post_id for p in res.json())

    # ---------- E10: Like / Unlike Post ----------
    res = client.post(f"/posts/{post_id}/like", headers=fan1_headers)
    assert res.status_code == 200
    assert res.json()["message"] == "Post liked"

    res = client.post(f"/posts/{post_id}/like", headers=fan1_headers)
    assert res.status_code == 200
    assert res.json()["message"] == "Post unliked"

    # ---------- E11: Create Poll (Organizer only) ----------
    today = date.today()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)

    res = client.post("/polls", headers=fan1_headers, json={
        "artist_id": artist_id,
        "question": "Favorite album?",
        "options": ["Wings", "Map of the Soul"],
        "opens_at": str(today),
        "closes_at": str(tomorrow)
    })
    assert res.status_code == 403

    # Invalid options (< 2) -> 400
    res = client.post("/polls", headers=org_headers, json={
        "artist_id": artist_id,
        "question": "Only one?",
        "options": ["Only One"],
        "opens_at": str(today),
        "closes_at": str(tomorrow)
    })
    assert res.status_code == 400

    # Valid poll -> 200
    res = client.post("/polls", headers=org_headers, json={
        "artist_id": artist_id,
        "question": "Favorite album?",
        "options": ["Wings", "Map of the Soul"],
        "opens_at": str(today),
        "closes_at": str(tomorrow)
    })
    assert res.status_code == 200
    poll_id = res.json()["poll_id"]

    # Closed poll for date-check test
    res = client.post("/polls", headers=org_headers, json={
        "artist_id": artist_id,
        "question": "Old poll?",
        "options": ["A", "B"],
        "opens_at": str(yesterday - timedelta(days=2)),
        "closes_at": str(yesterday)
    })
    assert res.status_code == 200
    closed_poll_id = res.json()["poll_id"]

    # ---------- E13 (pre-vote) & E12: Get Poll Results & Vote ----------
    res = client.get(f"/polls/{poll_id}/results")
    assert res.status_code == 200
    option_id = res.json()["results"][0]["option_id"]

    # Organizer cannot vote -> 403
    res = client.post(f"/polls/{poll_id}/vote", headers=org_headers, json={
        "option_id": option_id
    })
    assert res.status_code == 403

    # Fan votes -> 200
    res = client.post(f"/polls/{poll_id}/vote", headers=fan1_headers, json={
        "option_id": option_id
    })
    assert res.status_code == 200

    # Duplicate vote -> 409
    res = client.post(f"/polls/{poll_id}/vote", headers=fan1_headers, json={
        "option_id": option_id
    })
    assert res.status_code == 409

    # Voting on closed poll -> 400
    closed_opt_id = client.get(f"/polls/{closed_poll_id}/results").json()["results"][0]["option_id"]
    res = client.post(f"/polls/{closed_poll_id}/vote", headers=fan1_headers, json={
        "option_id": closed_opt_id
    })
    assert res.status_code == 400

    # E13: Verify vote count updated
    res = client.get(f"/polls/{poll_id}/results")
    assert res.status_code == 200
    assert res.json()["total_votes"] == 1
    assert res.json()["results"][0]["votes"] == 1

    # ---------- E14: Create Fan Event (Organizer only) ----------
    res = client.post("/events", headers=fan1_headers, json={
        "name": "Fan Meet 2026",
        "date": str(tomorrow),
        "venue": "Seoul Arena",
        "participant_limit": 1
    })
    assert res.status_code == 403

    res = client.post("/events", headers=org_headers, json={
        "name": "Fan Meet 2026",
        "date": str(tomorrow),
        "venue": "Seoul Arena",
        "participant_limit": 0
    })
    assert res.status_code == 400

    res = client.post("/events", headers=org_headers, json={
        "name": "Fan Meet 2026",
        "date": str(tomorrow),
        "venue": "Seoul Arena",
        "participant_limit": 1
    })
    assert res.status_code == 200
    event_id = res.json()["event_id"]

    # ---------- E15: Register for Event (Fan only) ----------
    res = client.post(f"/events/{event_id}/register", headers=org_headers)
    assert res.status_code == 403

    res = client.post(f"/events/{event_id}/register", headers=fan1_headers)
    assert res.status_code == 200

    # Duplicate registration -> 409
    res = client.post(f"/events/{event_id}/register", headers=fan1_headers)
    assert res.status_code == 409

    # Event full (limit=1) -> 400
    res = client.post(f"/events/{event_id}/register", headers=fan2_headers)
    assert res.status_code == 400
