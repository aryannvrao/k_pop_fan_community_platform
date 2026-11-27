from sqlalchemy.orm import Session
from functions import engine, Post, PostLike, User, post_to_dict


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
        result = post_to_dict(post)
        result["message"] = "Post liked"
    else:
        session.delete(existing)
        session.commit()
        result = post_to_dict(post)
        result["message"] = "Post unliked"

    session.close()
    return result
