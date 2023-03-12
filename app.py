"""Blogly application."""

from flask import Flask,  request, render_template,  redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretSauce123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

default_image_url = 'https://tinyurl.com/pr94wycc'

@app.route('/')
def home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/users/new', methods=["GET"])
def add_user_form():
    return render_template('user_form.html')

@app.route('/users/new', methods=["POST"])
def handle_add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url or None)
    
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit',methods= ["GET"])
def user_details_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)
    
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_user_detail_edit(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] if request.form['image_url'] else default_image_url

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted")
    return redirect('/users')

#############################################################

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_post_form(user_id):
    user = User.query.get_or_404(user_id)
    new_post= Post(title=request.form['title'],
                   content= request.form['content'],
                   user= user)
    db.session.add(new_post)
    db.session.commit()
    flash(f"New post '{new_post.title}' added")
    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    post= Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def post_details_edit(post_id):
    post= Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_detail_edit(post_id):
    post= Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited")
    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post= Post.query.get_or_404(post_id) 
    
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted")
    return redirect(f'/users/{post.user_id}')