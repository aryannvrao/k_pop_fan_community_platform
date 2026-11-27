from sqlalchemy.orm import Session
from functions import engine, Artist, artist_to_dict

def get_artist(artist_id):
    session = Session(engine)

    artist = session.get(Artist, artist_id)

    if artist is None:
        session.close()
        return None

    result = artist_to_dict(artist)

    session.close()
    return result



