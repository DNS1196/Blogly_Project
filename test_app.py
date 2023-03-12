
from unittest import TestCase
# from flask import current_app
from app import app
from models import db, User, Post


class usersTestcases(TestCase):
    """Tests for Blogly"""
    @classmethod
    def setUpClass(cls):
        """Set up the test database."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = False
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        
        with app.app_context():
            db.drop_all()
            db.create_all()
    
    
    def setUp(self):
       """Add sample User"""
           
       with app.app_context():
            Post.query.delete()
            User.query.delete()
    
            user = User(first_name = 'Test', last_name= 'User')
            db.session.add(user)
            post = Post(title="Test Post", content="Test Content", user=user)
            db.session.add(post)
            db.session.commit()
    
            self.user_id = user.id
            self.user = user
            self.post_id= post.id
       
    def tearDown(self):
       """Clean up any fouled transaction."""
       with app.app_context():
            db.session.rollback()
       
        
    def test_home(self):
        """Test home page redirects to user list page"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Blogly Recent Posts', html)
        
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
            
    def test_add_post_form(self):
        """Test new post form displays"""
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}/posts/new")
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Add post', html)
            
    def test_add_post(self):
        """Test adding a new post"""

        with app.test_client() as client:
            response = client.post(f"/users/{self.user_id}/posts/new", data={
                'title': 'Test Post 2',
                'content': 'Test Content 2'
            }, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Test Post 2", html)
            
    def test_post_details(self):
        """Test post details route"""

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Test Post</h1>", html)