from sqlalchemy.orm import Session
from functions import engine, Artist, User, FanClub, fanclub_to_dict


def create_fanclub(name, artist_id, username):
    session = Session(engine)

    artist = session.get(Artist, artist_id)
    if artist is None:
        session.close()
        return None

    user = session.query(User).filter_by(username=username).first()
    if user is None:
        session.close()
        return False

    club = FanClub(name=name, artist_id=artist_id, created_by=user.id)

    session.add(club)
    session.commit()
    session.refresh(club)

    result = fanclub_to_dict(club)

    session.close()
    return result