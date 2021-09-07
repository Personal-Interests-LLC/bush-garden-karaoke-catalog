import os
import csv
from collections import defaultdict
from datetime import datetime
from config import db
from models import Artist, Song

def initialize_artist_and_songs(combined_name, first_name, last_name, song_set):
    a = Artist(full_name=combined_name, first_name=first_name, last_name=last_name)
    for song in song_set:
        song_name, reference_id, set_timestamp = song
        a.songs.append(Song(
            song_name=song_name,
            reference_id=reference_id,
            timestamp=datetime.now()
            ))
    db.session.add(a)
    return


reader = csv.DictReader(open('magictrax_songbook.csv'))
result = {}
for row in reader:
    key = row.pop('key')
    if key in result:
        pass
    result[key] = row

artist_dict = defaultdict(list)
for key in result:
    # create dict with artist name as key and array of sets representing songs
    artist_dict[result[key]["artist_full_name"]].append(
        (
            result[key]["song_name"],
            result[key]["reference_id"],
            format(datetime.now())
        )
    )

# Delete db file if it already exists
if os.path.exists('kcatalog.db'):
    os.remove('kcatalog.db')

# Create the db
db.create_all()

sorted_dict = dict(sorted(artist_dict.items()))
for artist in sorted_dict:
    if ',' in artist:
        split_name = artist.split(', ')
        last_name = split_name[0]
        first_name = split_name[1]
        if 'The' in split_name:
            combined_name = f"{first_name} {last_name}"
            initialize_artist_and_songs(combined_name, last_name, last_name, sorted_dict[artist])
        else:
            combined_name = f"{first_name} {last_name}"
            initialize_artist_and_songs(combined_name, first_name, last_name, sorted_dict[artist])
    else:
        initialize_artist_and_songs(artist, artist, artist, sorted_dict[artist])
db.session.commit()