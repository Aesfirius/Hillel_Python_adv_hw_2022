

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


def query_insert_new_song():
    pass
