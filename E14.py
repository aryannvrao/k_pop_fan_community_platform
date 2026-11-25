from functions import Session, engine, Event


def create_event(name, date, venue, participant_limit):
    if participant_limit <= 0:
        return "invalid_limit"

    session = Session(engine)
    event = Event(
        name=name,
        date=date,
        venue=venue,
        participant_limit=participant_limit
    )
    session.add(event)
    session.commit()
    event_id = event.id
    session.close()
    return event_id
