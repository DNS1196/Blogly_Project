"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_image_url = 'https://tinyurl.com/pr94wycc'



class User(db.Model):
    """Users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text,nullable=False, default= default_image_url)
    posts = db.relationship('Post', backref="user", cascade= 'all, delete-orphan')
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
   
class Post(db.Model):
    """Blog posts"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer,
                   primary_key = True, 
                   autoincrement = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable =False,
                           default = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    
    @property
    def friendly_date(self):
        return self.created_at.strftime("%B %d, %Y at %I:%M %p")

   
def connect_db(app):
    db.app = app
    db.init_app(app)