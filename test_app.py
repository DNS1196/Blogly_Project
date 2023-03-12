from unittest import TestCase
from flask import current_app
from app import app
from models import db, User

# # Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
# app.config['SQLALCHEMY_ECHO'] = False

# # Make Flask errors be real errors, rather than HTML pages with error info
# app.config['TESTING'] = True

# # This is a bit of hack, but don't use Flask DebugToolbar
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



class usersTestcases(TestCase):
    """Tests for Blogly"""
    @classmethod
    def setUpClass(cls):
        """Set up the test database."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        with app.app_context():
            db.drop_all()
            db.create_all()
    
    
    def setUp(self):
       """Add sample User"""
           
       with app.app_context():
            User.query.delete()
    
            user = User(first_name = 'Test', last_name= 'User')
            db.session.add(user)
            db.session.commit()
    
            self.user_id = user.id
            self.user = user
       
    def tearDown(self):
       """Clean up any fouled transaction."""
       with app.app_context():
            db.session.rollback()
       
        
    def test_home(self):
        """Test home page redirects to user list page"""
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/users')
        
    def test_user_list(self):
        """Test user list page displays all users"""
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test User', html)
        
    def test_add_user_form(self):
        """Test add user form page displays"""
        with app.test_client() as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("<h1>Create a user</h1>", html)    
        
    def test_add_user(self):
        """Test adding a new user"""
        
        with app.test_client() as client:
            data = {'first_name': 'John', 'last_name': 'Doe','image_url': "https://tinyurl.com/pr94wycc"}
            response = client.post('/users/new', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('John Doe', html)