from sqlalchemy import func
from sqlalchemy.orm import Session
from functions import engine, Post, PostLike
from E8 import post_to_dict


def get_posts(user_id=None):
    session = Session(engine)

    query = session.query(Post, func.count(PostLike.id)) \
        .outerjoin(PostLike, PostLike.post_id == Post.id) \
        .group_by(Post.id)

    if user_id is not None:
        query = query.filter(Post.user_id == user_id)

    result = []
    for post, like_count in query.order_by(Post.id).all():
        result.append(post_to_dict(post, like_count))

    session.close()
    return result
