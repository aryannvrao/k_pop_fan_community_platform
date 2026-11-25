from sqlalchemy.orm import Session
from functions import engine, Artist, artist_to_dict

def get_artists():
    session = Session(engine)
    artists = session.query(Artist).order_by(Artist.id).all()
    result = [artist_to_dict(a) for a in artists]
    session.close()
    return result
