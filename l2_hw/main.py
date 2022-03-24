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


data = {
    'artists': {
        'acdc': {
            'artist_name': 'AC/DC',
            'albums': {'tnt': {'album_title': 'T.N.T',
                               'album_songs': ['It`s a Long Way to the Top',
                                               'Rock `n` Roll Singer',
                                               'The Jack',
                                               'Live Wire',
                                               'T.N.T.',
                                               'Rocket',
                                               'Can I Sit Next to You, Girl',
                                               'High Voltage',
                                               'School Days (Chuck Berry)']}},
            'songs': {
                'tnt': {
                    'albums': ['T.N.T', 'High Voltage'],
                    'song_title': 'T.N.T',
                    'song_text': f"""
                        Lorem ipsum <br>
                        dolor sit amet, <br>
                        consectetur <br>
                        adipiscing elit <br>
                        """}
            }
        },
        'simple': {
            'artist_name': 'Simple',
            'albums': {'simplest': {'album_title': 'Simplest',
                                    'album_songs': ['Simple DiMplE Song',
                                                    'Wooppa Suppa']}},
            'songs': {
                'simple_dimple_song': {
                    'albums': ['Simplest', 'Sunday'],
                    'song_title': 'Simple DiMplE Song',
                    'song_text': f"""
                        sed do eiusmod <br>
                        tempor incididunt <br> 
                        ut labore et dolore <br> 
                        magna aliqua <br>
                        """}
            }
        }
    }
}


class RouteQualifier(object):
    def __init__(self):
        self.all_artists = AllArtists()
        self.artist_title = Artist()
        self.album = Album()
        self.song = Song()
        self.search = Search()

    def _cp_dispatch(self, vpath):
        path_len = len(vpath)
        if path_len == 1 and 'search' in vpath:
            vpath.pop(0)
            return self.search

        elif path_len == 2 and 'artist' in vpath:
            if 'update_song' in vpath:
                vpath = str(self.song.data['url']).split('/')[1:-1]
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = vpath.pop(0)
                vpath.pop(0)
                cherrypy.request.params['song_title'] = vpath.pop(0)
                return self.song.update_song
            elif 'new_song' in vpath:
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = vpath.pop(0)
                return self.song.new_song
            elif 'delete_song' in vpath:
                vpath = str(self.song.data['url']).split('/')[1:-1]
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = vpath.pop(0)
                vpath.pop(0)
                cherrypy.request.params['song_title'] = vpath.pop(0)
                return self.song.delete_song
            else:
                vpath.pop(0)
                cherrypy.request.params['artist_name'] = vpath.pop(0)
                return self.artist_title

        elif path_len == 4:
            vpath.pop(0)
            cherrypy.request.params['artist_name'] = vpath.pop(0)
            if 'album' in vpath:
                vpath.pop(0)
                cherrypy.request.params['album'] = vpath.pop(0)
                return self.album
            elif 'song' in vpath:
                vpath.pop(0)
                cherrypy.request.params['song_title'] = vpath.pop(0)
                return self.song
        else:
            return vpath

    @cherrypy.expose
    def index(self):
        return AllArtists().index()


class AllArtists(object):
    @cherrypy.expose
    def index(self):
        return template() % f'' \
            f'<br>' \
            f'<p>Simulate Search<p>' \
            f'<form action="search" method="GET">Enter your search text here...' \
                f'<input type="text" name="search_text"/>' \
                f'<input type="submit"/>' \
            f'</form>' \
            f'<br>' \
            f'<p>Simulate main page with all artists (root)</p>' \
            f'<ul>'\
                f'<li><a href="./artist/acdc">AC/DC</a></li>' \
                f'<li><a href="./artist/simple">simple</a></li>' \
            f'</ul>' \
            f'<br>' \
            f'<p>Simulate album page with all songs</p>' \
            f'<ul>' \
                f'<li><a href="./artist/acdc/album/tnt">AC/DC with album: T.N.T</a></li>' \
                f'<li><a href="./artist/simple/album/simplest">Simple with album: Simplest</a></li>' \
            f'</ul>' \
            f'<br>' \
            f'<p>Simulate songs page with song info and actions</p>' \
            f'<ul>' \
                f'<li><a href="./artist/acdc/song/tnt">AC/DC with song: T.N.T</a></li>' \
                f'<li><a href="./artist/simple/song/simple_dimple_song">Simple with song: Simple-Dimple</a></li>' \
            f'</ul>' \
            f'<br>' \
            f'<p>Add New artist</p>' \
            f'<form action="/artist/new_song/" method="put" id="form_add">' \
            f'<label for="new_artist_name">Artist:</label>' \
            f'<input type="text" id="new_artist_name" name="new_artist_name">' \
            f'<br>' \
            f'<label for="new_song_title">Song title:</label>' \
            f'<input type="text" id="new_song_title" name="new_song_title">' \
            f'<br>' \
            f'<label for="new_song_text">Song text:</label>' \
            f'<input type="text" id="new_song_text" name="new_song_text">' \
            f'<br>' \
            f'</form>' \
            f'<button type="submit" form="form_add" value="Submit">ADD</button>' \
            f'<br>'


@cherrypy.popargs('artist_name')
class Artist(object):
    @cherrypy.expose
    def index(self, artist_name):
        data_artist = data["artists"][artist_name]
        return template() % f'' \
            f'<h3>About artist: {data_artist["artist_name"]}<h3>' \
            f'<br>' \
            f'<h3>Albums: {list(data_artist["albums"][u_album]["album_title"] for u_album in data_artist["albums"])}</h3>' \
            f'<h3>Songs: {list(data_artist["songs"][u_song]["song_title"] for u_song in data_artist["songs"])}</h3>' \
            f'<br>' \
            f'<a href="/">Back --> Home</a>' \
            f'<br>'


@cherrypy.popargs('artist_name', 'album')
class Album(object):
    @cherrypy.expose
    def index(self, artist_name, album):
        data_artist = data["artists"][artist_name]
        return template() % f'' \
            f'<h3>About album: {data_artist["albums"][album]["album_title"]} by artist: {data_artist["artist_name"]}<h3>' \
            f'<br>' \
            f'<h3>Songs: <br><br>{"<br>".join(data_artist["albums"][album]["album_songs"])}</h3>' \
            f'<br>' \
            f'<a href="/">Back --> Home</a>' \
            f'<br>'


class Song(object):
    def __init__(self):
        self.data = data

    @cherrypy.expose
    def index(self, **kwargs):
        ar_k = data["artists"][kwargs["artist_name"]]
        artist = ar_k["artist_name"]
        song_title = ar_k["songs"][kwargs["song_title"]]["song_title"]
        song_text = ar_k["songs"][kwargs["song_title"]]["song_text"]
        self.data['url'] = cherrypy.request.path_info
        return template() % f'' \
            f'<h3>About song: {song_title} <br>by artist: {artist}<h3>' \
            f'<br>' \
            f'<h4>Song text</h4>' \
            f'<p>{song_text}</p>' \
            f'<br>' \
            f'<br>' \
            f'<br>' \
            f'<form action="/artist/update_song" method="post" id="form_update">' \
            f'<label for="new_song_text">Update Song text:</label>' \
            f'<input type="text" id="new_song_text" name="new_song_text">' \
            f'<br>' \
            f'</form>' \
            f'<button type="submit" form="form_update" value="Submit">Update</button>' \
            f'<br>' \
            f'<form action="/artist/delete_song" method="delete" id="form_delete">' \
            f'</form>' \
            f'<button type="submit" form="form_delete" value="Delete">Delete</button>' \
            f'<br>' \
            f'<br>' \
            f'<a href="/">Back --> Home</a>' \
            f'<br>'

    @cherrypy.expose
    def new_song(self, *args, **kwargs):  # PUT
        u_artist_name = kwargs['new_artist_name'].replace(" ", "-").replace("/", "_").lower()
        u_song_title = kwargs['new_song_title'].replace(" ", "-").replace("/", "_").lower()
        self.data['artists'][u_artist_name] = {'artist_name': kwargs['new_artist_name'],
                                               'songs': {u_song_title: {'song_title': kwargs['new_song_title'],
                                                                        'song_text': kwargs['new_song_text']}}}
        ar_k = self.data["artists"][u_artist_name]
        artist = ar_k["artist_name"]
        song_title = ar_k["songs"][u_song_title]["song_title"]
        song_text = ar_k["songs"][u_song_title]["song_text"]
        print(ar_k)
        return template() % f'' \
            f'<h3>About new song: {song_title} <br>by new artist: {artist}<h3>' \
            f'<br>' \
            f'<h4>New Song text</h4>' \
            f'<p>{song_text}</p>' \
            f'<br>' \
            f'<br>' \
            f'<a href="/">Back --> Home</a>' \
            f'<br>'

    @cherrypy.expose
    def update_song(self, *args, **kwargs):  # POST
        self.data["artists"][kwargs["artist_name"]]["songs"][kwargs["song_title"]]["song_text"] = kwargs["new_song_text"]
        ar_k = self.data["artists"][kwargs["artist_name"]]
        artist = ar_k["artist_name"]
        song_title = ar_k["songs"][kwargs["song_title"]]["song_title"]
        song_text = ar_k["songs"][kwargs["song_title"]]["song_text"]
        print(ar_k)
        return template() % f'' \
            f'<h3>About updated song: {song_title} <br>by artist: {artist}<h3>' \
            f'<br>' \
            f'<h4>Updated Song text</h4>' \
            f'<p>{song_text}</p>' \
            f'<br>' \
            f'<br>' \
            f'<a href="/">Back --> Home</a>' \
            f'<br>'

    @cherrypy.expose
    def delete_song(self, *args, **kwargs):  # DELETE
        self.data["artists"][kwargs["artist_name"]]["songs"].pop(kwargs["song_title"], None)
        ar_k = self.data["artists"][kwargs["artist_name"]]
        artist = ar_k["artist_name"]
        song_title = kwargs["song_title"]
        print(ar_k)
        return template() % f'' \
            f'<h3>Deleted song: {song_title} <br>by artist: {artist}<h3>' \
            f'<br>' \
            f'<br>' \
            f'<a href="/">Back --> Home</a>' \
            f'<br>'


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
