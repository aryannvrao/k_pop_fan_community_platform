from sqlalchemy.orm import Session
from functions import engine, Post, post_to_dict


def get_posts(user_id=None):
    session = Session(engine)

    query = session.query(Post)

    if user_id is not None:
        query = query.filter(Post.user_id == user_id)

    result = []
    for post in query.order_by(Post.id).all():
        result.append(post_to_dict(post))

    session.close()
    return result
