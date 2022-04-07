from flask import Flask, request

from l6_hw.view import *
from l6_hw.queries import *
from l6_hw.helpers import translate_to

"""
/
/artist/<artist>
/artist/<artist>/album/<album>
/artist/<artist>/song/<song>
/search
"""

app = Flask(__name__, static_url_path='', template_folder='templates')


@app.route('/', methods=['GET'])
def home():
    db_resp = db_req(query_all_artists())
    return template(home_page_body(db_resp))


@app.route('/search/')
def search():
    search_text = request.args.get('search_text')
    if search_text == '':
        return template(search_page_body_empty())
    else:
        artists_data = db_req(query_search_all_artists_by_like(search_text))
        albums_data = db_req(query_search_all_albums_by_like(search_text))
        songs_data = db_req(query_search_all_songs_by_like(search_text))
        return template(search_page_body(search_text, artists_data, albums_data, songs_data))


@app.route('/artist/<id_artist>/')
def artist(id_artist):
    data_artist = db_req(query_artist_by_id(id_artist))
    data_albums = db_req(query_all_albums(id_artist))
    data_x_songs = db_req(query_songs_not_in_albums(id_artist))

    return template(artist_page_body(data_artist, data_albums, data_x_songs))


@app.route('/artist/<id_artist>/album/<id_album>/')
def album(id_artist, id_album):
    data_artist = db_req(query_artist_by_id(id_artist))
    data_album = db_req(query_album_info(id_album))
    data_songs = db_req(query_album_songs(id_artist, id_album))

    return template(album_page_body(data_artist, data_album, data_songs))


@app.route('/artist/<id_artist>/song/<id_song>/')
def song(id_artist, id_song):
    id_album = request.args.get('id_album')
    translate = request.args.get('translate')
    data_artist = db_req(query_artist_by_id(id_artist))
    data_album = db_req(query_album_info(id_album)) if id_album not in [0, '0', '', 'None', None] else None
    data_song = db_req(query_song_data_by_id(id_artist, id_song))

    if translate is not None:
        translated_text = translate_to(origin_text=data_song[0]['song_text'], from_lang=data_song[0]['origin_lang'],
                                       to_lang=translate)
    else:
        translated_text = translate

    return template(song_page_body(data_artist, data_album, data_song, translated_text=translated_text))


if __name__ == '__main__':
    app.run(debug=True)
