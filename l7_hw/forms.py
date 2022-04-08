from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddSong(FlaskForm):
    new_artist_name = StringField('new_artist_name', validators=[DataRequired()])
    new_artist_info = StringField('new_artist_info')

    new_album_title = StringField('new_album_title')
    new_album_year = StringField('new_album_year')
    new_album_info = StringField('new_album_info')

    new_song_title = StringField('new_song_title', validators=[DataRequired()])
    new_song_year = StringField('new_song_year')
    new_song_text = StringField('new_song_text', validators=[DataRequired()])
    new_song_lang = StringField('new_song_lang', validators=[DataRequired()])
