from sqlalchemy import create_engine, String, Column, Integer, Date, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone
import os
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# ---------- Database connection ----------
ph = PasswordHasher()

DB_URL = "sqlite:///kpop.db"
engine = create_engine(DB_URL)

ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@kpop.com"
ADMIN_PASSWORD = "123456"

ACCESS_TOKEN_EXPIRY = 15 #mins
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "SECRET123")
ALGORITHM = "HS256"

# ---------- Tables / Models ----------

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)            # admin / organizer / fan


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)


class FanClub(Base):
    __tablename__ = "fan_clubs"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    created_by = Column(Integer, ForeignKey("users.id"))


class FanClubMember(Base):
    __tablename__ = "fan_club_members"

    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey("fan_clubs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    image_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    question = Column(String)
    opens_at = Column(Date)
    closes_at = Column(Date)


class PollOption(Base):
    __tablename__ = "poll_options"

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey("polls.id"))
    text = Column(String)


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey("polls.id"))
    option_id = Column(Integer, ForeignKey("poll_options.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(Date)
    venue = Column(String)
    participant_limit = Column(Integer)


class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


# Create the tables if they don't exist.
Base.metadata.create_all(engine)


# ---------- AUTH ----------


def create_token(username, token_type):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "username": username,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_login(username, password):
    session = Session(engine)
    user = session.query(User).filter_by(username=username).first()

    if user is None:
        session.close()
        return False

    try:
        ph.verify(user.hashed_password, password)
    except VerifyMismatchError:
        session.close()
        return False

    session.close()

    access_token = create_token(username=username, token_type="access")
    refresh_token = create_token(username=username, token_type="refresh")

    return {"access_token": access_token, "refresh_token": refresh_token}

# ------ Users ------



# ---------- FAN CLUBS ----------


def fanclub_to_dict(f):
    return {
        "id": f.id,
        "name": f.name,
        "artist_id": f.artist_id,
        "created_by": f.created_by,
    }


def get_fanclubs():
    session = Session(engine)
    clubs = session.query(FanClub).order_by(FanClub.id).all()
    result = [fanclub_to_dict(c) for c in clubs]
    session.close()
    return result


def join_fanclub(club_id, username):
    session = Session(engine)

    club = session.get(FanClub, club_id)
    if club is None:
        session.close()
        return None

    user = session.query(User).filter_by(username=username).first()
    if user is None:
        session.close()
        return False

    existing = session.query(FanClubMember).filter_by(club_id=club_id, user_id=user.id).first()
    if existing is None:
        session.add(FanClubMember(club_id=club_id, user_id=user.id))
        session.commit()

    session.close()
    return True


# ---------- POSTS ----------


def post_to_dict(p):
    return {
        "id": p.id,
        "text": p.text,
        "image_url": p.image_url,
        "user_id": p.user_id,
    }


def create_post(text, image_url=None, username=None):
    session = Session(engine)

    user = session.query(User).filter_by(username=username).first()

    post = Post(text=text, image_url=image_url, user_id=user.id if user is not None else None)
    session.add(post)
    session.commit()
    session.refresh(post)

    result = post_to_dict(post)

    session.close()
    return result


def get_posts():
    session = Session(engine)
    posts = session.query(Post).order_by(Post.id).all()
    result = [post_to_dict(p) for p in posts]
    session.close()
    return result


def like_or_unlike_post(post_id, username):
    session = Session(engine)

    user = session.query(User).filter_by(username=username).first()
    if user is None:
        session.close()
        return None

    post = session.get(Post, post_id)
    if post is None:
        session.close()
        return None

    existing = session.query(PostLike).filter_by(post_id=post_id, user_id=user.id).first()
    if existing is None:
        session.add(PostLike(post_id=post_id, user_id=user.id))
        session.commit()
    else:
        session.delete(existing)
        session.commit()

    session.close()
    return post_to_dict(post)


# ---------- SEED (only admins can create organizers, so add the first admin) ----------

def seed_admin():
    session = Session(engine)

    if session.query(User).filter_by(role="admin").count() == 0:
        session.add(User(username=ADMIN_USERNAME, email=ADMIN_EMAIL,
                         password=ph.hash(ADMIN_PASSWORD), role="admin"))
        session.commit()

    session.close()


seed_admin()
