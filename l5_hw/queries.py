

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


def query_insert_new_artist(*args):
    # where -> (artist_name, artist_info)
    # what  -> (new_artist_name, new_artist_info)
    return f"""
    INSERT INTO artist (artist_name, artist_info)
    VALUES {args}"""


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


def query_insert_new_album(*args):
    # where -> (album_title, album_year, album_info)
    # what  -> (new_album_title, int(new_album_year), new_album_info)
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


def query_song_data_by_title(id_artist, song_title):
    return f'''
    SELECT DISTINCT song.id_song, song.song_title, song.song_year, song.song_text  
    FROM rel_table 
    INNER JOIN artist, song
    ON rel_table.id_artist = artist.id_artist
    AND rel_table.id_song = song.id_song
    WHERE artist.id_artist = "{id_artist}"
    AND song.song_title = "{song_title}"'''


def query_insert_new_song(*args):
    # where -> (song_title, song_year, song_text, origin_lang)
    # what  -> (new_song_title, int(new_song_year), new_song_text, new_origin_lang)
    return f"""
    INSERT INTO song (song_title, song_year, song_text, origin_lang)
    VALUES {args}"""


def query_update_song_text(*args):
    # (id_song, new_song_text)
    return f"""
    UPDATE song
    SET song_text = "{args[1]}"
    WHERE song.id_song = "{args[0]}";"""


def query_delete_song_from_songs_table(id_song):
    return f"""
    DELETE 
    FROM song
    WHERE song.id_song = {id_song};"""


def query_search_all_songs_by_like(search_text):
    return f"""
    SELECT DISTINCT rel_table.id_artist, rel_table.id_album, song.id_song, song.song_title
    FROM rel_table
    INNER JOIN song
    ON rel_table.id_song = song.id_song
    WHERE song.song_title like '%{search_text}%';"""


###########################################
#               TRACK LIST                #
###########################################

def query_insert_new_track_list(track_list_params):
    # where -> (id_artist, id_song, id_album, track_number)
    # what  -> (new_artist_id, new_song_id, new_album_id, new_song_track_number)
    return f"""
    INSERT INTO rel_table {tuple(track_list_params.keys())}
    VALUES {tuple(track_list_params.values())}"""


def query_delete_song_track_list(id_artist, id_song):
    return f"""
    DELETE 
    FROM rel_table
    WHERE rel_table.id_artist = {id_artist}
    AND rel_table.id_song = {id_song};"""
