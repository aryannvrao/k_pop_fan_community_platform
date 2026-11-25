from functions import *


def get_poll_results(poll_id):
    session = Session(engine)

    poll = session.get(Poll, poll_id)
    if poll is None:
        session.close()
        return None

    options = session.query(PollOption).filter_by(poll_id=poll_id).all()
    results = []
    total_votes = 0
    for option in options:
        votes_count = session.query(Vote).filter_by(poll_id=poll_id, option_id=option.id).count()
        total_votes += votes_count
        results.append({
            "option_id": option.id,
            "text": option.text,
            "votes": votes_count
        })

    data = {
        "poll_id": poll.id,
        "artist_id": poll.artist_id,
        "question": poll.question,
        "opens_at": poll.opens_at,
        "closes_at": poll.closes_at,
        "total_votes": total_votes,
        "results": results
    }
    session.close()
    return data
