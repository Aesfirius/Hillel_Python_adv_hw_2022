import os
import urllib.parse
import cherrypy
import sqlite3

from l4_hw.queries import *
from l4_hw.view import *
from l4_hw.helpers import f_from_url, f_for_url

"""
/
/artist/<id_artist>
/artist/<id_artist>/album/<id_album>
/artist/<id_artist>/song/<id_song>
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
                # vpath = str(self.crumbs['url']).split('/')[1:-1]
                vpath.pop(0)
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = self.crumbs['artist']
                cherrypy.request.params['song_title'] = self.crumbs['song']
                return self.song.update_song
            elif 'new_song' == vpath[1]:
                vpath.pop(0)
                vpath.pop(0)
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

        # defaults
        d_map = 000

        # add song
        song_tuple = (new_song_title, int(new_song_year), new_song_text, new_song_lang)
        if None not in (new_song_title, new_song_year, new_song_text, new_song_lang):
            d_map += 100

        # add album
        album_tuple = (new_album_title, int(new_album_year), new_album_info)
        if None not in (new_album_title, new_album_year):
            d_map += 10

        # add artist
        artist_tuple = (new_artist_name, new_artist_info)
        if new_artist_name is not None:
            d_map += 1

        # add to track list
        if d_map == 111:
            # add song
            db_req(query_insert_new_song(*song_tuple))
            new_song_id = db_req(get_last_song_id())[0]['id_song']
            # add album
            db_req(query_insert_new_album(*album_tuple))
            new_album_id = db_req(get_last_album_id())[0]['id_album']
            # add artist
            db_req(query_insert_new_artist(*artist_tuple))
            new_artist_id = db_req(get_last_artist_id())[0]['id_artist']

            # add track list
            track_list_tuple = (int(new_artist_id), int(new_song_id), int(new_album_id), int(new_song_track_number))
            db_req(query_insert_new_track_list(*track_list_tuple))
            return template(song_page_body_new_success(new_artist_name, new_song_title))

    @cherrypy.expose
    def update_song(self, **kwargs):  # POST
        db_req(query_update_song_text(kwargs['song_title'], kwargs['new_song_text']))
        return template(song_page_body_update_text(kwargs['artist_name'], kwargs['song_title']))

    @cherrypy.expose
    def delete_song(self, artist_name, song_title):  # DELETE
        # todo ! QUERY !
        # получить Id_song
        # удалить строку из таблицы track list
        # удалить строку из таблицы song
        return template(song_page_body_deleted(artist_name, song_title))


class Search(object):
    @cherrypy.expose
    def index(self, search_text):
        if search_text == '':
            search_text = 'Go Back and take a cup of coffee'
        return template(search_page_body(search_text))


if __name__ == '__main__':
    cherrypy.quickstart(RouteQualifier())
