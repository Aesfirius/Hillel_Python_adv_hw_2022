import cherrypy

"""
/
/artist/<artist>
/artist/<artist>/album/<album>
/artist/<artist>/song/<song>
/search

"""


def template():
    return '<html><body>' \
           '<h2>Hillel HW Lesson 2</h2>' \
           '<br>' \
           '<br>' \
           '%s' \
           '</body></html>'


class RouteQualifier(object):
    def __init__(self):
        self.all_artists = AllArtists()
        self.artist = Artist()
        self.album = Album()
        # self.song = Song()
        self.search = Search()

    def _cp_dispatch(self, vpath):
        print(vpath)
        path_len = len(vpath)

        if path_len == 1 and 'search' in vpath:
            vpath.pop(0)
            return self.search

        elif path_len == 2 and 'artist' in vpath:
            vpath.pop(0)
            cherrypy.request.params['artist_name'] = vpath.pop(0)
            return self.artist

        elif path_len == 4:
            if 'album' in vpath:
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = vpath.pop(0)
                vpath.pop(0)
                cherrypy.request.params['album'] = vpath.pop(0)
                print(vpath)
                return self.album
            # elif 'song' in vpath:
            #     return self.song
        else:
            return AllArtists().index()

    @cherrypy.expose
    def index(self):
        return AllArtists().index()


class AllArtists(object):
    @cherrypy.expose
    def index(self):
        return template() % f'' \
            f'<h3>You see a list of all Artists</h3>' \
            f'<br>' \
            f'<form action="search" method="GET">' \
            f'Enter your search text here...' \
            f'<input type="text" name="search_text"/>' \
            f'<input type="submit"/>' \
            f'</form>' \
            f'<br>' \
            f'<ul>' \
            f'<li><a href="./artist/acdc?artist_name=AC/DC">AC/DC</a></li>' \
            f'<li><a href="./artist/simple">simple</a></li>' \
            f'</ul>' \
            f'<br>' \
            f'<ul>' \
            f'<li><a href="./artist/acdc/album/tnt?artist_name=AC/DC&album=T.N.T">AC/DC    album: T.N.T</a></li>' \
            f'<li><a href="./artist/simple/album/simplest">Simple    album: Simplest</a></li>' \
            f'</ul>'


@cherrypy.popargs('artist_name')
class Artist(object):
    @cherrypy.expose
    def index(self, artist_name):
        return template() % f'' \
            f'<h3>About artist:<h3>' \
            f'<br>' \
            f'<h3>{artist_name}</h3>'\
            f'<br>' \
            f'<a href="/">Back --> Home</a>' \
            f'<br>'


# @cherrypy.popargs('artist_name', 'album')
class Album(object):
    @cherrypy.expose
    def index(self, artist_name, album):
        return template() % f'{artist_name, album}' \
            f'<h3>About album: {"album"} by artist: {"artist"}<h3>' \
            f'<br>' \
            f'<a href="/">Back --> Home</a>' \
            f'<br>'


# @cherrypy.popargs('artist_name', 'song_title')
# class Song(object):
#     @cherrypy.expose
#     def index(self, artist, title):
#         return 'Song about %s by %s...' % (title, artist)


class Search(object):
    @cherrypy.expose
    def index(self, search_text):
        if search_text == '':
            search_text = 'Go Back and take a cup of coffee'
        return template() % f'' \
            f'<h3>You searching:</h3>' \
            f'<br>' \
            f'<h3><b>{search_text}</b></h3>' \
            f'<br>' \
            f'<a href="/">Back --> Home</a>' \
            f'<br>'


if __name__ == '__main__':
    cherrypy.quickstart(RouteQualifier(), '')