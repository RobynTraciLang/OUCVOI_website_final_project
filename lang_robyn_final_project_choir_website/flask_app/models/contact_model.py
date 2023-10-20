from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import member_model, suggestion_model, song_model, event_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'oucvoi_final'


class Contact:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.company_name = data['company_name']
        self.reason = data['reason']
        self.how = data['how']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_contact(cls, data):
        query = '''
        INSERT INTO contacts (first_name, last_name, email, company_name, reason, how) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(company_name)s, %(reason)s, %(how)s)
        ;'''
        return connectToMySQL(db).query_db(query, data)