from functions import Session, engine, Event, EventRegistration


def register_for_event(event_id, user_id):
    session = Session(engine)

    event = session.get(Event, event_id)
    if event is None:
        session.close()
        return "event_not_found"

    existing = session.query(EventRegistration).filter_by(event_id=event_id, user_id=user_id).first()
    if existing is not None:
        session.close()
        return "already_registered"

    current_count = session.query(EventRegistration).filter_by(event_id=event_id).count()
    if current_count >= event.participant_limit:
        session.close()
        return "event_full"

    registration = EventRegistration(event_id=event_id, user_id=user_id)
    session.add(registration)
    session.commit()
    session.close()
    return "registered"
