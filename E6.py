from sqlalchemy import func
from sqlalchemy.orm import Session
from functions import engine, FanClub, FanClubMember


def fanclub_to_dict(f, member_count=0):
    return {
        "id": f.id,
        "name": f.name,
        "artist_id": f.artist_id,
        "created_by": f.created_by,
        "member_count": member_count,
    }


def get_fanclubs(artist_id=None, name=None):
    session = Session(engine)

    query = session.query(FanClub, func.count(FanClubMember.id)) \
        .outerjoin(FanClubMember, FanClubMember.club_id == FanClub.id) \
        .group_by(FanClub.id)

    if artist_id is not None:
        query = query.filter(FanClub.artist_id == artist_id)
    if name is not None:
        query = query.filter(FanClub.name.ilike(name))

    result = []
    for club, member_count in query.order_by(FanClub.id).all():
        result.append(fanclub_to_dict(club, member_count))

    session.close()
    return result
