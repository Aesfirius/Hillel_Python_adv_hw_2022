import os
import json
from flask import Flask, request, render_template

from l8_hw.db_queries import *
from l8_hw.helpers import translate_to

"""
/
/artist/<artist>
/artist/<artist>/album/<album>
/artist/<artist>/song/<song>
/search
"""

app = Flask(__name__, static_url_path='', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.environ.get("DB_NAME")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)


@app.route('/add/', methods=['PUT'])
@app.route('/', methods=['GET', 'PUT'])
def home():
    if request.method == "PUT":
        data = json.loads(request.json)
        fn_add__song(data)

    return render_template('home.html',
                           artists_list=get__all_artists())


@app.route('/search/')
def search():
    search_text = request.args.get('search_text')
    if search_text != '':
        artists_data = get__search_all_artists__by_like(search_text)
        albums_data = get__search_all_albums__by_like(search_text)
        songs_data = get__search_all_songs__by_like(search_text)
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
        data_artist = get__artist__by_id(id_artist)
        data_albums = get__all_artist_albums(id_artist)
        data_x_songs = get__all_songs_not_in_album(id_artist)

        return render_template('artist.html',
                               data_artist=data_artist,
                               data_albums=data_albums,
                               data_x_songs=data_x_songs)

    elif request.method == 'DELETE':
        id_song = request.json.get('id_song')
        id_album = request.json.get('id_album')
        fn_delete__song(id_artist, id_song, id_album)

        data_artist = get__artist__by_id(id_artist)
        data_albums = get__all_artist_albums(id_artist)
        data_x_songs = get__all_songs_not_in_album(id_artist)
        return render_template('artist.html',
                               data_artist=data_artist,
                               data_albums=data_albums,
                               data_x_songs=data_x_songs)


@app.route('/artist/<id_artist>/album/<id_album>/', methods=['GET'])
def album(id_artist, id_album):
    if request.method == 'GET':
        data_artist = get__artist__by_id(id_artist)
        data_album = get__album__by_id(id_album)
        data_songs = get__all_album_songs(id_artist, id_album)

        return render_template('album.html',
                               data_artist=data_artist,
                               data_album=data_album,
                               data_songs=data_songs)


@app.route('/artist/<id_artist>/song/<id_song>/', methods=['GET', 'POST'])
def song(id_artist, id_song):
    if request.method == 'GET':
        id_album = request.args.to_dict().get('id_album')
        translate = request.args.to_dict().get('translate')
        data_artist = get__artist__by_id(id_artist)
        data_album = get__album__by_id(id_album)
        data_song = get__song_track__by_id(id_artist, id_song)
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

        update__song_text(id_song, new_text)

        data_artist = get__artist__by_id(id_artist)
        data_album = get__album__by_id(id_album)
        data_song = get__song_track__by_id(id_artist, id_song)
        return render_template('song.html',
                               data_artist=data_artist,
                               data_album=data_album,
                               data_song=data_song,
                               translated_text=None)


if __name__ == '__main__':
    app.run(debug=True)
