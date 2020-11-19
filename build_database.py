import os
from config import db
from models import Artist, Song 
from datetime import datetime

# Data to initialize db with
ARTIST = [
    {
        "full_name": "Lex Oconnel",
        "first_name": "Lex",
        "last_name": "Oconnel",
        "songs": [
            ("Song1", "1E2B", "2020-02-06 22:17:54"),
            ("Turkey Time", "2B8J", "2008-05-08 22:17:54"),
        ],
    },
    {
        "first_name": "David King",
        "last_name": "",
        "full_name": "",
        "songs": [
            ("Yum that sounds perf","28BBD","2009-01-01 22:17:54",),
            ("Maybe next time","234F", "1992-02-06 22:17:54",),
        ],
    },
    {
        "first_name": "",
        "last_name": "Salmon Man",
        "full_name": "My my",
        "songs": [
            ("Tuna Roe", "TR89", "2001-01-05 22:47:54"),
            ("Please don't", "8UY9","1988-12-06 22:17:54"),
        ],
    },
]


# Delete db file if it already exists
if os.path.exists('kcatalog.db'):
    os.remove('kcatalog.db')

# Create the db
db.create_all()

# Iterate over ARTIST struct and populate the db
for artist in ARTIST:
    a = Artist(last_name=artist['last_name'], full_name=artist['full_name'], first_name=artist['first_name'])

    # Add songs for each artist
    for song in artist.get("songs"):
        song_name, reference_id, timestamp = song
        a.songs.append(
                Song(
                    song_name=song_name,
                    reference_id=reference_id,
                    timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    )
                )

    db.session.add(a)

db.session.commit()
