from sqlalchemy.sql.functions import current_time

from functions import *

def create_poll(artist_id, question, closes_at, options):

    session = Session()

    poll = Poll(artist_id=artist_id, question=question, opens_at=datetime.now(),closes_at=closes_at)
    poll_options = []
    for option in options:
        poll_options.append(PollOption(option))


    session.add(poll)
    session.add_all(poll_options)
    session.commit()

