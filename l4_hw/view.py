import urllib.parse
from l4_hw.helpers import f_from_url, f_for_url


def template(body):
    return f'''
    <html><body>
    <h2>Hillel HW Lesson 4</h2>
    <br>
    <br>
    {body}
    <br>
    <br>
    </body></html>'''


def home_page_body(db_resp):
    artists_list = ''.join([f'<li><a href="/artist/{f_for_url(urllib.parse.quote_plus(artist["artist_name"]))}/">{artist["artist_name"]}</a></li>' for artist in db_resp])
    style_p_div = 'style="position: relative; height: 10;"'
    style_label = 'style="position: absolute; left: 0;"'
    style_input = 'style="position: absolute; left: 200;"'
    return f'''
    <br>
    <p>Simulate Search<p>
    <form id="form_search" action="search" method="GET">Enter your search text here...
    <input type="text" name="search_text"/>
    <button style="width: 100px;"type="submit" form="form_search" value="Submit">Search</button>

    </form>
    <br>
    <p>All artists</p>
    <ul>
    {artists_list}
    </ul>
    <br>
    <p>Add New song data</p>
    <form action="/artist/new_song/" method="put" id="form_add">
    <h3>Artist:</h3>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_artist_name">Artist name:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_artist_name" name="new_artist_name">
        </div>
    </div>
    <br>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_artist_info">Artist info:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_artist_info" name="new_artist_info">
        </div>
    </div>
   <br>
    <h3>Album:</h3>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_album_title">Album title:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_album_title" name="new_album_title">
        </div>
    </div>
    <br>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_album_year">Album year:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_album_year" name="new_album_year">
        </div>
    </div>
    <br>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_album_info">Album info:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_album_info" name="new_album_info">
        </div>
    </div>
    <br>
    <h3>Song:</h3>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_song_title">Song title:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_song_title" name="new_song_title">
        </div>
    </div>
    <br>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_song_year">Song year:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_song_year" name="new_song_year">
        </div>
    </div>
    <br>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_song_text">Song text:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_song_text" name="new_song_text">
        </div>
    </div>
    <br>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_song_track_number">Song number in album:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_song_track_number" name="new_song_track_number">
        </div>
    </div>
    <br>
    <div {style_p_div}>
        <div {style_label}>
            <label for="new_song_lang">Song language:</label>
        </div>
        <div {style_input}>
            <input type="text" id="new_song_lang" name="new_song_lang">
        </div>
    </div>
    <br>
    </form>
    <button style="width: 380px;" type="submit" form="form_add" value="Submit">ADD</button>
    <br>
    '''


def artist_page_body(artist_name, data_artist, data_albums, data_x_songs):
    n_artist_name = f_from_url(urllib.parse.unquote_plus(artist_name))
    albums_list = ''.join([f'<li><a href="/artist/{artist_name}/album/{f_for_url(urllib.parse.quote_plus(album["album_title"]))}/">{album["album_title"]}</a></li>' for album in data_albums] if len(data_albums) > 0 else '')
    x_songs_list = ''.join([f'<li><a href="/artist/{artist_name}/song/{f_for_url(urllib.parse.quote_plus(song["song_title"]))}/">{song["song_title"]}</a></li>' for song in data_x_songs] if len(data_x_songs) > 0 else '')
    return f'''
    <h3>Artist: {n_artist_name}</h3>
    <br>
    <h4>INFO:</h4>
    <p>{data_artist[0]['artist_info']}</p>
    <br>
    <br>
    <h4>ALL ALBUMS</h4>
    <ul>{albums_list}</ul>
    <br>
    <br>
    <h4>SONGS NOT IN ALBUMS</h4>
    <ul>{x_songs_list}</ul>
    <br>
    <br>
    <a href="/">Back --> Home</a>
    <br>'''


def album_page_body(artist_name, album_title, data_album, data_songs):
    n_artist_name = f_from_url(urllib.parse.unquote_plus(artist_name))
    n_album_title = f_from_url(urllib.parse.unquote_plus(album_title))
    songs_list = ''.join([f'<li><a href="/artist/{artist_name}/song/{f_for_url(urllib.parse.quote_plus(song["song_title"]))}/">{song["track_number"]}. {song["song_title"]}</a></li>' for song in data_songs] if len(data_songs) > 0 else '')

    return f"""
    <h3>Artist: {n_artist_name}</h3>
    <br>
    <h3>Album: <b>"{n_album_title}"</b> released in {data_album[0]['album_year']}</h3>
    <br>
    <h4>INFO:</h4>
    <p>{data_album[0]['album_info']}</p>
    <br>
    <br>
    <h4>SONGS</h4>
    <ul>{songs_list}</ul>
    <br>
    <br>
    <a href="/artist/{artist_name}/">Back --> Artist albums</a>
    <br>
    <br>
    <a href="/">Back --> Home</a>
    <br>"""


def song_page_body(artist_name, album, song_title, data_song, song_text):
    n_artist_name = f_from_url(urllib.parse.unquote_plus(artist_name))
    n_song_title = f_from_url(urllib.parse.unquote_plus(song_title))

    style_p_div = 'style="position: relative; height: 10;"'
    style_label = 'style="position: absolute; left: 0;"'
    style_input = 'style="position: absolute; left: 200;"'
    conf_del = '<script> ' \
               'function myFunction() { ' \
               'if (confirm("Are you sure you want to delete song") == true) { ' \
               'window.open("%s", name="_parent");}' \
               'else {' \
               'window.open(".", name="_parent");}' \
               ';}' \
               '</script>'
    return f"""
    <h3>Artist: {n_artist_name}</h3>
    <br>
    <h3>Song: <b>"{n_song_title}"</b> released in {data_song[0]['song_year']}</h3>
    <br>
    <h3>Lyrics</h3>
    <br>
    <p>{song_text}</p>
    <br>
    <br>
    <form action="/artist/update_song" method="post" id="form_update">
        <div {style_p_div}>
            <div {style_label}>
               <label for="new_song_text">Update Song text:</label>
            </div>
            <div {style_input}>
                <input type="text" id="new_song_text" name="new_song_text">
            </div>
        </div>
    </form>
    <button style="width: 380px;" type="submit" form="form_update" value="Submit">Update</button>
    <br>
    <br>    
    <button style="width: 380px;" type="submit" value="Delete" onclick="myFunction()">Delete</button>
    {conf_del % f"/artist/delete_song/?artist_name={artist_name}&song_title={song_title}"}
    <br>
    <br>
    <a href="/artist/{artist_name}/album/{album}/">Back --> Album songs</a>
    <br>
    <br>
    <a href="/artist/{artist_name}/">Back --> Artist albums</a>
    <br>
    <br>
    <a href="/">Back --> Home</a>
    <br>
    """


def song_page_body_deleted(artist_name, song_title):
    u_artist_name = f_for_url(urllib.parse.quote_plus(artist_name))
    return f"""
    <h3>Song "{song_title}" of artist "{artist_name}" ==>> DELETED</h3>
    <br>
    <br>
    <a href="/artist/{u_artist_name}/">Back --> Artist albums</a>
    <br>
    <br>
    <a href="/">Back --> Home</a>
    <br>"""
