from app import app, db
from models import Location

locations = [
    # --- NEW LOCATIONS YOU JUST PROVIDED ---
    ("Franz Park", "https://goo.gl/maps/9kovEVZTjvVMDpWK9"),
    ("Gay Field", "https://goo.gl/maps/9RDddjeHS35Lc5en9"),
    ("Heartland Park", "https://goo.gl/maps/wzkn6AcLrKmZicF79"),
    ("Heman Park", "https://goo.gl/maps/jTMcPG8kTjQ9DgbD6"),
    ("Fenton Sports Complex", "https://maps.app.goo.gl/xzWSXHbqv3BKQhxeA"),
    ("Ladue 5th Grade Center", "https://goo.gl/maps/DWQjxFRMo3UzMAEK9"),
    ("Ladue HS", "https://maps.app.goo.gl/K5qU8eCFzNfxGocm6"),
    ("Logan Chiropractic College", "https://goo.gl/maps/sVCcSS3qhG6tjZV7"),
    ("Maplewood HS", "https://maps.app.goo.gl/RWnihYzAuERayikE9"),
    ("Mehlville HS", "https://goo.gl/maps/ushkevZ2oNTUgRcM6"),
    ("medical field", "https://goo.gl/maps/8hY6TU8vAF8amZMD6"),
    ("O'Fallon Sports Park", "https://goo.gl/maps/oakjRhzTdKvqmND78"),
    ("Pacific-Liberty Fields", "https://maps.app.goo.gl/4NEHMRwibb3VVZf7"),
    ("Parkway North HS", "https://goo.gl/maps/pCvhWTgLEh22UFYo9"),
    ("Parkway Central HS", "https://goo.gl/maps/ECsu6M93fCZTZDJ67"),
    ("Parkway Central Middle", "https://goo.gl/maps/mBrzgzdMxtZPpoNm7"),
    ("Parkway South", "https://maps.app.goo.gl/RCJLsCK6S8AT8BZ27"),
    ("Ryan Hummert Park", "https://goo.gl/maps/18Nz2GLYacUEnv8LA"),
    ("Shaw Park (Soccer field 1)", "https://goo.gl/maps/38sNZWcf8wiQjDHs5"),
    ("Southview", "https://goo.gl/maps/h3M5QwM6rEjhMc7c9"),
    ("Sunset Hills Bermuda", "https://goo.gl/maps/syUYPmRB2NoGJ1Fq5"),
    ("Tiemeyer Park", "https://maps.app.goo.gl/AB2nsGZCQaVedFdn7"),
    ("Tower Grove Park", "https://goo.gl/maps/1mkjueMeWRWC92or5"),
    ("Ucity HS", "https://maps.app.goo.gl/GWx8B2UJLsLSeWAw7"),
    ("Vandevender", "https://goo.gl/maps/3jhJeecJ4aKaUeYNA"),
    ("Wash U South", "https://goo.gl/maps/8nnsQaa5i97qNi2EA"),
    ("Watson Trails Park", "https://goo.gl/maps/HshwPK8DRYEHP1WEA"),
    ("Webster Groves in-line rink & courts", "https://goo.gl/maps/2ThTZiZx8UyXR5WL9"),
    ("Wehner Park", "https://goo.gl/maps/m3xXDEHazr6Xhq1Ur"),
    ("Whitecliff Park", "https://goo.gl/maps/ALTjBYPfEG6sXmGTT"),
    ("Wilmore Park", "https://goo.gl/maps/Ydcfo9U4xnpvxZMv7"),
    ("Wilmore Futsal", "https://goo.gl/maps/BsJzmuipuk2TFp2c8"),
]

with app.app_context():
    for name, address in locations:
        if not Location.query.filter_by(name=name).first():
            db.session.add(Location(name=name, address=address))
    db.session.commit()

print("New locations added.")
