from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import functions
from datetime import date
from typing import List
import E1,E2,E3,E4,E5
import E6
import E7
import E8
import E9
import E10
import E11
import E12
import E13
import E14
import E15

app = FastAPI(title="K-Pop Universe - Fan Community Platform")


# ---------- Request bodies (Pydantic) ----------

class OrganizerCreate(BaseModel):
    username: str
    email: str
    password: str


class ArtistCreate(BaseModel):
    name: str
    description: str
    category: str


class FanClubCreate(BaseModel):
    name: str
    artist_id: int


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role :str = "fan"


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str

class CreatePollRequest(BaseModel):
    artist_id: int
    question: str
    options: List[str]
    opens_at: date
    closes_at: date


class VoteRequest(BaseModel):
    option_id: int


class CreateEventRequest(BaseModel):
    name: str
    date: date
    venue: str
    participant_limit: int


class PostCreate(BaseModel):
    text: str
    image_url: str = None


def check_token(token):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return payload

def validate_organizer(username=None, email=None, password=None):
    if username is not None and username.strip() == "":
        raise HTTPException(status_code=422, detail="Username cannot be empty")
    if email is not None and email.strip() == "":
        raise HTTPException(status_code=422, detail="Email cannot be empty")
    if password is not None and password.strip() == "":
        raise HTTPException(status_code=422, detail="Password cannot be empty")


def validate_artist(name=None, description=None, category=None):
    if name is not None and name.strip() == "":
        raise HTTPException(status_code=422, detail="Name cannot be empty")
    if description is not None and description.strip() == "":
        raise HTTPException(status_code=422, detail="Description cannot be empty")
    if category is not None and category.strip() == "":
        raise HTTPException(status_code=422, detail="Category cannot be empty")


def validate_fanclub(name=None):
    if name is not None and name.strip() == "":
        raise HTTPException(status_code=422, detail="Fan club name cannot be empty")


@app.get("/")
def hello():
    return {"message": "K-Pop Universe API. Docs at /docs"}


# ---------- Auth ----------
@app.post("/auth/register")
def register_user(data: RegisterRequest):
    if functions.register_user(username=data.username, email=data.email, password=data.password, role=data.role):
        return {"message": "user registered successfully"}
    raise HTTPException(status_code=400, detail="User already exists")


@app.post("/auth/login")
def login(data: LoginRequest):
    token = functions.verify_login(email=data.email, password=data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return token


@app.post("/auth/refresh")
def refresh(data: RefreshRequest):
    payload = functions.verify_token(token=data.refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")

    access_token = functions.create_token(
        username=payload["username"],
        role=payload["role"],
        user_id=payload["user_id"],
        token_type="access"
    )
    return {"access_token": access_token}


# ---------- End Points ----------

@app.post("/admin/organizers")
def create_organizer(data: OrganizerCreate, token = Header(None)):
    payload = check_token(token)
    if payload["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create organizers")
    validate_organizer(username=data.username, email=data.email, password=data.password)

    if not E1.create_organizer(username=data.username, email=data.email, password=data.password):
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "Organizer created successfully"}

# ---------- Artists ----------
@app.post("/artists")
def create_artist(data: ArtistCreate, token = Header(None)):
    payload = check_token(token)
    if payload["role"] != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers can add artists")
    validate_artist(name=data.name, description=data.description, category=data.category)

    return E2.create_artist(name=data.name, description=data.description, category=data.category)

@app.get("/artists")
def get_artists():
    return E3.get_artists()

@app.get("/artists/{artist_id}")
def get_artist(artist_id: int):
    artist = E4.get_artist(artist_id=artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@app.post("/fanclubs")
def create_fanclub(data: FanClubCreate, token = Header(None)):
    payload = check_token(token)
    if payload["role"] != "fan":
        raise HTTPException(status_code=403, detail="Only fans can create fan clubs")
    validate_fanclub(name=data.name)

    result = E5.create_fanclub(name=data.name, artist_id=data.artist_id, username=payload["username"])
    if result is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    if result is False:
        raise HTTPException(status_code=404, detail="User not found")
    return result

# ---------- Fan clubs ----------

@app.get("/fanclubs")
def get_fanclubs(artist_id: int = None, name: str = None):
    return E6.get_fanclubs(artist_id=artist_id, name=name)


@app.post("/fanclubs/{club_id}/join")
def join_fanclub(club_id: int, token = Header(None)):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    if payload["role"] != "fan":
        raise HTTPException(status_code=403, detail="Only fans can join fan clubs")

    result = E7.join_fanclub(club_id=club_id, username=payload["username"])
    if result == "club_not_found":
        raise HTTPException(status_code=404, detail="Fan club not found")
    if result == "user_not_found":
        raise HTTPException(status_code=404, detail="User not found")
    if result == "already_joined":
        raise HTTPException(status_code=409, detail="Already a member of this fan club")
    return {"message": "Joined fan club"}


# ---------- Posts ----------

@app.post("/posts", status_code=201)
def create_post(data: PostCreate, token = Header(None)):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    if payload["role"] != "fan":
        raise HTTPException(status_code=403, detail="Only fans can create posts")
    if data.text.strip() == "":
        raise HTTPException(status_code=422, detail="Post text cannot be empty")

    post = E8.create_post(text=data.text, image_url=data.image_url, username=payload["username"])
    if post is None:
        raise HTTPException(status_code=404, detail="User not found")
    return post


@app.get("/posts")
def get_posts(user_id: int = None):
    return E9.get_posts(user_id=user_id)


@app.post("/posts/{post_id}/like")
def like_or_unlike_post(post_id: int, token = Header(None)):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    if payload["role"] != "fan":
        raise HTTPException(status_code=403, detail="Only fans can like or unlike posts")

    result = E10.like_or_unlike_post(post_id=post_id, username=payload["username"])
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return result


# ---------- Polls ----------

@app.post("/polls")
def create_new_poll(data: CreatePollRequest, token = Header(None)):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    if payload["role"] != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers can create polls")

    result = E11.create_poll(
        artist_id=data.artist_id,
        question=data.question,
        opens_at=data.opens_at,
        closes_at=data.closes_at,
        options=data.options
    )

    if result == "artist_not_found":
        raise HTTPException(status_code=404, detail="Artist not found")
    if result == "invalid_options":
        raise HTTPException(status_code=400, detail="Poll must have at least 2 options")
    if result == "invalid_dates":
        raise HTTPException(status_code=400, detail="closes_at must be after opens_at")

    return {"message": "Poll created successfully", "poll_id": result}


@app.post("/polls/{poll_id}/vote")
def vote_in_poll(poll_id: int, data: VoteRequest, token = Header(None)):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    if payload["role"] != "fan":
        raise HTTPException(status_code=403, detail="Only fans can vote in polls")

    result = E12.vote_in_poll(
        poll_id=poll_id,
        option_id=data.option_id,
        user_id=payload["user_id"]
    )

    if result == "poll_not_found":
        raise HTTPException(status_code=404, detail="Poll not found")
    if result == "poll_closed":
        raise HTTPException(status_code=400, detail="Poll is not open for voting")
    if result == "option_not_found":
        raise HTTPException(status_code=404, detail="Poll option not found")
    if result == "already_voted":
        raise HTTPException(status_code=409, detail="You have already voted in this poll")

    return {"message": "Vote recorded successfully"}


@app.get("/polls/{poll_id}/results")
def get_poll_results(poll_id: int):
    result = E13.get_poll_results(poll_id=poll_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return result


# ---------- Events ----------

@app.post("/events")
def create_new_event(data: CreateEventRequest, token = Header(None)):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    if payload["role"] != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers can create events")

    result = E14.create_event(
        name=data.name,
        date=data.date,
        venue=data.venue,
        participant_limit=data.participant_limit
    )

    if result == "invalid_limit":
        raise HTTPException(status_code=400, detail="Participant limit must be greater than 0")

    return {"message": "Event created successfully", "event_id": result}


@app.post("/events/{event_id}/register")
def register_for_event(event_id: int, token = Header(None)):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    if payload["role"] != "fan":
        raise HTTPException(status_code=403, detail="Only fans can register for events")

    result = E15.register_for_event(
        event_id=event_id,
        user_id=payload["user_id"]
    )

    if result == "event_not_found":
        raise HTTPException(status_code=404, detail="Event not found")
    if result == "already_registered":
        raise HTTPException(status_code=409, detail="You are already registered for this event")
    if result == "event_full":
        raise HTTPException(status_code=400, detail="Event is full")

    return {"message": "Registered for event successfully"}
