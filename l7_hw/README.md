##Урок 7
### ТЗ
    
    Flask
    -----------------------------------------------------------------------------------------------------------------
---


### ДЗ

    Добавить в роут /add метод POST и дописать функци добавления данных
    * Добавить методы для остальных эндпоинтов с обновлением данных, 
      а для песни ещё и удаление песни по методу DELETE
---


схема входящих данных
```json
{
  "song_info": {
    "song_title": "song title 9",
    "song_text": "blah-blah-blah 9",
    "song_year": "1989",
    "song_lang": "en"
  },
  "artist_info": [
    {
      "artist_name": "Artist name 9",
      "artist_info": "artist info bla-bla",
      "album_info": [
        {
          "album_title": "Album title 9.1",
          "album_year": "1991",
          "album_info": "album info9.1",
          "track_number": "1"
        },
        {
          "album_title": "Album title 9.2",
          "album_year": "1992",
          "album_info": "album info9.2",
          "track_number": "5"
        }
      ]
    }
  ]
}
```