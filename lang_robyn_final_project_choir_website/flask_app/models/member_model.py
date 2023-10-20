from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'oucvoi_final'


class Member:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.role = data['role']
        self.voice_part = data['voice_part']
        self.phone = data['phone']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.address = None


    @classmethod
    def create_member(cls, data):
        query = '''
        INSERT INTO members (first_name, last_name, role, voice_part, phone, email, password) VALUES (%(first_name)s, %(last_name)s, %(role)s, %(voice_part)s, %(phone)s, %(email)s, %(password)s)
        ;'''
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_member_by_id(cls, member_id):
        query = 'SELECT * FROM members WHERE members.id = %(id)s;'
        data = {
            'id': member_id
        }
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all_members(cls):
        query = 'SELECT * FROM members;'
        result = connectToMySQL(db).query_db(query)
        return result


    @classmethod
    def get_member_by_email(cls,data):
        query = 'SELECT * FROM members WHERE email = %(email)s;'
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])





    @staticmethod
    def validate_member_registration(member):
        is_valid = True
        result = Member.get_member_by_email(member)
        if result:
            flash('Invalid Email/Password', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(member['email']):
            flash('Invalid Email/Password', 'register')
            is_valid = False
        if len(member['first_name']) < 3:
            flash('First Name must be at least 2 characters.', 'register')
            is_valid = False
        if len(member['last_name']) < 3:
            flash('Last Name must be at least 2 characters.', 'register')
            is_valid = False
        if member['role'] == "choose_an_option":
            flash('Role cannot be blank.', 'register')
            is_valid = False
        if member['voice_part'] == "choose_an_option":
            flash('Voice Part cannot be blank.', 'register')
            is_valid = False
        if len(member['phone']) < 10:
            flash('Invalid Phone Number.', 'register')
            is_valid = False
        if len(member['password']) < 8:
            flash('Password must be at least 8 characters.', 'register')
            is_valid = False
        if member['password'] != member['confirm_password']:
            flash('Passwords do not match!', 'register')
            is_valid = False
        return is_valid



    @staticmethod
    def validate_songs(song):
        is_valid = True
        if len(song['title']) < 3:
            flash('Title must be at least 3 characters.', 'suggestions')
            is_valid = False
        if len(song['artist']) == 0:
            flash('"Artist" cannot be blank.', 'suggestions')
            is_valid = False
        if len(song['link']) == 0:
            flash('"YouTube Link" cannot be blank.', 'suggestions')
            is_valid = False
        return is_valid




    @staticmethod
    def validate_songs(song):
        is_valid = True
        if len(song['title']) < 3:
            flash('Title must be at least 3 characters.', 'edit')
            is_valid = False
        if len(song['artist']) == 0:
            flash('"Artist" cannot be blank.', 'edit')
            is_valid = False
        if len(song['link']) == 0:
            flash('"YouTube Link" cannot be blank.', 'edit')
            is_valid = False
        return is_valid





    @staticmethod
    def validate_contact_request(contact):
        is_valid = True
        if len(contact['first_name']) == 0:
            flash('First name must not be blank.', 'contact')
            is_valid = False
        if len(contact['last_name']) == 0:
            flash('Last name must not be blank.', 'contact')
            is_valid = False
        if not EMAIL_REGEX.match(contact['email']):
            flash('Invalid Email/Password', 'contact')
            is_valid = False
        if len(contact['reason']) == 0:
            flash('Reason for contacting cannot be blank.', 'contact')
            is_valid = False
        if contact['how'] == "choose_an_option":
            flash('Please tell us how you heard about us.', 'contact')
            is_valid = False
        return is_valid