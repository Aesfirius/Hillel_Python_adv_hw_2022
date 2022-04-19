from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class artist(db.Model):
    """
        CREATE TABLE "artist" (
        "id_artist"	INTEGER NOT NULL UNIQUE,
        "artist_name"	TEXT NOT NULL UNIQUE,
        "artist_info"	TEXT,
        PRIMARY KEY("id_artist" AUTOINCREMENT)
        )
    """
    id_artist = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    artist_name = db.Column(db.Text, nullable=False, unique=True)
    artist_info = db.Column(db.Text, nullable=True)


class album(db.Model):
    """
        CREATE TABLE "album" (
        "id_album"	INTEGER NOT NULL UNIQUE,
        "album_title"	TEXT NOT NULL,
        "album_year"	INTEGER NOT NULL,
        "album_info"	TEXT,
        PRIMARY KEY("id_album" AUTOINCREMENT)
        )
    """
    id_album = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    album_title = db.Column(db.Text, nullable=False)
    album_year = db.Column(db.Integer, nullable=False)
    album_info = db.Column(db.Text, nullable=True)


class song(db.Model):
    """
        CREATE TABLE "song" (
        "id_song"	INTEGER NOT NULL UNIQUE,
        "song_title"	TEXT NOT NULL,
        "song_year"	INTEGER NOT NULL,
        "song_text"	TEXT NOT NULL,
        "origin_lang"	TEXT NOT NULL,
        PRIMARY KEY("id_song" AUTOINCREMENT)
    )
    """
    id_song = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    song_title = db.Column(db.Text, nullable=False)
    song_year = db.Column(db.Integer, nullable=False)
    song_text = db.Column(db.Text,  nullable=False, unique=True)
    origin_lang = db.Column(db.Text, nullable=True)


class track_list(db.Model):
    """
    CREATE TABLE "track_list" (
        "id_tl"	INTEGER NOT NULL UNIQUE,
        "id_artist"	INTEGER NOT NULL,
        "id_song"	INTEGER NOT NULL,
        "id_album"	INTEGER,
        "track_number"	INTEGER,
        PRIMARY KEY("id_tl" AUTOINCREMENT),
        FOREIGN KEY("id_song") REFERENCES "song"("id_song"),
        FOREIGN KEY("id_artist") REFERENCES "artist"("id_artist"),
        FOREIGN KEY("id_album") REFERENCES "album"("id_album")
    )
    """
    id_tl = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    id_artist = db.Column(db.Integer, db.ForeignKey('artist.id_artist'), nullable=False)
    id_song = db.Column(db.Integer, db.ForeignKey('song.id_song'), nullable=False)
    id_album = db.Column(db.Integer, db.ForeignKey('album.id_album'))
    track_number = db.Column(db.Integer)


def do_commit():
    db.session.commit()


def delete_(obj_in):
    db.session.delete(obj_in)
    do_commit()


def create_(obj_in):
    db.session.add(obj_in)
    do_commit()
