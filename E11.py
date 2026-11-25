from functions import Session, engine, Poll, PollOption, Artist


def create_poll(artist_id, question, opens_at, closes_at, options):
    session = Session(engine)

    artist = session.get(Artist, artist_id)
    if artist is None:
        session.close()
        return "artist_not_found"

    if len(options) < 2:
        session.close()
        return "invalid_options"

    if closes_at <= opens_at:
        session.close()
        return "invalid_dates"

    poll = Poll(
        artist_id=artist_id,
        question=question,
        opens_at=opens_at,
        closes_at=closes_at
    )
    session.add(poll)

    poll_options = []
    for option in options:
        poll_options.append(PollOption(poll_id=poll.id, text=option))

    session.add_all(poll_options)
    session.commit()
    poll_id = poll.id
    session.close()
    return poll_id

