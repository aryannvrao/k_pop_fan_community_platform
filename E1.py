from sqlalchemy.orm import Session
from functions import engine, User, ph



def create_organizer(username, email, password):
    session = Session(engine)
    user_exists = session.query(User).filter_by(username=username).first()

    if user_exists is not None:
        session.close()
        return False

    session.add(User(username=username, email=email,
                     password=ph.hash(password), role="organizer"))
    session.commit()
    session.close()
    return True