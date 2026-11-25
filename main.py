from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import functions
from datetime import date
from typing import List
import E11

app = FastAPI(title="K-Pop Universe - Fan Community Platform")


# ---------- Request bodies (Pydantic) ----------
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


class PostCreate(BaseModel):
    text: str
    image_url: str = None


def check_token(token):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return payload["username"]


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





# ---------- Admin ----------


# ---------- Artists ----------


# ---------- Fan clubs ----------

@app.get("/fanclubs")
def get_fanclubs():
    return functions.get_fanclubs()


@app.post("/fanclubs/{club_id}/join")
def join_fanclub(club_id: int, token = Header(None)):
    username = check_token(token)
    if functions.join_fanclub(club_id=club_id, username=username) is None:
        raise HTTPException(status_code=404, detail="Fan club not found")
    return {"message": "Joined fan club"}


# ---------- Posts ----------

@app.post("/posts", status_code=201)
def create_post(data: PostCreate, token = Header(None)):
    username = check_token(token)
    return functions.create_post(text=data.text, image_url=data.image_url, username=username)


@app.get("/posts")
def get_posts():
    return functions.get_posts()


@app.post("/posts/{post_id}/like")
def like_or_unlike_post(post_id: int, token = Header(None)):
    username = check_token(token)
    result = functions.like_or_unlike_post(post_id=post_id, username=username)
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


# ---------- Events ----------
