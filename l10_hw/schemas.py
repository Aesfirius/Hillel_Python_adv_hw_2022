from marshmallow import Schema, fields, validate
from marshmallow import ValidationError
from constants import LANG_CODES


###########################################
#                  ADD                    #
###########################################

class ADDSongSchema(Schema):
    song_title = fields.String(validate=validate.Length(min=1), required=True)
    song_text = fields.String(validate=validate.Length(min=1), required=True)
    song_year = fields.Integer(validate=validate.Range(min=1950, max=2022), required=True)
    song_lang = fields.String(validate=validate.OneOf(LANG_CODES), required=True)


class ADDArtistSchema(Schema):
    artist_name = fields.String(validate=validate.Length(min=1), required=True)
    artist_info = fields.String(validate=validate.Length(min=1), required=False)
    album_info = fields.Dict(required=False)


class ADDAlbumSchema(Schema):
    album_title = fields.String(validate=validate.Length(min=1), required=True)
    album_year = fields.Integer(validate=validate.Range(min=1950, max=2022), required=False)
    album_info = fields.String(validate=validate.Length(min=1), required=False)
    track_number = fields.Integer(validate=validate.Range(min=1, max=100), required=True)


def validate_track_data__add(json_data):
    """
    {
  "song_info": {
    "song_title": "song title 9",
    "song_text": "blah-blah-blah 9",
    "song_year": 1989,
    "song_lang": "en"
  },
  "artist_info": [
    {
      "artist_name": "Artist name 9",
      "artist_info": "artist info bla-bla",
      "album_info": [
        {
          "album_title": "Album title 9.1",
          "album_year": 1991,
          "album_info": "album info9.1",
          "track_number": 5
        },
        {
          "album_title": "Album title 9.2",
          "album_year": 1993,
          "album_info": "album info9.2",
          "track_number": 5
        }
      ]
    }
  ]
}
    """
    errors = []
    if json_data.get('song_info') is not None:
        try:
            ADDSongSchema().load(json_data['song_info'])
        except ValidationError as err:
            errors.append(err.messages)
        if json_data.get('artist_info') is not None and len(json_data['artist_info']) > 0:
            for art_info in json_data['artist_info']:
                try:
                    ADDArtistSchema().load(art_info)
                except ValidationError as err:
                    errors.append(err.messages)
                if art_info.get('album_info') is not None and len(art_info['album_info']) > 0:
                    for album in art_info['album_info']:
                        try:
                            ADDAlbumSchema().load(album)
                        except ValidationError as err:
                            errors.append(err.messages)
    else:
        return """NEED MORE DATA"""
    if len(errors) > 0:
        print(ValidationError(errors))
        return ValidationError(errors)


###########################################
#                UPDATE                   #
###########################################

class UPDATESongSchema(Schema):
    song_text = fields.String(validate=validate.Length(min=1), required=True)


def validate_song_data__update(song_data):
    try:
        UPDATESongSchema().load(song_data)
    except ValidationError as err:
        return err.messages, 400
