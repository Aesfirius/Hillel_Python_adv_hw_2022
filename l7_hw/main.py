import json
from flask import Flask, request, render_template

from l7_hw.forms import *
from l7_hw.view import *
from l7_hw.queries import *
from l7_hw.helpers import translate_to

"""
/
/artist/<artist>
/artist/<artist>/album/<album>
/artist/<artist>/song/<song>
/search
"""

app = Flask(__name__, static_url_path='', template_folder='templates')


@app.route('/add/', methods=['PUT'])  # для задания, но у меня реализовано через главную страницу.
@app.route('/', methods=['GET', 'PUT'])
def home():
    if request.method == "PUT":
        data = json.loads(request.json)
        fn_add_song(data)

    db_resp = db_req(query_all_artists())
    return render_template('home.html',
                           artists_list=db_resp)


@app.route('/search/')
def search():
    search_text = request.args.get('search_text')
    if search_text != '':
        artists_data = db_req(query_search_all_artists_by_like(search_text))
        albums_data = db_req(query_search_all_albums_by_like(search_text))
        songs_data = db_req(query_search_all_songs_by_like(search_text))
    else:
        artists_data = albums_data = songs_data = []

    return render_template('search.html',
                           search_text=search_text,
                           artists_data=artists_data,
                           albums_data=albums_data,
                           songs_data=songs_data)


@app.route('/artist/<id_artist>/', methods=['GET', 'DELETE'])
def artist(id_artist):
    if request.method == 'GET':
        data_artist = db_req(query_artist_by_id(id_artist))
        data_albums = db_req(query_all_albums(id_artist))
        data_x_songs = db_req(query_songs_not_in_albums(id_artist))

        return render_template('artist.html',
                               data_artist=data_artist[0],
                               data_albums=data_albums,
                               data_x_songs=data_x_songs)

    elif request.method == 'DELETE':
        id_song = request.json.get('id_song')

        fn_delete_song(id_artist, id_song)

        data_artist = db_req(query_artist_by_id(id_artist))
        data_albums = db_req(query_all_albums(id_artist))
        data_x_songs = db_req(query_songs_not_in_albums(id_artist))
        return render_template('artist.html',
                               data_artist=data_artist[0],
                               data_albums=data_albums,
                               data_x_songs=data_x_songs)


@app.route('/artist/<id_artist>/album/<id_album>/', methods=['GET'])
def album(id_artist, id_album):
    if request.method == 'GET':
        data_artist = db_req(query_artist_by_id(id_artist))
        data_album = db_req(query_album_info(id_album))
        data_songs = db_req(query_album_songs(id_artist, id_album))

        return render_template('album.html',
                               data_artist=data_artist[0],
                               data_album=data_album[0],
                               data_songs=data_songs)


@app.route('/artist/<id_artist>/song/<id_song>/', methods=['GET', 'POST'])
def song(id_artist, id_song):
    if request.method == 'GET':
        id_album = request.args.to_dict().get('id_album')
        translate = request.args.to_dict().get('translate')
        data_artist = db_req(query_artist_by_id(id_artist))[0]
        data_album = db_req(query_album_info(id_album))[0] if id_album not in [0, '0', '', 'None', None] else None
        data_song = db_req(query_song_data_by_id(id_artist, id_song))[0]
        if translate not in ['', 'None', None]:
            translated_text = translate_to(origin_text=data_song['song_text'],
                                           from_lang=data_song['origin_lang'],
                                           to_lang=translate)
        else:
            translated_text = None
        return render_template('song.html',
                               data_artist=data_artist,
                               data_album=data_album,
                               data_song=data_song,
                               translated_text=translated_text)

    elif request.method == 'POST':
        id_album = request.form.to_dict().get('id_album')
        new_text = request.form.to_dict().get('new_song_text')

        db_req(query_update_song_text(id_song, new_text))

        data_artist = db_req(query_artist_by_id(id_artist))[0]
        data_album = db_req(query_album_info(id_album))[0] if id_album not in [0, '0', '', 'None', None] else None
        data_song = db_req(query_song_data_by_id(id_artist, id_song))[0]
        return render_template('song.html',
                               data_artist=data_artist,
                               data_album=data_album,
                               data_song=data_song,
                               translated_text=None)


if __name__ == '__main__':
    app.run(debug=True)
