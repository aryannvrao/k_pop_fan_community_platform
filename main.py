from email.quoprimime import body_check

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


@app.post("/auth/login")
def login(data: LoginRequest):
    token = functions.verify_login(email=data.email, password=data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return token


@app.post("/auth/refresh")
def refresh(data: RefreshRequest):
    username = functions.verify_token(token=data.refresh_token, token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")

    access_token = functions.create_token(username=username, token_type="access")
    return {"access_token": access_token}


# ---------- Admin ----------


# ---------- Artists ----------


# ---------- Fan clubs ----------


# ---------- Posts ----------


# ---------- Polls ----------

@app.post("/create-poll")
def create_new_poll(artist_id : str, question : str, closes_at : str, options=body):


# ---------- Events ----------
