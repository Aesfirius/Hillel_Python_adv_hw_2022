
def template(body):
    return f"""
    <html><body>
    <h2>Hillel HW Lesson 5</h2>
    <br>
    <br>
    {body}
    <br>
    <br>
    </body></html>"""


def home_page_body(db_resp):
    artists_list = ''.join([f'<li><a href="/artist/{artist["id_artist"]}/">{artist["artist_name"]}</a></li>'
                            for artist in db_resp])
    style_p_div = 'style="position: relative; height: 10;"'
    style_label = 'style="position: absolute; left: 0;"'
    style_input = 'style="position: absolute; left: 200;"'
    return f'''
    <br>
    <br>
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


def artist_page_body(data_artist, data_albums, data_x_songs):
    id_artist = data_artist[0]['id_artist']
    albums_list = ''.join([f'<li><a href="/artist/{id_artist}/album/{album["id_album"]}/">{album["album_title"]}</a></li>'
                           for album in data_albums] if len(data_albums) > 0 else '')
    x_songs_list = ''.join([f'<li><a href="/artist/{id_artist}/song/{song["id_song"]}/?id_album=0">{song["song_title"]}</a></li>'
                            for song in data_x_songs] if len(data_x_songs) > 0 else '')
    return f'''
    <h3>Artist: {data_artist[0]['artist_name']}</h3>
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
    <a href="/">Back ==>> Home</a>
    <br>'''


def album_page_body(data_artist, data_album, data_songs):
    songs_list = ''.join([f'<li><a href="/artist/{data_artist[0]["id_artist"]}/song/{song["id_song"]}/'
                          f'?id_album={data_album[0]["id_album"]}">{song["track_number"]}. {song["song_title"]}</a></li>'
                          for song in data_songs] if len(data_songs) > 0 else '')
    return f"""
    <h3>Artist: {data_artist[0]['artist_name']}</h3>
    <br>
    <h3>Album: <b>"{data_album[0]['album_title']}"</b> released on {data_album[0]['album_year']}</h3>
    <br>
    <h4>INFO:</h4>
    <p>{data_album[0]['album_info']}</p>
    <br>
    <br>
    <h4>SONGS</h4>
    <ul>{songs_list}</ul>
    <br>
    <br>
    <a href="/artist/{data_artist[0]['id_artist']}/">Back ==>> Artist albums</a>
    <br>
    <br>
    <a href="/">Back ==>> Home</a>
    <br>"""


def song_page_body(data_artist, data_album, data_song, translated_text):
    id_artist = data_artist[0]['id_artist']
    song_text = data_song[0]['song_text'].replace('\n', '<br>')
    back_to_albums = f"<a href='/artist/{id_artist}/album/{data_album[0]['id_album']}/'>Back ==>> Album songs</a>" \
        if data_album is not None else ''

    style_p_div = 'style="position: relative; height: 10;"'
    style_label = 'style="position: absolute; left: 0;"'
    style_input = 'style="position: absolute; left: 200;"'
    confirm_del = '<script> ' \
                  'function myFunction() { ' \
                  'if (confirm("Are you sure you want to delete song") == true) { ' \
                  'window.open("%s", name="_parent");}' \
                  'else {' \
                  'window.open(".", name="_parent");}' \
                  ';}' \
                  '</script>'

    translate_form = f"""
    <form action="." method="get" id="translate">
        <div {style_p_div}>
            <div {style_label}>
               <label for="translate">Translate to ...</label>
            </div>
            <div {style_input}>
                <input type="hidden" name="id_album" value="{data_album[0]['id_album'] if data_album is not None else ''}">
                <input type="text" id="translate" name="translate">
            </div>
        </div>
    </form>
    <button style="width: 380px;" type="submit" form="translate" value="Translate">Translate</button>"""

    return f"""
    <h3>Artist: {data_artist[0]['artist_name']}</h3>
    <br>
    <h3>Song: <b>"{data_song[0]['song_title']}"</b> released in {data_song[0]['song_year']}</h3>
    <br>
    <br>
    {translate_form}
    <br>
    <br>
    <h3>Lyrics</h3>
    <br>
        <table style="width:100%">
        <tr>
            <td><b>Origin language text</b></td>
            <td><b>{"Translated text" if translated_text is not None else ""}</b></td>
        </tr>
        <tr>
            <td style="width:40%">{song_text}</td>
            <td style="width:40%">{translated_text if translated_text is not None else ""}</td>
        </tr>
    </table>
    <p>{song_text}</p>
    <br>
    <br>
    {translate_form}
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
    {confirm_del % f"/artist/delete_song/?id_artist={id_artist}&id_song={data_song[0]['id_song']}"}
    <br>
    <br>
    {back_to_albums}
    <br>
    <br>
    <a href="/artist/{id_artist}/">Back ==>> Artist albums</a>
    <br>
    <br>
    <a href="/">Back ==>> Home</a>
    <br>
    """


def song_page_body_new_success(artist_name, song_title):
    return f"""
    <h3>Song "{song_title}" of artist "{artist_name}" ==>> CREATED</h3>
    <br>
    <br>
    <a href="/">Back ==>> Home</a>
    <br>"""


def song_page_body_update_text(data_artist, data_song):
    id_artist = data_artist[0]['id_artist']
    return f"""
    <h3>Song "{data_song[0]['song_title']}" of artist "{data_artist[0]['artist_name']}" ==>> Lyrics UPDATED</h3>
    <br>
    <br>
    <a href="/artist/{id_artist}/song/{data_song[0]['id_song']}/">Back ==>> Song</a>
    <br>
    <br>
    <a href="/artist/{id_artist}/">Back ==>> Artist albums</a>
    <br>
    <br>
    <a href="/">Back ==>> Home</a>
    <br>"""


def song_page_body_deleted(data_artist, data_song):
    return f"""
    <h3>Song "{data_song[0]['song_title']}" of artist "{data_artist[0]['artist_name']}" ==>> DELETED</h3>
    <br>
    <br>
    <a href="/artist/{data_artist[0]['id_artist']}/">Back ==>> Artist albums</a>
    <br>
    <br>
    <a href="/">Back ==>> Home</a>
    <br>"""


def search_page_body(search_text, artists_data, albums_data, songs_data):
    """
    Artists            Albums              Songs


    """
    artists_list = ''.join([f'<li><a href="/artist/{artist["id_artist"]}/">{artist["artist_name"]}</a></li>'
                            for artist in artists_data] if len(artists_data) > 0 else '')
    albums_list = ''.join([f'<li><a href="/artist/{album["id_artist"]}/album/{album["id_album"]}/">{album["album_title"]}</a></li>'
                           for album in albums_data] if len(albums_data) > 0 else '')
    songs_list = ''.join([f'<li><a href="/artist/{song["id_artist"]}/song/{song["id_song"]}/?id_album={song["id_album"]}">{song["song_title"]}</a></li>'
                          for song in songs_data] if len(songs_data) > 0 else '')

    return f"""
    <h3>You searching: <b>{search_text}</b></h3>
    <br>
    <br>
    <br>
    <table style="width:100%">
        <tr>
            <td><b>Artists</b></td>
            <td><b>Albums</b></td>
            <td><b>Songs</b></td>
        </tr>
        <tr>
            <td>{artists_list}</td>
            <td>{albums_list}</td>
            <td>{songs_list}</td>
        </tr>
    </table>
    <br>
    <br>
    <a href="/">Back ==>> Home</a>
    <br>"""


def search_page_body_empty():
    return f"""
    <br>
    <br>
    <br>
    <h2>Go Back and take a cup of coffee</h2>
    <br>
    <br>
    <a href="/">Back ==>> Home</a>
    <br>"""
