from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import uuid 
from datetime import datetime 

from werkzeug.security import generate_password_hash, check_password_hash

import secrets 

from flask_login import UserMixin, LoginManager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) 

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy = True)

    def __init__(self, email, username, password, first_name = '', last_name = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username 

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"User {self.email} has been added to the database! Woohoo!"    

class Character (db.Model): 
    id = db.Column(db.String, primary_key = True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    superhero_name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    weakness = db.Column(db.String(100), nullable=True)
    normal_job = db.Column(db.String(150), nullable=True)
    team = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, fname, lname, superhero_name, description, weakness,normal_job,  team, gender, user_token):
        self.id = self.set_id()
        self.fname = fname
        self.lname = lname
        self.superhero_name = superhero_name
        self.description = description
        self.weakness = weakness
        self.normal_job = normal_job
        self.team = team
        self.gender = gender
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Character {self.name} has been added to the database! Woohoo!"    

class CharacterSchema(ma.Schema): 
    class Meta:
        fields = ['id', 'fname', 'lname', 'superhero_name' 'description',  'weakness', 'normal_job', 'team',
                  'gender']
        
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)


