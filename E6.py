from sqlalchemy.orm import Session
from functions import engine, FanClub, fanclub_to_dict


def get_fanclubs(artist_id=None, name=None):
    session = Session(engine)

    query = session.query(FanClub)

    if artist_id is not None:
        query = query.filter(FanClub.artist_id == artist_id)
    if name is not None:
        query = query.filter(FanClub.name.ilike(name))

    result = []
    for club in query.order_by(FanClub.id).all():
        result.append(fanclub_to_dict(club))

    session.close()
    return result
