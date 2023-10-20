from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import song_model, performance_song_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'oucvoi_final'


class Event:
    def __init__(self, data):
        self.id = data['id']
        self.event_name = data['event_name']
        self.description = data['description']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.location_name = data['location_name']
        self.address = data['address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.songs = []


    @classmethod
    def create_event(cls, data):
        query = '''
        INSERT INTO events (event_name, description, start_date, end_date, start_time, end_time, location_name, address)
        VALUES (%(event_name)s, %(description)s, %(start_date)s, %(end_date)s, %(start_time)s, %(end_time)s, %(location_name)s, %(address)s)
        ;'''
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_event_by_id(cls, data):
        query = '''
        SELECT * FROM events
        LEFT JOIN performance_songs ON performance_songs.event_id = events.id
        LEFT JOIN performance_songs ON performance_songs.song_id = songs.id
        WHERE start_date = %(start_date)s
        AND end_date = %(end_date)s
        ;'''
        results = connectToMySQL(db).query_db(query, data)
        events = []
        for each_event in results:
            if len(events) == 0 or each_event['id'] != events[len(events) - 1].id:
                event_instance = cls(each_event)
                events.append(event_instance)
            event_instance = events[len(events) - 1]
            performance_song_data = {
                'id': each_event['performance_songs.id'],
                'title': each_event['performance_songs.title'],
                'artist': each_event['performance_songs.artist'],
                'link': each_event['performance_songs.link'],
                'created_at': each_event['performance_songs.created_at'],
                'updated_at': each_event['performance_songs.updated_at'],
            }
            event_instance.songs.append(performance_song_model.Performance_song(performance_song_data))
        return events


    @classmethod
    def get_all_events_with_songs(cls):
        query = '''
        SELECT * FROM events
        LEFT JOIN performance_songs ON performance_songs.event_id = events.id
        LEFT JOIN songs ON performance_songs.song_id = songs.id;
        ;'''
        results = connectToMySQL(db).query_db(query)
        events = []
        for each_event in results:
            if len(events) == 0 or each_event['id'] != events[len(events) - 1].id:
                event_instance = cls(each_event)
                events.append(event_instance)
            event_instance = events[len(events) - 1]
            song_data = {
                'id': each_event['performance_songs.id'],
                'title': each_event['title'],
                'artist': each_event['artist'],
                'link': each_event['link'],
                'created_at': each_event['performance_songs.created_at'],
                'updated_at': each_event['performance_songs.updated_at'],
            }
            event_instance.songs.append(song_model.Song(song_data))
        return events


    @classmethod
    def get_all_events_by_date_with_songs(cls):
        query = '''
        SELECT * FROM events
        LEFT JOIN performance_songs ON performance_songs.event_id = events.id
        LEFT JOIN performance_songs ON performance_songs.song_id = songs.id
        WHERE start_date = %(start_date)s
        AND end_date = %(end_date)s
        ;'''
        results = connectToMySQL(db).query_db(query)
        events = []
        for each_event in results:
            if len(events) == 0 or each_event['id'] != events[len(events) - 1].id:
                event_instance = cls(each_event)
                events.append(event_instance)
            event_instance = events[len(events) - 1]
            performance_song_data = {
                'id': each_event['performance_songs.id'],
                'song_id': each_event['song_id'],
                'event_id': each_event['event_id'],
                'created_at': each_event['performance_songs.created_at'],
                'updated_at': each_event['performance_songs.updated_at'],
            }
            event_instance.songs.append(performance_song_model.Performance_song(performance_song_data))
        return events