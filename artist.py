# routes associated with artists
from flask import make_response, abort
# importing db, models
from config import db
from models import Artist, ArtistSchema, Song 


# handler for read (GET) artist function
def read_all():
    """
    This function responds to a request for /api/artist
    with the complete lists of artist
    :return:    sorted list of artist and their songs
    """
    artist = Artist.query.order_by(Artist.full_name).all()

    # Serialize the data 
    artist_schema = ArtistSchema(many=True)

    # the list of artists
    return artist_schema.dump(artist)


def read_one(artist_id):
    """
    This function responds to a request for /api/artist/{artist_id}
    with one matching artist from artist
    :param artist_id:  integer ID of the artist to find in the db
    :return:    artist matching ID and all assoc songs
    """
    artist = Artist.query.filter(Artist.artist_id == artist_id).outerjoin(Song).one_or_none()

    if artist is not None:
        artist_schema = ArtistSchema()
        return artist_schema.dump(artist)
    else:
        abort(
            404,
            f'Could not find artist with ID: {artist_id}'
        )


# handler for create (POST) artist
def create(artist):
    """
    This function creates a new artist in the artist structure
    based on the passed in artist data
    :param artist:  artist to create in artist structure
    :return:    201 on success, 406 on artist exists
    """
    full_name = artist.get("full_name", None)

    existing_artist = Artist.query.filter(Artist.full_name == full_name).one_or_none()

    # Conditional for new artist
    if existing_artist is None:

        # create new artist using the Artist schema
        artist_schema = ArtistSchema()
        new_artist = artist_schema.load(artist, session=db.session)
        # add artist to db
        db.session.add(new_artist)
        db.session.commit()
        # serialize and return newly created artist in result
        return artist_schema.dump(new_artist), 201
    # otherwise if artist already exists
    else:
        return abort(409, f'Artist {full_name} already exists')


def update(artist_id, artist):
    """
    This function updates an existing artist in the artist structure
    :param artist_id:   artist ID of artist to update in artist structure
    :param artist:  artist to update
    :return:        updated artist structure
    """
    full_name = artist.get('full_name')

    # Does the artist ID actually exist in db
    update_artist = Artist.query.filter(Artist.artist_id == artist_id).one_or_none()

    # Is there a artist with these attributes already existing in db
    existing_artist = Artist.query.filter(Artist.full_name == full_name).one_or_none()

    if update_artist is None:
        return abort(404, f'Artist not found for {artist_id}')
    # If there's a artist in the db with matching attributes but a different ID than the one passed by customer
    elif existing_artist is not None and existing_artist.artist_id != artist_id:
        return abort(409, f'Artist {full_name} already exists')
    # Else update this artist
    else:
        # Turn the passed in artist object into db object
        artist_schema = ArtistSchema()
        update = artist_schema.load(artist, session=db.session)

        # Set the id of the new artist db object to the artist I want to update
        update.artist_id = update_artist.artist_id

        # merge new object into the old and commit to the db
        db.session.merge(update)
        db.session.commit()

        # return serialized updated artist data
        return artist_schema.dump(update_artist), 200


def delete(artist_id):
    """
    This function deletes a artist from the artist table
    :param artist_id:   Artist ID of artist to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does artist id exist in db?
    delete_artist = Artist.query.filter(Artist.artist_id == artist_id).one_or_none()

    if delete_artist is not None:
        db.session.delete(delete_artist)
        db.session.commit()
        return make_response(
                f'Successfully deleted artist with ID: {artist_id}',
            200
        )
    # otherwise, no artist to delete found
    else:
        abort(
            404,
            f'Could not find artist with ID: {artist_id}' 
            )
