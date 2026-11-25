from sqlalchemy.orm import Session
from functions import engine, Artist



def artist_to_dict(a):
    return {
        "id": a.id,
        "name": a.name,
        "description": a.description,
        "category": a.category,
    }



def create_artist(name, description, category):
    session = Session(engine)

    artist = Artist(
        name=name,
        description=description,
        category=category
    )

    session.add(artist)
    session.commit()
    session.refresh(artist)

    result = artist_to_dict(artist)

    session.close()
    return result
