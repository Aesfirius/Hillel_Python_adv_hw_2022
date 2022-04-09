import os
import sqlite3


def db_req(sql_query):
    """
    :param sql_query: SQL query
    :return: [{k1:v1, k2:v1}, {k3:v3, k4:v4}]
    """
    db_name = os.environ.get('DB_NAME')
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql_query)
    result = [dict(i) for i in cur.fetchall()]
    con.commit()
    con.close()
    return result


def get_last_inserted_row_id():
    return "select last_insert_rowid()"


###########################################
#                 ARTIST                  #
###########################################

def get_last_artist_id():
    """
    :return: id_artist
    """
    return """
    SELECT artist.id_artist
    FROM artist
    ORDER BY
        artist.id_artist DESC
        LIMIT 1;"""


def query_all_artists():
    """
    All artists in track list
    :return: [{id_artist, artist_name}] ?
    """
    return '''
    SELECT DISTINCT artist.id_artist, artist.artist_name
    FROM rel_table 
    INNER JOIN artist
    ON rel_table.id_artist = artist.id_artist
    ORDER BY artist_name;'''


def query_artist_by_id(id_artist):
    """
    :param id_artist:
    :return: id_artist, artist_name, artist_info
    """
    return f'''
    SELECT artist.id_artist, artist.artist_name, artist.artist_info
    FROM artist
    WHERE artist.id_artist = "{id_artist}"'''


def query_artist_by_name(artist_name):
    """
    Artist data by Artist name
    :param artist_name:
    :return: id_artist, artist_name, artist_info
    """
    return f'''
    SELECT artist.id_artist, artist.artist_name, artist.artist_info
    FROM artist
    WHERE artist.artist_name = "{artist_name}"'''


def query_search_all_artists_by_like(search_text):
    """
    Artists
    :param search_text: Search request
    :return: id_artist, artist_name
    """
    return f"""
    SELECT id_artist, artist_name
    FROM artist
    WHERE artist.artist_name like '%{search_text}%';"""


def query_insert_new_artist(*args):
    """
    where -> (artist_name, artist_info)
    what  -> args -> (new_artist_name, new_artist_info)
    """
    return f"""
    INSERT INTO artist (artist_name, artist_info)
    VALUES {args}"""


def fn_insert_artist(artist_name, artist_info):
    """
    Insert new artist
    :param artist_name: new artist name
    :param artist_info: new artist info
    :return: new artist id
    """
    artist_data = db_req(query_artist_by_name(artist_name))
    if not artist_data:  # [] < 1
        db_req(query_insert_new_artist(artist_name, artist_info))
        artist_data = db_req(query_artist_by_name(artist_name))
    return artist_data[0]['id_artist']


###########################################
#                 ALBUM                   #
###########################################

def get_last_album_id():
    return """
    SELECT album.id_album
    FROM album
    ORDER BY
        album.id_album DESC
        LIMIT 1;"""


def query_all_albums(id_artist):
    return f'''
    SELECT DISTINCT artist.id_artist, artist.artist_name, album.id_album, album.album_title, album.album_year
    FROM rel_table
    INNER JOIN artist, album
    ON rel_table.id_artist = artist.id_artist
    AND rel_table.id_album = album.id_album
    WHERE artist.id_artist = "{id_artist}"
    ORDER BY album.album_year;'''


def query_album_info(id_album):
    return f'''
    SELECT album.id_album, album.album_title, album.album_year, album.album_info
    FROM album 
    WHERE album.id_album = "{id_album}"'''


def query_album_info_by_title(album_title):
    return f'''
    SELECT album.id_album, album.album_title, album.album_year, album.album_info
    FROM album 
    WHERE album.album_title = "{album_title}"'''


def query_insert_new_album(*args):
    """
    where -> (album_title, album_year, album_info)
    what  -> (new_album_title, int(new_album_year), new_album_info)
    """
    return f"""
    INSERT INTO album (album_title, album_year, album_info)
    VALUES {args}"""


def query_search_all_albums_by_like(search_text):
    return f"""
    SELECT DISTINCT rel_table.id_artist, album.id_album, album.album_title
    FROM rel_table
    INNER JOIN album
    ON rel_table.id_album = album.id_album
    WHERE album.album_title like '%{search_text}%';"""


def fn_insert_album(album_title, album_year, album_info):
    album_data = db_req(query_album_info_by_title(album_title))
    if len(album_data) < 1:
        if not isinstance(album_year, int) and album_year not in ['', None]:
            album_year = int(album_year)
        db_req(query_insert_new_album(album_title, album_year, album_info))
        album_data = db_req(query_album_info_by_title(album_title))
    return album_data[0]['id_album']


###########################################
#                  SONG                   #
###########################################

def get_last_song_id():
    return """
    SELECT song.id_song
    FROM song
    ORDER BY
        song.id_song DESC
        LIMIT 1;"""


def query_songs_not_in_albums(id_artist):
    return f'''
    SELECT DISTINCT artist.id_artist, artist.artist_name, song.id_song, song.song_title, song.song_year
    FROM rel_table 
    INNER JOIN artist, song
    ON rel_table.id_artist = artist.id_artist
    AND rel_table.id_song = song.id_song
    WHERE artist.id_artist = "{id_artist}"
    AND rel_table.id_album is NULL
    ORDER BY song.song_year;'''


def query_album_songs(id_artist, id_album):
    return f'''
    SELECT artist.id_artist, album.id_album, song.id_song, song.song_title, song.song_year, rel_table.track_number 
    FROM rel_table 
    INNER JOIN artist, album, song
    ON rel_table.id_artist = artist.id_artist
    AND rel_table.id_album = album.id_album
    AND rel_table.id_song = song.id_song
    WHERE artist.id_artist = "{id_artist}"
    AND album.id_album = "{id_album}"
    ORDER BY song.song_year;'''


def query_song_data_by_id(id_artist, id_song):
    return f'''
    SELECT DISTINCT song.id_song, song.song_title, song.song_year, song.song_text, song.origin_lang
    FROM rel_table 
    INNER JOIN artist, song
    ON rel_table.id_artist = artist.id_artist
    AND rel_table.id_song = song.id_song
    WHERE artist.id_artist = "{id_artist}"
    AND song.id_song = "{id_song}"'''


def query_song_data_by_title(song_title):
    return f'''
    SELECT song.id_song, song.song_title, song.song_year, song.song_text  
    FROM song
    WHERE song.song_title = "{song_title}"'''


def query_search_all_songs_by_like(search_text):
    return f"""
    SELECT DISTINCT rel_table.id_artist, rel_table.id_album, song.id_song, song.song_title
    FROM rel_table
    INNER JOIN song
    ON rel_table.id_song = song.id_song
    WHERE song.song_title like '%{search_text}%';"""


def query_insert_new_song(*args):
    """
    where -> (song_title, song_year, song_text, origin_lang)
    what  -> (new_song_title, int(new_song_year), new_song_text, new_origin_lang)
    """
    return f"""
    INSERT INTO song (song_title, song_year, song_text, origin_lang)
    VALUES {args}"""


def query_update_song_text(id_song, new_song_text):
    """
    (id_song, new_song_text)
    """
    return f"""
    UPDATE song
    SET song_text = "{new_song_text}"
    WHERE song.id_song = "{id_song}";"""


def query_delete_song_from_songs_table(id_song):
    return f"""
    DELETE 
    FROM song
    WHERE song.id_song = {id_song};"""


def fn_insert_song(song_title, song_text, song_year: int, song_lang):
    song_data = db_req(query_song_data_by_title(song_title))
    if len(song_data) < 1:
        if not isinstance(song_year, int) and song_year not in ['', None]:
            song_year = int(song_year)
        db_req(query_insert_new_song(song_title, song_year, song_text, song_lang))
        song_data = db_req(query_song_data_by_title(song_title))
    return song_data[0]['id_song']


###########################################
#               TRACK LIST                #
###########################################

def query_track_list(id_artist, id_song, id_album, track_number):
    return f"""
    SELECT id_artist, id_song, id_album
    from rel_table
    WHERE id_artist={id_artist}
    AND id_song={id_song}
    AND id_album={id_album}
    AND track_number={track_number}""".replace('None', 'NULL')


def query_insert_new_track_list(*args):
    # where -> (id_artist, id_song, id_album, track_number)
    # what  -> (new_artist_id, new_song_id, new_album_id, new_song_track_number)
    return f"""
    INSERT INTO rel_table (id_artist, id_song, id_album, track_number)
    VALUES {args}""".replace('None', 'NULL')


def query_delete_song_track_list(id_artist, id_song):
    return f"""
    DELETE 
    FROM rel_table
    WHERE rel_table.id_artist = {id_artist}
    AND rel_table.id_song = {id_song};"""


def fn_insert_to_tracklist(id_artist: int, id_song: int, id_album, track_number):
    tracklist_data = db_req(query_track_list(id_artist, id_song, id_album, track_number))
    if len(tracklist_data) < 1:
        db_req(query_insert_new_track_list(id_artist, id_song, id_album, track_number))


def fn_add_song(data):
    if data['song_info']['song_title'] not in ['', None]:
        song_id = fn_insert_song(song_title=data['song_info']['song_title'],
                                 song_text=data['song_info']['song_text'],
                                 song_year=int(data['song_info']['song_year']),
                                 song_lang=data['song_info']['song_lang'])
        if len(data['artist_info']) > 0:
            for artist_data in data['artist_info']:
                if artist_data['artist_name'] not in ['', None]:
                    artist_id = fn_insert_artist(artist_name=artist_data['artist_name'],
                                                 artist_info=artist_data['artist_info'])
                    if len(artist_data['album_info']) > 0:
                        for album_data in artist_data['album_info']:
                            if album_data['album_title'] not in ['', None]:
                                album_id = fn_insert_album(album_title=album_data['album_title'],
                                                           album_year=album_data['album_year'],
                                                           album_info=album_data['album_info'])
                                fn_insert_to_tracklist(id_artist=int(artist_id),
                                                       id_song=int(song_id),
                                                       id_album=int(album_id),
                                                       track_number=int(album_data['track_number']))
                            else:
                                fn_insert_to_tracklist(id_artist=artist_id, id_song=song_id,
                                                       id_album=None,
                                                       track_number=None)
                    else:
                        fn_insert_to_tracklist(id_artist=artist_id, id_song=song_id, id_album=None, track_number=None)


def fn_delete_song(id_artist, id_song):
    db_req(query_delete_song_track_list(id_artist, id_song))
    db_req(query_delete_song_from_songs_table(id_song))
