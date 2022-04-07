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
    return """
    SELECT artist.id_artist
    FROM artist
    ORDER BY
        artist.id_artist DESC
        LIMIT 1;"""


def query_all_artists():
    return '''
    SELECT DISTINCT artist.id_artist, artist.artist_name
    FROM rel_table 
    INNER JOIN artist
    ON rel_table.id_artist = artist.id_artist
    ORDER BY artist_name;'''


def query_artist_by_id(id_artist):
    return f'''
    SELECT artist.id_artist, artist.artist_name, artist.artist_info
    FROM artist
    WHERE artist.id_artist = "{id_artist}"'''


def query_artist_by_name(artist_name):
    return f'''
    SELECT artist.id_artist, artist.artist_name, artist.artist_info
    FROM artist
    WHERE artist.artist_name = "{artist_name}"'''


def query_search_all_artists_by_like(search_text):
    return f"""
    SELECT id_artist, artist_name
    FROM artist
    WHERE artist.artist_name like '%{search_text}%';"""


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


def query_search_all_albums_by_like(search_text):
    return f"""
    SELECT DISTINCT rel_table.id_artist, album.id_album, album.album_title
    FROM rel_table
    INNER JOIN album
    ON rel_table.id_album = album.id_album
    WHERE album.album_title like '%{search_text}%';"""


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
    SELECT DISTINCT song.id_song, song.song_title, song.song_year, song.song_text  
    FROM song
    WHERE song.song_title = "{song_title}"'''


def query_search_all_songs_by_like(search_text):
    return f"""
    SELECT DISTINCT rel_table.id_artist, rel_table.id_album, song.id_song, song.song_title
    FROM rel_table
    INNER JOIN song
    ON rel_table.id_song = song.id_song
    WHERE song.song_title like '%{search_text}%';"""
