# kpop-universe

# Team - K-Pop Universe – Fan Community Platform

| Partner 1 | Partner 2 | Partner 3 | Project |
|---|---|---|---|
| Aryan | Harsita | Kaif | K-Pop Universe – Fan Community Platform |

## 1. Who is doing what

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Aryan | Repo setup, DB schema (`functions.py`), auth (`A1`–`A3`), Dockerfile & CI/CD base | ✅ | `E6`–`E10` (fan clubs & posts) | None |
| Day 1 | Harsita | `E1`–`E3` (create organizer, add/get artists) | ✅ | `E4`–`E5` (artist details, create fan club) | None |
| Day 1 | Kaif | JWT payload updates (`functions.py`), `E11`–`E12` (create poll, vote in poll) | ✅ | `E13`–`E15` (poll results & events) | None |
| Day 2 | Aryan | `E6`–`E10` (fan clubs & posts) and EC2 deployment setup | ✅ | Persistent DB mount & presentation prep | None |
| Day 2 | Harsita | `E4`–`E5` (artist details, create fan club) and endpoint wiring in `main.py` | ✅ | `/docs` verification & presentation prep | None |
| Day 2 | Kaif | `E13`–`E15` (poll results, create event, register for event) | ✅ | Automated testing & CI/CD test gate | None |
| Day 3 | Aryan | Deployment verification & presentation prep | ✅ | Final demo & submission | None |
| Day 3 | Harsita | API verification in `/docs`, README & presentation prep | ✅ | Final demo & submission | None |
| Day 3 | Kaif | Automated test suite (`test_api.py`), CI test gate & SQLite mount in `deploy.yml` | ✅ | Final demo & submission | None |

## 2. User roles 

| Role | Responsibilities |
|---|---|
| Admin | Manage organizers, users and platform moderation |
| Organizer | Manage artists, fan events and community activities |
| Fan | Create fan clubs, publish posts, vote and participate in events |

New registrations receive the **fan** role by default. Only admins can create organizer accounts.

## 3. API contract 

Backend runs on **port 8001**. Methods, paths and bodies below are our team's decisions.

### Authentication APIs (3)

| # | What it does | Method | Path | Request body | Success code |
|---|---|---|---|---|---|
| A1 | Register a new account (role = fan) | POST | `/auth/register` | `{ username, email, password }` | 200 |
| A2 | Login and generate access and refresh tokens | POST | `/auth/login` | `{ email, password }` | 200 |
| A3 | Generate a new access token | POST | `/auth/refresh` | `{ refresh_token }` | 200 |

### Project-specific APIs (15)

| # | What it does | Method | Path | Request body | Access | Success code |
|---|---|---|---|---|---|---|
| E1 | Create an organizer account | POST | `/admin/organizers` | `{ username, email, password }` | Admin | 200 |
| E2 | Add an artist or group | POST | `/artists` | `{ name, description, category }` | Organizer | 200 |
| E3 | Get all artists and groups | GET | `/artists` | — | All | 200 |
| E4 | Get details of one artist or group | GET | `/artists/{artist_id}` | — | All | 200 |
| E5 | Create a fan club | POST | `/fanclubs` | `{ name, artist_id }` | Fan | 200 |
| E6 | Get all available fan clubs | GET | `/fanclubs` | — | All | 200 |
| E7 | Join a fan club | POST | `/fanclubs/{club_id}/join` | — | Fan | 200 |
| E8 | Create a community post | POST | `/posts` | `{ text, image_url (optional) }` | Fan | 201 |
| E9 | Get posts from the community feed | GET | `/posts` | — | All | 200 |
| E10 | Like or unlike a post | POST | `/posts/{post_id}/like` | — | Fan | 200 |
| E11 | Create a poll for an artist or group | POST | `/polls` | `{ artist_id, question, options[], opens_at, closes_at }` | Organizer | 200 |
| E12 | Vote in a poll | POST | `/polls/{poll_id}/vote` | `{ option_id }` | Fan | 200 |
| E13 | Get poll results | GET | `/polls/{poll_id}/results` | — | All | 200 |
| E14 | Create a fan event | POST | `/events` | `{ name, date, venue, participant_limit }` | Organizer | 200 |
| E15 | Register for a fan event | POST | `/events/{event_id}/register` | — | Fan | 200 |

All protected endpoints take the JWT access token in the `token` request header.

## 4. Business rules the API must check 

| Rule | Proposed status |
|---|---|
| Non-admin trying to create an organizer | 403 |
| Wrong role for a protected endpoint | 403 |
| Invalid or expired access / refresh token | 401 |
| A fan joining the same fan club twice | 409 |
| A fan liking the same post twice | 409 |
| A fan voting more than once in a poll | 409 |
| Voting outside the poll's opening/closing dates | 400 |
| The same fan registering for the same event twice | 409 |
| Registering for an event that is full | 400 |
| Missing or empty required fields | 422 |

Every error returns a meaningful message. Admins must be able to manage inappropriate users and community content.

## 5. Endpoint tracker

Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Who |
|---|---|---|---|---|
| A1 | POST /auth/register | ✅ | ✅ | Aryan / Kaif |
| A2 | POST /auth/login | ✅ | ✅ | Aryan / Kaif |
| A3 | POST /auth/refresh | ✅ | ✅ | Aryan / Kaif |
| E1 | POST /admin/organizers | ✅ | ✅ | Harsita |
| E2 | POST /artists | ✅ | ✅ | Harsita |
| E3 | GET /artists | ✅ | ✅ | Harsita |
| E4 | GET /artists/{artist_id} | ✅ | ✅ | Harsita |
| E5 | POST /fanclubs | ✅ | ✅ | Harsita |
| E6 | GET /fanclubs | ✅ | ✅ | Aryan |
| E7 | POST /fanclubs/{club_id}/join | ✅ | ✅ | Aryan |
| E8 | POST /posts | ✅ | ✅ | Aryan |
| E9 | GET /posts | ✅ | ✅ | Aryan |
| E10 | POST /posts/{post_id}/like | ✅ | ✅ | Aryan |
| E11 | POST /polls | ✅ | ✅ | Kaif |
| E12 | POST /polls/{poll_id}/vote | ✅ | ✅ | Kaif |
| E13 | GET /polls/{poll_id}/results | ✅ | ✅ | Kaif |
| E14 | POST /events | ✅ | ✅ | Kaif |
| E15 | POST /events/{event_id}/register | ✅ | ✅ | Kaif |

## 6. Setup & deployment tracker

| Item | Status | Who |
|---|---|---|
| GitHub repo + collaborators + README | ✅ | Team |
| Database schema design (tables, fields, relationships) | ✅ | Aryan |
| Dockerfile | ✅ | Aryan |
| Automated API testing (`test_api.py` + CI test gate) | ✅ | Kaif |
| Docker image built & verified locally | ✅ | Team |
| Image pushed to Docker Hub | ✅ | Aryan / Kaif |
| GitHub Actions workflow (test → build → Docker Hub → EC2) | ✅ | Aryan / Kaif |
| EC2 instance + Docker installed + security group | ✅ | Aryan |
| Persistent SQLite directory mounted on EC2 | ✅ | Kaif |
| Public API URL working after auto-deploy | ✅ | Team |

Credentials (Docker Hub, EC2 SSH) live in **GitHub Actions Secrets** — never in the repo.

## 7. Tech Stack & Deployment

- **Backend:** Python, FastAPI, Pydantic, SQLite, SQLAlchemy, PyJWT, argon2-cffi
- **Auth:** JWT access + refresh tokens, role-based access control (Admin / Organizer / Fan)
- **Deployment:** Docker (no Compose), GitHub Actions CI/CD, AWS EC2
- **Database:** SQLite file, persisted outside the container via a mounted directory on EC2

## 8. How to Run Locally

### Backend (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Swagger UI: http://127.0.0.1:8001/docs

### Automated Tests

```powershell
pip install pytest httpx
pytest -v
```

### Docker

```powershell
docker build -f dockerfile -t kpop-universe .
docker run -p 8001:8001 kpop-universe
```

Verify the API works through the container at http://127.0.0.1:8001/docs
