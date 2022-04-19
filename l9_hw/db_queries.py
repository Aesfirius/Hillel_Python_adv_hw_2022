from l9_hw.db_models import *


###########################################
#                 ARTIST                  #
###########################################


def get__all_artists():
    """
    All artists in track list
    :return: [{artist_Row_1}, {artist_Row_2}]
    """
    artists_data = artist.query\
        .join(track_list, track_list.id_artist == artist.id_artist)\
        .order_by(artist.artist_name).all()
    return artists_data


def get__artist__by_id(id_artist):
    """
    Artist data by Artist id
    :param id_artist:
    :return: artist_data (Row) | None
    """
    artist_data = artist.query\
        .with_entities(artist.id_artist, artist.artist_name, artist.artist_info)\
        .filter(artist.id_artist == id_artist).first()
    return artist_data


def get__id_artist__by_name(artist_name):
    """
    Artist data by Artist name
    :param artist_name:
    :return: artist_data (Row.id_artist)
    """
    artist_data = artist.query \
        .with_entities(artist.id_artist) \
        .filter(artist.artist_name == artist_name).first()
    return artist_data


def get__search_all_artists__by_like(search_text):
    """
    Find All Artists with artist_name like search_text
    :param search_text: Search request
    :return: id_artist, artist_name
    """
    artists_data = artist.query \
        .with_entities(artist.id_artist, artist.artist_name) \
        .filter(artist.artist_name.like(f'%{search_text}%')).all()
    return artists_data


def insert__new_artist(new_artist_name, new_artist_info):
    """
    Add new artist data
    """
    new_artist_data = artist(artist_name=new_artist_name, artist_info=new_artist_info)
    create_(new_artist_data)


def fn_insert__new_artist(artist_name, artist_info):
    """
    Insert new artist if not exists by name
    :param artist_name: new artist name
    :param artist_info: new artist info
    :return: new artist id
    """
    artist_data = get__id_artist__by_name(artist_name)
    if artist_data is None:
        insert__new_artist(artist_name, artist_info)
        artist_data = get__id_artist__by_name(artist_name)
    return artist_data.id_artist


###########################################
#                 ALBUM                   #
###########################################

def get__all_artist_albums(id_artist):
    """
    Get all artist albums by id_artist
    :return: albums_data Row(id_album, album_title)
    """
    albums_data = album.query \
        .with_entities(album.id_album, album.album_title) \
        .join(track_list, track_list.id_album == album.id_album) \
        .join(artist, track_list.id_artist == artist.id_artist) \
        .filter(artist.id_artist == id_artist) \
        .order_by(album.album_year).distinct().all()
    return albums_data


def get__album__by_id(id_album):
    """
    Get album data by id_album
    :param id_album:
    :return: album_data (Row)
    """
    album_data = album.query \
        .with_entities(album.id_album, album.album_title, album.album_year, album.album_info) \
        .filter(album.id_album == id_album).first()
    return album_data


def get__id_album__by_title(album_title):
    """
    Get album data by album_title
    :param album_title:
    :return: album_data (Row.id_album)
    """
    album_data = album.query \
        .with_entities(album.id_album) \
        .filter(album.album_title == album_title).first()
    return album_data


def get__search_all_albums__by_like(search_text):
    """
    Find All Albums with album_title like search_text
    :param search_text: Search request
    :return: [{Row(id_artist, id_album, album_title)}, {}]
    """
    albums_data = album.query \
        .with_entities(track_list.id_artist, album.id_album, album.album_title) \
        .join(track_list, track_list.id_album == album.id_album) \
        .filter(album.album_title.like(f'%{search_text}%')).distinct().all()
    return albums_data


def insert__new_album(new_album_title, new_album_year, new_album_info):
    """
    Add new album data
    """
    new_album_data = album(album_title=new_album_title,
                           album_year=new_album_year,
                           album_info=new_album_info)
    create_(new_album_data)


def fn_insert__new_album(album_title, album_year, album_info):
    album_data = get__id_album__by_title(album_title)
    if album_data is None:
        if not isinstance(album_year, int) and album_year not in ['', None]:
            album_year = int(album_year)
        insert__new_album(album_title, album_year, album_info)
        album_data = get__id_album__by_title(album_title)
    return album_data.id_album


###########################################
#                  SONG                   #
###########################################

def get__song__by_id(id_song):
    """
    Get song data by id_song
    :param: id_song
    :return: song_data (Row(id_song, song_title, song_year, song_text, origin_lang))
    """
    song_data = song.query.filter(song.id_song == id_song).first()
    return song_data


def get__all_songs_not_in_album(id_artist):
    """
    Get all artist songs not in album by id_artist
    :return: songs_data Row(id_artist, artist_name, id_song, song_title, song_year)
    """
    songs_data = song.query \
        .with_entities(artist.id_artist, artist.artist_name, song.id_song, song.song_title, song.song_year) \
        .join(track_list, track_list.id_song == song.id_song) \
        .join(artist, track_list.id_artist == artist.id_artist) \
        .filter(track_list.id_artist == id_artist) \
        .filter(track_list.id_album == None) \
        .order_by(song.song_year).all()
    return songs_data


def get__all_album_songs(id_artist, id_album):
    """
    Get all album songs by (id_artist, id_album)
    :return: songs_data Row(id_artist, artist_name, id_song, song_title, song_year, track_number)
    """
    songs_data = song.query \
        .with_entities(artist.id_artist, artist.artist_name,
                       song.id_song, song.song_title, song.song_year,
                       track_list.track_number) \
        .join(track_list, track_list.id_song == song.id_song) \
        .join(artist, track_list.id_artist == artist.id_artist) \
        .join(album, track_list.id_album == album.id_album) \
        .filter(track_list.id_artist == id_artist) \
        .filter(track_list.id_album == id_album) \
        .order_by(track_list.track_number).all()
    return songs_data


def get__song_track__by_id(id_artist, id_song):
    """
    Get song data by (id_artist, id_song)
    :param: id_artist, id_song
    :return: song_data (Row(id_song, song_title, song_year, song_text, origin_lang))
    """
    song_data = song.query \
        .with_entities(song.id_song, song.song_title, song.song_year, song.song_text, song.origin_lang) \
        .join(track_list, track_list.id_song == song.id_song) \
        .join(artist, track_list.id_artist == artist.id_artist) \
        .filter(track_list.id_artist == id_artist) \
        .filter(track_list.id_song == id_song).first()
    return song_data


def get__search_all_songs__by_like(search_text):
    """
    Find All Songs with song_title like search_text
    :param search_text: Search request
    :return: [{Row(id_artist, id_album, id_song, song_title)}, {}]
    """
    songs_data = track_list.query \
        .with_entities(track_list.id_artist, track_list.id_album, song.id_song, song.song_title) \
        .join(song, track_list.id_song == song.id_song) \
        .filter(song.song_title.like(f'%{search_text}%')).distinct().all()
    return songs_data


def get__id_song__by_title(song_title):
    """
    Get song data by song_title
    :param song_title:
    :return: song_data (Row.id_song)
    """
    song_data = song.query.filter(song.song_title == song_title).first()
    return song_data


def insert__new_song(new_song_title, new_song_year, new_song_text, new_origin_lang):
    """
    Add new song data
    """
    new_song_data = song(song_title=new_song_title,
                         song_year=new_song_year,
                         song_text=new_song_text,
                         origin_lang=new_origin_lang)
    create_(new_song_data)


def fn_insert__new_song(song_title, song_text, song_year: int, song_lang):
    """
    Add new song if not exist
    :return: new is_song
    """
    song_data = get__id_song__by_title(song_title)
    if song_data is None:
        if not isinstance(song_year, int) and song_year not in ['', None]:
            song_year = int(song_year)
        insert__new_song(song_title, song_year, song_text, song_lang)
        song_data = get__id_song__by_title(song_title)
    return song_data.id_song


def update__song_text(id_song, new_song_text):
    """
    Update song text
    :param: id_song, new_song_text
    """
    song_data = get__song__by_id(id_song)
    song_data.song_text = new_song_text
    do_commit()


def delete__song__by_id(id_song):
    """
    Delete song (from song table)
    """
    song_data = get__song__by_id(id_song)
    delete_(song_data)


def fn_delete__song(id_artist, id_song, id_album):
    """
    Delete Song from tables:
    track list
    song
    """
    delete__track(id_artist, id_song, id_album)
    delete__song__by_id(id_song)


###########################################
#               TRACK LIST                #
###########################################

def get__track(id_artist, id_song, id_album):
    """
    Get track data
    """
    if id_album in [0, '0', '']:
        id_album = None
    track_data = track_list.query\
        .filter(track_list.id_artist == id_artist) \
        .filter(track_list.id_song == id_song) \
        .filter(track_list.id_album == id_album).first()
    return track_data


def insert__new_track(new_artist_id, new_song_id, new_album_id, new_song_track_number):
    """
    Add new track data
    """
    new_track_data = track_list(id_artist=new_artist_id,
                                id_song=new_song_id,
                                id_album=new_album_id,
                                track_number=new_song_track_number)
    create_(new_track_data)


def fn_insert__new_track(id_artist, id_song, id_album, track_number):
    """
    Add new track if not exist
    """
    tracklist_data = get__track(id_artist, id_song, id_album)
    if tracklist_data is None:
        insert__new_track(id_artist, id_song, id_album, track_number)


def delete__track(id_artist, id_song, id_album):
    """
    Delete track
    """
    track_data = get__track(id_artist, id_song, id_album)
    delete_(track_data)


###########################################
###########################################
###########################################

def fn_add__song(data):
    """
    Add data(artist, song, album, track number) to track list
    """
    if data['song_info']['song_title'] not in ['', None]:
        song_id = fn_insert__new_song(song_title=data['song_info']['song_title'],
                                      song_text=data['song_info']['song_text'],
                                      song_year=int(data['song_info']['song_year']),
                                      song_lang=data['song_info']['song_lang'])
        if len(data['artist_info']) > 0:
            for artist_data in data['artist_info']:
                if artist_data['artist_name'] not in ['', None]:
                    artist_id = fn_insert__new_artist(artist_name=artist_data['artist_name'],
                                                      artist_info=artist_data['artist_info'])
                    if len(artist_data['album_info']) > 0:
                        for album_data in artist_data['album_info']:
                            if album_data['album_title'] not in ['', None]:
                                album_id = fn_insert__new_album(album_title=album_data['album_title'],
                                                                album_year=album_data['album_year'],
                                                                album_info=album_data['album_info'])
                                fn_insert__new_track(id_artist=int(artist_id),
                                                     id_song=int(song_id),
                                                     id_album=int(album_id),
                                                     track_number=int(album_data['track_number']))
                            else:
                                fn_insert__new_track(id_artist=artist_id, id_song=song_id,
                                                     id_album=None,
                                                     track_number=None)
                    else:
                        fn_insert__new_track(id_artist=artist_id, id_song=song_id, id_album=None, track_number=None)
