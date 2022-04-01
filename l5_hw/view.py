
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


def artist_page_body(data_artist, data_albums, data_x_songs):
    id_artist = data_artist[0]['id_artist']
    albums_list = ''.join([f'<li><a href="/artist/{id_artist}/album/{album["id_album"]}/">{album["album_title"]}</a></li>' for album in data_albums] if len(data_albums) > 0 else '')
    x_songs_list = ''.join([f'<li><a href="/artist/{id_artist}/song/{song["id_song"]}/">{song["song_title"]}</a></li>' for song in data_x_songs] if len(data_x_songs) > 0 else '')
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
    songs_list = ''.join([f'<li><a href="/artist/{data_artist[0]["id_artist"]}/song/{song["id_song"]}/">{song["track_number"]}. {song["song_title"]}</a></li>' for song in data_songs] if len(data_songs) > 0 else '')
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


def song_page_body(data_artist, data_album, data_song):
    id_artist = data_artist[0]['id_artist']
    song_text = data_song[0]['song_text'].replace('\n', '<br>')

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
    return f"""
    <h3>Artist: {data_artist[0]['artist_name']}</h3>
    <br>
    <h3>Song: <b>"{data_song[0]['song_title']}"</b> released in {data_song[0]['song_year']}</h3>
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
    {confirm_del % f"/artist/delete_song/?id_artist={id_artist}&id_song={data_song[0]['id_song']}"}
    <br>
    <br>
    <a href="/artist/{id_artist}/album/{data_album[0]['id_album']}/">Back ==>> Album songs</a>
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


def search_page_body(search_text):
    return f"""
    <h3>You searching:</h3>
    <br>
    <h3><b>{search_text}</b></h3>
    <br>
    <a href="/">Back ==>> Home</a>
    <br>"""
