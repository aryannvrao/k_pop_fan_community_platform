from datetime import date
from functions import Session, engine, Poll, PollOption, Vote


def vote_in_poll(poll_id, option_id, user_id):
    session = Session(engine)

    poll = session.get(Poll, poll_id)
    if poll is None:
        session.close()
        return "poll_not_found"

    today = date.today()
    if today < poll.opens_at or today > poll.closes_at:
        session.close()
        return "poll_closed"

    option = session.query(PollOption).filter_by(id=option_id, poll_id=poll_id).first()
    if option is None:
        session.close()
        return "option_not_found"

    existing_vote = session.query(Vote).filter_by(poll_id=poll_id, user_id=user_id).first()
    if existing_vote is not None:
        session.close()
        return "already_voted"

    vote = Vote(poll_id=poll_id, option_id=option_id, user_id=user_id)
    session.add(vote)
    session.commit()
    session.close()
    return "voted"