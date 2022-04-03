import os
import cherrypy
import sqlite3

from l5_hw.queries import *
from l5_hw.view import *
from l5_hw.helpers import translate_to

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
                vpath.pop(0)
                vpath.pop(0)
                cherrypy.request.params['id_artist'] = self.crumbs['artist']
                cherrypy.request.params['id_song'] = self.crumbs['song']
                return self.song.update_song
            elif 'new_song' == vpath[1]:
                vpath.pop(0)
                vpath.pop(0)
                return self.song.new_song
            elif 'delete_song' == vpath[1]:
                vpath.pop(0)
                vpath.pop(0)
                cherrypy.request.params['id_artist'] = self.crumbs['artist']
                cherrypy.request.params['id_song'] = self.crumbs['song']
                return self.song.delete_song
            else:
                vpath.pop(0)
                cherrypy.request.params['id_artist'] = vpath.pop(0)
                return self.artist_title

        elif path_len == 4:
            vpath.pop(0)
            cherrypy.request.params['id_artist'] = vpath.pop(0)
            if 'album' == vpath[0]:
                vpath.pop(0)
                cherrypy.request.params['id_album'] = vpath.pop(0)
                return self.album
            elif 'song' == vpath[0]:
                vpath.pop(0)
                cherrypy.request.params['id_song'] = vpath.pop(0)
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
        db_resp = db_req(query_all_artists())
        return template(home_page_body(db_resp))


class Artist(object):

    def __init__(self, home):
        self.crumbs = home.crumbs

    @cherrypy.expose
    def index(self, id_artist):
        self.crumbs['artist'] = id_artist

        data_artist = db_req(query_artist_by_id(id_artist))
        data_albums = db_req(query_all_albums(id_artist))
        data_x_songs = db_req(query_songs_not_in_albums(id_artist))

        return template(artist_page_body(data_artist, data_albums, data_x_songs))


class Album(object):

    def __init__(self, home):
        self.crumbs = home.crumbs

    @cherrypy.expose
    def index(self, id_artist, id_album):
        self.crumbs['artist'] = id_artist
        self.crumbs['album'] = id_album

        data_artist = db_req(query_artist_by_id(id_artist))
        data_album = db_req(query_album_info(id_album))
        data_songs = db_req(query_album_songs(id_artist, id_album))

        return template(album_page_body(data_artist, data_album, data_songs))


class Song(object):

    def __init__(self, home):
        self.crumbs = home.crumbs

    @cherrypy.expose
    def index(self, id_artist, id_song, id_album=None, translate=None):
        self.crumbs['artist'] = id_artist
        self.crumbs['song'] = id_song

        data_artist = db_req(query_artist_by_id(id_artist))
        data_album = db_req(query_album_info(id_album)) if id_album not in [0, '0', '', 'None', None] else None
        data_song = db_req(query_song_data_by_id(id_artist, id_song))

        if translate is not None:
            translated_text = translate_to(origin_text=data_song[0]['song_text'], from_lang=data_song[0]['origin_lang'], to_lang=translate)
        else:
            translated_text = translate

        return template(song_page_body(data_artist, data_album, data_song, translated_text=translated_text))

    @cherrypy.expose
    def new_song(self,
                 new_artist_name='',
                 new_artist_info='',
                 new_album_title='',
                 new_album_year='',
                 new_album_info='',
                 new_song_title='',
                 new_song_year='',
                 new_song_text='',
                 new_song_lang='',
                 new_song_track_number=1000,
                 ):  # PUT

        # defaults
        track_list_params = {}

        # add artist
        artist_tuple = (new_artist_name, new_artist_info)
        if new_artist_name != '':
            data_artist = db_req(query_artist_by_name(new_artist_name))
            if len(data_artist) == 0:
                db_req(query_insert_new_artist(*artist_tuple))
                new_artist_id = int(db_req(get_last_artist_id())[0]['id_artist'])
                track_list_params['id_artist'] = new_artist_id
            else:
                track_list_params['id_artist'] = data_artist[0]['id_artist']

        # add song
        song_tuple = (new_song_title, int(new_song_year), new_song_text, new_song_lang)
        if all(song_tuple):
            data_song = db_req(query_song_data_by_title(track_list_params['id_artist'], new_song_title))
            if len(data_song) == 0:
                db_req(query_insert_new_song(*song_tuple))
                new_song_id = int(db_req(get_last_song_id())[0]['id_song'])
                track_list_params['id_song'] = new_song_id
            else:
                track_list_params['id_song'] = data_song[0]['id_song']

        # add album
        album_tuple = (new_album_title, new_album_year, new_album_info)
        if new_album_title != '':
            data_album = db_req(query_album_info_by_title(new_album_title))
            if len(data_album) == 0:
                db_req(query_insert_new_album(*album_tuple))
                new_album_id = int(db_req(get_last_album_id())[0]['id_album'])
                track_list_params['id_album'] = new_album_id
            else:
                track_list_params['id_album'] = data_album[0]['id_album']

        # add track list
        track_list_params['track_number'] = new_song_track_number
        db_req(query_insert_new_track_list(track_list_params))

        return template(song_page_body_new_success(new_artist_name, new_song_title))

    @cherrypy.expose
    def update_song(self, **kwargs):  # POST
        data_artist = db_req(query_artist_by_id(kwargs['id_artist']))
        data_song = db_req(query_song_data_by_id(kwargs['id_artist'], kwargs['id_song']))
        db_req(query_update_song_text(kwargs['id_song'], kwargs['new_song_text']))
        return template(song_page_body_update_text(data_artist, data_song))

    @cherrypy.expose
    def delete_song(self, id_artist, id_song):  # DELETE
        data_artist = db_req(query_artist_by_id(id_artist))
        data_song = db_req(query_song_data_by_id(id_artist, id_song))

        query_delete_song_track_list(id_artist, id_song)
        query_delete_song_from_songs_table(id_song)
        return template(song_page_body_deleted(data_artist, data_song))


class Search(object):
    @cherrypy.expose
    def index(self, search_text):
        if search_text == '':
            return template(search_page_body_empty())
        else:
            artists_data = db_req(query_search_all_artists_by_like(search_text))
            albums_data = db_req(query_search_all_albums_by_like(search_text))
            songs_data = db_req(query_search_all_songs_by_like(search_text))
            return template(search_page_body(search_text, artists_data, albums_data, songs_data))


if __name__ == '__main__':
    cherrypy.quickstart(RouteQualifier())
