from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import member_model, suggestion_model, event_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'oucvoi_final'


class Song:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.artist = data['artist']
        self.link = data['link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.event = []

    @classmethod
    def create_song(cls, data):
        query = '''
        INSERT INTO songs (title, artist, link)
        VALUES (%(title)s, %(artist)s, %(link)s)
        ;'''
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_all_songs_by_event(cls):
        query = '''
        SELECT * FROM songs
        LEFT JOIN events ON performance_songs.event_id = events.id
        LEFT JOIN performance_songs ON performance_songs.song_id = songs.id
        ;'''
        results = connectToMySQL(db).query_db(query)
        songs = []
        for each_song in results:
            if len(songs) == 0 or each_song['id'] != songs[len(songs) - 1].id:
                song_instance = cls(each_song)
                songs.append(song_instance)
            song_instance = songs[len(songs) - 1]
            event_data = {
                'id': each_song['events.id'],
                'event_name': each_song['event_name'],
                'description': each_song['description'],
                'start_date': each_song['start_date'],
                'end_date': each_song['end_date'],
                'start_time': each_song['start_time'],
                'end_time': each_song['end_time'],
                'location_name': each_song['location_name'],
                'address': each_song['address'],
                'created_at': each_song['events.created_at'],
                'updated_at': each_song['events.updated_at'],
            }
            song_instance.events.append(event_model.Event(event_data))
        return songs