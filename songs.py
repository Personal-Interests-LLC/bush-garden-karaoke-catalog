# songs CRUD stuffffffffff
from flask import abort, make_response
from models import Song, SongSchema, Artist
from config import db


def read_all():
    """
    this function responds to a requet
    to /api/songs and returns all songs
    sorted by song name
    :return:    json list of all songs for all people
    """
    # Query the db for all songs
    songs = Song.query.order_by(Song.song_name).all()
    # Serialize the list of songs from our data
    song_schema = SongSchema(many=True)
    data = song_schema.dump(songs)
    return data


def read_one(artist_id, song_id):
    """
    This function responds to a request for
    /api/people/{artist_id}/songs/{song_id}
    with one matching song for the associated artist

    :param artist_id:       Id of artist the song is related to
    :param song_id:         Id of the song
    :return:                json string of song contents
    """
    # Query db for the song
    # First make query to join artist with songs
    # Then filter for input parameters
    song = (
            Song.query.join(Artist, Artist.artist_id == Song.artist_id)
            .filter(Artist.artist_id == artist_id)
            .filter(Song.song_id == song_id)
            .one_or_none()
            )

    # Was a song found
    if song is not None:
        song_schema = SongSchema()
        data = song_schema.dump(song)
        return data

    else:
        abort(404, f'Song not found for ID: {song_id}')


def create(artist_id, song):
    """
    Create a new song associated with ID of a db artist 
    :param artist_id:   int, id of artist assoc with song 
    :param song:        str, text content of the song to create
    :return:            201, successfully created song
    """
    # get the parent artist for the song
    artist = Artist.query.filter(Artist.artist_id == artist_id).one_or_none()

    if artist is None:
        abort(404, f'Artist not found for ID: {artist_id}')
    
    song_schema = SongSchema()

    for existing_song in artist.songs:
        if existing_song.song_name == song['song_name']:
            abort(409, 'Artist {artist} already has a song named: {song}'.format(artist=artist.full_name, song=song['song_name']))

    # init a song schema instance
    new_song = song_schema.load(song, session=db.session)

    artist.songs.append(new_song)
    db.session.commit()

    # Serialize and return the newly created song
    data = song_schema.dump(new_song)
    return data, 201


def update(artist_id, song_id, song):
    """
    :param artist_id:  
    :param song_id:  
    :param song:  
    :return:
    """
    # Query for song assoc with artist_id param that has song_id param
    update_song = (
            Song.query.filter(Artist.artist_id == artist_id)
            .filter(Song.song_id == song_id)
            .one_or_none()
            )

    if update_song is not None:
        # turn passed in song to db object
        schema = SongSchema()
        update = schema.load(song, session=db.session)

        # set new obj id to song we want to modify
        update.artist_id = update_song.artist_id
        update.song_id = update_song.song_id

        # merge new obj to old and commit
        db.session.merge(update)
        db.session.commit()
        
        # return updated song in response
        return schema.dump(update_song), 200

    else:
        abort(404, f'Song not found for ID: {song_id}')


def delete(artist_id, song_id):
    """
    :param artist_id:
    :param song_id:
    :return: 200 on success, 404 on failure
    """
    song_query = (
            Song.query.filter(Artist.artist_id == artist_id)
            .filter(Song.song_id == song_id)
            .one_or_none()
            )

    if song_query is not None:
        db.session.delete(song_query)
        db.session.commit()
        return make_response(
                f'Song {song_id} deleted.', 200)

    else:
        abort(404, f'Song not found for id: {song_id}')
