from sqlalchemy.orm import Session
from functions import engine, FanClub, FanClubMember, User


def join_fanclub(club_id, username):
    session = Session(engine)

    club = session.get(FanClub, club_id)
    if club is None:
        session.close()
        return "club_not_found"

    user = session.query(User).filter_by(username=username).first()
    if user is None:
        session.close()
        return "user_not_found"

    existing = session.query(FanClubMember).filter_by(club_id=club_id, user_id=user.id).first()
    if existing is not None:
        session.close()
        return "already_joined"

    session.add(FanClubMember(club_id=club_id, user_id=user.id))
    session.commit()
    session.close()
    return "joined"
