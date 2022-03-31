import os
import urllib.parse
import cherrypy
import sqlite3

from l4_hw.queries import *
from l4_hw.view import *
from l4_hw.helpers import f_from_url, f_for_url

"""
/
/artist/<artist>
/artist/<artist>/album/<album>
/artist/<artist>/song/<song>
/search
"""


def db_req(sql_query):
    """
    :param sql_query: SQL query
    :return: [{k1:v1, k2:v1}, {k3:v3, k4:v4}]
    """
    db_name = os.environ.get('DB_NAME')
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql_query)
    result = [dict(i) for i in cur.fetchall()]
    con.commit()
    con.close()
    return result


class RouteQualifier(object):

    def __init__(self):
        self.crumbs = {'artist': '', 'album': '', 'song': ''}
        self.all_artists = AllArtists()
        self.artist_title = Artist(self)
        self.album = Album(self)
        self.song = Song(self)
        self.search = Search()

    def _cp_dispatch(self, vpath):
        print(self.crumbs)
        path_len = len(vpath)
        if path_len == 1 and 'search' in vpath:
            vpath.pop(0)
            return self.search

        elif path_len == 2 and 'artist' == vpath[0]:
            if 'update_song' == vpath[1]:
                vpath = str(self.crumbs['url']).split('/')[1:-1]
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = vpath.pop(0)
                vpath.pop(0)
                cherrypy.request.params['song_title'] = vpath.pop(0)
                return self.song.update_song
            elif 'new_song' == vpath[1]:
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = vpath.pop(0)
                return self.song.new_song
            elif 'delete_song' == vpath[1]:
                vpath.pop(0)
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = self.crumbs['artist']
                cherrypy.request.params['song_title'] = self.crumbs['song']
                return self.song.delete_song
            else:
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = vpath.pop(0)
                return self.artist_title

        elif path_len == 4:
            vpath.pop(0)
            cherrypy.request.params['artist_name'] = vpath.pop(0)
            if 'album' == vpath[0]:
                vpath.pop(0)
                cherrypy.request.params['album_title'] = vpath.pop(0)
                return self.album
            elif 'song' == vpath[0]:
                vpath.pop(0)
                cherrypy.request.params['song_title'] = vpath.pop(0)
                return self.song
        else:
            return self.all_artists.index()
        vpath = []
        return self

    @cherrypy.expose
    def index(self):
        return self.all_artists.index()


class AllArtists(object):
    @cherrypy.expose
    def index(self):
        db_resp = db_req(query_artists())
        return template(home_page_body(db_resp))


@cherrypy.popargs('artist_name')
class Artist(object):

    def __init__(self, home):
        self.crumbs = home.crumbs

    @cherrypy.expose
    def index(self, artist_name):
        self.crumbs['artist'] = artist_name

        n_artist_name = f_from_url(urllib.parse.unquote_plus(artist_name))

        data_artist = db_req(query_artist(n_artist_name))
        data_albums = db_req(query_albums(n_artist_name))
        data_x_songs = db_req(query_songs_not_in_albums(n_artist_name))

        return template(artist_page_body(artist_name, data_artist, data_albums, data_x_songs))


@cherrypy.popargs('artist_name', 'album_title')
class Album(object):

    def __init__(self, home):
        self.crumbs = home.crumbs

    @cherrypy.expose
    def index(self, artist_name, album_title):
        self.crumbs['artist'] = artist_name
        self.crumbs['album'] = album_title

        n_artist_name = f_from_url(urllib.parse.unquote_plus(artist_name))
        n_album_title = f_from_url(urllib.parse.unquote_plus(album_title))

        data_album = db_req(query_album_info(n_album_title))
        data_songs = db_req(query_album_songs(n_artist_name, n_album_title))

        return template(album_page_body(artist_name, album_title, data_album, data_songs))


class Song(object):

    def __init__(self, home):
        self.crumbs = home.crumbs

    @cherrypy.expose
    def index(self, artist_name, song_title):
        self.crumbs['artist'] = artist_name
        self.crumbs['song'] = song_title

        n_artist_name = f_from_url(urllib.parse.unquote_plus(artist_name))
        n_song_title = f_from_url(urllib.parse.unquote_plus(song_title))

        data_song = db_req(query_song_data(n_artist_name, n_song_title))
        song_text = data_song[0]['song_text'].replace('\n', '<br>')
        return template(song_page_body(artist_name, self.crumbs['album'], song_title, data_song, song_text))

    @cherrypy.expose
    def new_song(self,
                 new_artist_name=None,
                 new_artist_info=None,
                 new_album_title=None,
                 new_album_year=None,
                 new_album_info=None,
                 new_song_title=None,
                 new_song_year=None,
                 new_song_text=None,
                 new_song_lang=None,
                 new_song_track_number=None,
                 ):  # PUT

        # check important song data
        if new_song_title is not None \
                and new_song_year is not None\
                and new_song_text is not None\
                and new_song_lang is not None:
            # INSERT IN DB
            db_req(query_insert_new_song)
            pass
        pass

        #
        #
        # # INSERT IN DB
        # self.data['artists'][u_artist_name] = {'artist_name': kwargs['new_artist_name'],
        #                                        'songs': {u_song_title: {'song_title': kwargs['new_song_title'],
        #                                                                 'song_text': kwargs['new_song_text']}}}
        # # GET FROM DB
        # ar_k = self.data["artists"][u_artist_name]
        # artist = ar_k["artist_name"]
        # song_title = ar_k["songs"][u_song_title]["song_title"]
        # song_text = ar_k["songs"][u_song_title]["song_text"]
        # print(ar_k)
        # return template() % f'' \
        #     f'<h3>About new song: {song_title} <br>by new artist: {artist}<h3>' \
        #     f'<br>' \
        #     f'<h4>New Song text</h4>' \
        #     f'<p>{song_text}</p>' \
        #     f'<br>' \
        #     f'<br>' \
        #     f'<a href="/">Back --> Home</a>' \
        #     f'<br>'

    @cherrypy.expose
    def update_song(self, *args, **kwargs):  # POST
        pass
        # self.data["artists"][kwargs["artist_name"]]["songs"][kwargs["song_title"]]["song_text"] = kwargs["new_song_text"]
        # ar_k = self.data["artists"][kwargs["artist_name"]]
        # artist = ar_k["artist_name"]
        # song_title = ar_k["songs"][kwargs["song_title"]]["song_title"]
        # song_text = ar_k["songs"][kwargs["song_title"]]["song_text"]
        # print(ar_k)
        # return template() % f'' \
        #     f'<h3>About updated song: {song_title} <br>by artist: {artist}<h3>' \
        #     f'<br>' \
        #     f'<h4>Updated Song text</h4>' \
        #     f'<p>{song_text}</p>' \
        #     f'<br>' \
        #     f'<br>' \
        #     f'<a href="/">Back --> Home</a>' \
        #     f'<br>'

    @cherrypy.expose
    def delete_song(self, artist_name, song_title):  # DELETE
        return template(song_page_body_deleted(artist_name, song_title))
        # self.data["artists"][kwargs["artist_name"]]["songs"].pop(kwargs["song_title"], None)
        # ar_k = self.data["artists"][kwargs["artist_name"]]
        # artist = ar_k["artist_name"]
        # song_title = kwargs["song_title"]
        # print(ar_k)
        # return template() % f'' \
        #     f'<h3>Deleted song: {song_title} <br>by artist: {artist}<h3>' \
        #     f'<br>' \
        #     f'<br>' \
        #     f'<a href="/">Back --> Home</a>' \
        #     f'<br>'


class Search(object):
    @cherrypy.expose
    def index(self, search_text):
        pass
        # if search_text == '':
        #     search_text = 'Go Back and take a cup of coffee'
        # return template() % f'' \
        #     f'<h3>You searching:</h3>' \
        #     f'<br>' \
        #     f'<h3><b>{search_text}</b></h3>' \
        #     f'<br>' \
        #     f'<a href="/">Back --> Home</a>' \
        #     f'<br>'


if __name__ == '__main__':
    cherrypy.quickstart(RouteQualifier())
