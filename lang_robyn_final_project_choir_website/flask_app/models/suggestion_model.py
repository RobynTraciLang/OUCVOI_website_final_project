from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import member_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'oucvoi_final'


class Suggestion:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.artist = data['artist']
        self.link = data['link']
        self.member_id = data['member_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.member = None


    @classmethod
    def create_suggestion(cls, data):
        query = '''
        INSERT INTO suggestions (title, artist, link, member_id) VALUES (%(title)s, %(artist)s, %(link)s, %(member_id)s)
        ;'''
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_all_suggestions_with_member(cls):
        query = '''
        SELECT * FROM suggestions
        LEFT JOIN members ON suggestions.member_id = members.id
        ;'''
        results = connectToMySQL(db).query_db(query)
        suggestions = []
        for each_suggestion in results:
            suggestion_instance = cls(each_suggestion)
            member_data = {
                'id': each_suggestion['members.id'],
                'first_name': each_suggestion['first_name'],
                'last_name': each_suggestion['last_name'],
                'role': each_suggestion['role'],
                'voice_part': each_suggestion['voice_part'],
                'phone': each_suggestion['phone'],
                'email': each_suggestion['email'],
                'password': None,
                'created_at': each_suggestion['members.created_at'],
                'updated_at': each_suggestion['members.updated_at'],
            }
            suggestion_instance.member = member_model.Member(member_data)
            suggestions.append(suggestion_instance)
        return suggestions


    @classmethod
    def edit_suggestion(cls, data):
        query = '''
        UPDATE suggestions SET title = %(title)s, artist = %(artist)s, link = %(link)s, member_id = %(member_id)s WHERE suggestions.id = %(id)s
        ;'''
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def delete_suggestion(cls, suggestion_id):
        query = '''
        DELETE FROM suggestions WHERE id = %(id)s
        ;'''
        data = {'id': suggestion_id}
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_suggestion_by_id(cls, data):
        query = '''
        SELECT * from suggestions
        LEFT JOIN members on suggestions.member_id = members.id
        WHERE suggestions.id = %(id)s
        ;'''
        suggestion_id = {
            'id': data
        }
        result = connectToMySQL(db).query_db(query, suggestion_id)
        suggestion_instance = cls(result[0])
        for suggestion in result:
            member_data = {
                'id': suggestion['members.id'],
                'first_name': suggestion['first_name'],
                'last_name': suggestion['last_name'],
                'role': suggestion['role'],
                'voice_part': suggestion['voice_part'],
                'phone': suggestion['phone'],
                'email': suggestion['email'],
                'password': None,
                'created_at': suggestion['members.created_at'],
                'updated_at': suggestion['members.updated_at'],
            }
            member_instance = member_model.Member(member_data)
            suggestion_instance.member = member_instance
        return suggestion_instance