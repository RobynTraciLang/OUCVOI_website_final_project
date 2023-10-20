from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import member_model, suggestion_model, song_model
from flask import flash
import pprint
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'oucvoi_final'


class Performance_song:
    def __init__(self, data):
        self.id = data['id']
        self.song_id = data['song_id']
        self.event_id = data['event_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_performance_song(cls, data):
        query = '''
        INSERT INTO performance_songs (song_id, event_id) VALUES (%(song_id)s, %(event_id)s)
        ;'''
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_all_performance_songs_by_event(cls):
        query = '''
        SELECT * FROM performance_songs
        WHERE event_id = %(event_id)s
        ;'''
        results = connectToMySQL(db).query_db(query)
        return results