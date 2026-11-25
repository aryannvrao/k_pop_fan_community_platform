from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import functions

app = FastAPI(title="K-Pop Universe - Fan Community Platform")


# ---------- Request bodies (Pydantic) ----------
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class PostCreate(BaseModel):
    text: str
    image_url: str = None


def check_token(token):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return username


@app.get("/")
def hello():
    return {"message": "K-Pop Universe API. Docs at /docs"}


# ---------- Auth ----------
@app.post("/auth/register")
def register_user(data: RegisterRequest):
    if functions.register_user(username=data.username, email=data.email, password=data.password):
        return {"message": "user registered successfully"}
    raise HTTPException(status_code=400, detail="User already exists")





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


# ---------- Events ----------
