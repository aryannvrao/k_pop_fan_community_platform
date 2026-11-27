from sqlalchemy.orm import Session
from functions import engine, Post, User, post_to_dict


def create_post(text, image_url=None, username=None):
    session = Session(engine)

    user = session.query(User).filter_by(username=username).first()
    if user is None:
        session.close()
        return None

    post = Post(text=text, image_url=image_url, user_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    result = post_to_dict(post)

    session.close()
    return result
