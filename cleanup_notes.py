from app import app, db
from models import Event

with app.app_context():
    fixed = 0
    events = Event.query.all()

    for e in events:
        # Normalize empty or whitespace notes
        if not e.note or not e.note.strip():
            e.note = None
            fixed += 1

    db.session.commit()

    print(f"Cleanup complete. Fixed {fixed} events.")
