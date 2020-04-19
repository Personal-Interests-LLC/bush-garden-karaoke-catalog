from datetime import datetime
from marshmallow import fields
from config import db, ma


class Artist(db.Model):
    """
    Artist model definition, basic naming assumptions
    TODO: need hands on current records to know
    which fields we actually need here
    """
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128), index=True)
    last_name = db.Column(db.String(32))
    first_name = db.Column(db.String(32))
    # relationship of song to artist
    songs = db.relationship(
            'Song',
            backref='artist',
            cascade='all, delete, delete-orphan',
            single_parent=True,
            order_by='desc(Song.song_name)'
            )


class Song(db.Model):
    """
    Song model definition, basic naming assumptions
    TODO: need hands on current records to know
    which fields we actually need here
    """
    __tablename__ = 'song'
    song_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'))
    song_name = db.Column(db.String(128))
    reference_id = db.Column(db.String(32))
    timestamp = db.Column(
            db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
            )


class ArtistSchema(ma.ModelSchema):
    class Meta:
        model = Artist
        sqla_session = db.session
    songs = fields.Nested('ArtistSongSchema', default=[], many=True)


class ArtistSongSchema(ma.ModelSchema):
    """
    circumvent recursion issue - defines what a 
    Song object looks like as Marshmallow 
    serializes the songs list
    """
    song_name = fields.Str()
    song_id = fields.Int()
    artist_id = fields.Int()
    reference_id = fields.Str()


class SongSchema(ma.ModelSchema):
    class Meta:
        model = Song
        sqla_session = db.session
    artist = fields.Nested('SongArtistSchema', default=None)


class SongArtistSchema(ma.ModelSchema):
    """
    circumvent recursion issue - defines what a 
    SongSchema.artist attribute looks like
    """
    artist_id = fields.Int()
    full_name = fields.Str()
    last_name = fields.Str()
    first_name = fields.Str()
    timestamp = fields.Str()
