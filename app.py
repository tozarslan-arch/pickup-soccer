from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from models import db, Location, Event, Vote

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///soccer.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.after_request
def add_header(response):
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    return response


@app.route("/", methods=["GET"])
def index():
    locations = Location.query.order_by(Location.name).all()
    now = datetime.now()

    upcoming = (
        Event.query
        .filter(Event.date_time >= now)
        .order_by(Event.date_time)
        .all()
    )

    cutoff = now - timedelta(days=60)

    old_games = Event.query.filter(Event.date_time < cutoff).all()
    for g in old_games:
        db.session.delete(g)
    db.session.commit()

    past = (
        Event.query
        .filter(Event.date_time < now)
        .filter(Event.date_time >= cutoff)
        .order_by(Event.date_time.desc())
        .all()
    )

    return render_template(
        "index.html",
        locations=locations,
        upcoming=upcoming,
        past=past,
        now=now
    )


@app.route("/locations/add", methods=["POST"])
def add_location():
    name = request.form.get("location_name", "").strip()
    address = request.form.get("location_address", "").strip()

    if name and address:
        existing = Location.query.filter_by(name=name).first()
        if not existing:
            loc = Location(name=name, address=address)
            db.session.add(loc)
            db.session.commit()

    return redirect(url_for("index"))


@app.route("/locations/<int:location_id>/edit", methods=["POST"])
def edit_location(location_id):
    loc = Location.query.get_or_404(location_id)
    name = request.form.get("location_name", "").strip()
    address = request.form.get("location_address", "").strip()

    if name and address:
        loc.name = name
        loc.address = address
        db.session.commit()

    return redirect(url_for("index"))


@app.route("/locations/<int:location_id>/delete", methods=["POST"])
def delete_location(location_id):
    loc = Location.query.get_or_404(location_id)
    db.session.delete(loc)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/events/add", methods=["POST"])
def add_event():
    location_id = request.form.get("location_id")
    date_str = request.form.get("date")

    # DEFAULT TIME
    time_str = request.form.get("time") or "10:00"

    # DEFAULT MIN PLAYERS = 8
    target_str = request.form.get("target")
    target = int(target_str) if target_str else 8

    # NORMALIZE NOTE
    note_raw = request.form.get("note", "")
    note = note_raw.strip()
    if not note:
        note = None

    # Only require location + date
    if not (location_id and date_str):
        return redirect(url_for("index"))

    dt = datetime.fromisoformat(f"{date_str}T{time_str}")

    event = Event(
        location_id=int(location_id),
        date_time=dt,
        target=target,
        note=note
    )

    db.session.add(event)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/events/<int:event_id>/vote", methods=["POST"])
def vote_event(event_id):
    event = Event.query.get_or_404(event_id)
    vote = Vote(event=event)
    db.session.add(vote)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/events/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
