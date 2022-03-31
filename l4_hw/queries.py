

def get_last_inserted_row_id():
    return "select last_insert_rowid()"


def get_last_song_id():
    return """
    SELECT song.id_song
    FROM song
    ORDER BY
        song.id_song DESC
        LIMIT 1;"""


def get_last_album_id():
    return """
    SELECT album.id_album
    FROM album
    ORDER BY
        album.id_album DESC
        LIMIT 1;"""


def get_last_artist_id():
    return """
    SELECT artist.id_artist
    FROM artist
    ORDER BY
        artist.id_artist DESC
        LIMIT 1;"""


def query_artists():
    return '''
    SELECT DISTINCT artist.id_artist, artist.artist_name
    FROM rel_table 
    INNER JOIN artist
    ON rel_table.id_artist = artist.id_artist
    ORDER BY artist_name;'''


def query_artist(n_artist_name):
    return f'''
    SELECT artist.artist_name, artist.artist_info
    FROM artist
    WHERE artist.artist_name = "{n_artist_name}"'''


def query_albums(n_artist_name):
    return f'''
    SELECT DISTINCT album.id_album, artist.artist_name, album.album_title, album.album_year
    FROM rel_table
    INNER JOIN artist, album
    ON rel_table.id_artist = artist.id_artist
    AND rel_table.id_album = album.id_album
    WHERE artist.artist_name = "{n_artist_name}"
    ORDER BY album.album_year;'''


def query_songs_not_in_albums(n_artist_name):
    return f'''
    SELECT DISTINCT artist.artist_name, song.song_title, song.song_year
    FROM rel_table 
    INNER JOIN artist, song
    ON rel_table.id_artist = artist.id_artist
    AND rel_table.id_song = song.id_song
    WHERE artist.artist_name = "{n_artist_name}"
    AND rel_table.id_album is NULL
    ORDER BY song.song_year;'''


def query_album_info(n_album_title):
    return f'''
    SELECT album.album_title, album.album_year, album.album_info
    FROM album 
    WHERE album.album_title = "{n_album_title}"'''


def query_album_songs(n_artist_name, n_album_title):
    return f'''
    SELECT song.song_title, song.song_year, rel_table.track_number 
    FROM rel_table 
    INNER JOIN artist, album, song
    ON rel_table.id_artist = artist.id_artist
    AND rel_table.id_album = album.id_album
    AND rel_table.id_song = song.id_song
    WHERE artist.artist_name = "{n_artist_name}"
    AND album.album_title = "{n_album_title}"
    ORDER BY song.song_year;'''


def query_song_data(n_artist_name, n_song_title):
    return f'''
    SELECT DISTINCT song.song_title, song.song_year, song.song_text  
    FROM rel_table 
    INNER JOIN artist, song
    ON rel_table.id_artist = artist.id_artist
    AND rel_table.id_song = song.id_song
    WHERE artist.artist_name = "{n_artist_name}"
    AND song.song_title = "{n_song_title}"'''


def query_insert_new_song(*args):
    # where -> (song_title, song_year, song_text, origin_lang)
    # what  -> (new_song_title, int(new_song_year), new_song_text, new_origin_lang)
    return f"""
    INSERT INTO song (song_title, song_year, song_text, origin_lang)
    VALUES {args}"""


def query_insert_new_album(*args):
    # where -> (album_title, album_year, album_info)
    # what  -> (new_album_title, int(new_album_year), new_album_info)
    return f"""
    INSERT INTO album (album_title, album_year, album_info)
    VALUES {args}"""


def query_insert_new_artist(*args):
    # where -> (artist_name, artist_info)
    # what  -> (new_artist_name, new_artist_info)
    return f"""
    INSERT INTO artist (artist_name, artist_info)
    VALUES {args}"""


def query_insert_new_track_list(*args):
    # where -> (id_artist, id_song, id_album, track_number)
    # what  -> (new_artist_id, new_song_id, new_album_id, new_song_track_number)
    return f"""
    INSERT INTO rel_table (id_artist, id_song, id_album, track_number)
    VALUES {args}"""


def query_update_song_text(*args):
    # (song_title, new_song_text)
    return f"""
    UPDATE song
    SET song_text = "{args[1]}"
    WHERE song.song_title = "{args[0]}";"""
