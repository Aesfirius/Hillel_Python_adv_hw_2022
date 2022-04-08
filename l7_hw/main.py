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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = json.loads(request.form['add_song_form'])
        query_add_song(data)
    db_resp = db_req(query_all_artists())
    add_song_form = AddSong(meta={'csrf': False})
    return render_template('home.html',
                           artists_list=db_resp,
                           add_song_form=add_song_form)


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


@app.route('/artist/<id_artist>/song/<id_song>/', methods=['GET', 'DELETE', 'PUT'])
def song(id_artist, id_song):
    if request.method == 'DELETE':
        pass
    else:
        id_album = request.args.to_dict().get('id_album')
        translate = request.args.to_dict().get('translate')
        data_artist = db_req(query_artist_by_id(id_artist))[0]
        data_album = db_req(query_album_info(id_album))[0] if id_album not in [0, '0', '', 'None', None] else None
        data_song = db_req(query_song_data_by_id(id_artist, id_song))[0]
        if request.method == 'GET':
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
        elif request.method == 'PUT':

            return template(song_page_body(data_artist, data_album, data_song, translated_text=translate))


# @app.route('/add/', methods=['GET', 'POST'])
# def add_song():
#     if request.method == 'POST':
#         data = json.loads(request.form['add_song_form'])
#         query_add_song(data)
#     db_resp = db_req(query_all_artists())
#     add_song_form = AddSong(meta={'csrf': False})
#     return render_template('home.html',
#                            artists_list=db_resp,
#                            add_song_form=add_song_form)


if __name__ == '__main__':
    app.run(debug=True)
