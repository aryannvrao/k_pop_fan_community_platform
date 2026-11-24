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





# ---------- Admin ----------


# ---------- Artists ----------


# ---------- Fan clubs ----------


# ---------- Posts ----------


# ---------- Polls ----------


# ---------- Events ----------
