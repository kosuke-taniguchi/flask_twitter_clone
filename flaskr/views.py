from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flaskr.forms import SignupForm, LoginForm, PostForm, SearchPostForm, CommentForm
from flaskr.models import User, Post, Comment, PostLike
from flask_login import login_user, logout_user, login_required, current_user
import datetime
from flaskr import db


bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/')
@bp.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=15)
    trend_posts = Post.query.order_by(Post.like_count.desc()).limit(6)
    return render_template('home.html', posts=posts, trend_posts=trend_posts)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(
          username,
          email,
          password
        )
        user.add_user()
        return redirect(url_for('app.login'))
    return render_template('signup.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        user = User.select_user_by_email(email)
        if user and user.validate_password(password):
            login_user(user)
            next = request.args.get('next')
            if not next:
                next = url_for('app.home')
            return redirect(next)
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.home'))

@bp.route('/post', methods=['GET','POST'])
@login_required
def post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        author = form.author.data
        date_posted = datetime.datetime.now()
        content = form.content.data
        user_id = form.user_id.data
        like_count = 0
        post = Post(
            author,
            date_posted,
            content,
            user_id,
            like_count
        )
        post.add_post()
        return redirect(url_for('app.home'))
    return render_template('post.html', form=form)

@bp.route('/user_profile/<int:user_id>')
def user_profile(user_id):
    user = User.query.filter(User.id==user_id).first()
    # posts = Post.query.filter(Post.user_id==user_id).all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.user_id==user_id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template('user_profile.html', user=user, posts=posts)

@bp.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    post = Post.query.filter(Post.id==post_id).first()
    comments = Comment.query.filter(Comment.comment_id==post_id).all()
    return render_template('post_detail.html', post=post, comments=comments)

@bp.route('/likes/<int:post_id>/<action>')
@login_required
def likes(post_id, action):
    post = Post.query.filter(Post.id==post_id).first()
    if action == 'like':
        current_user.like_post(post)
        post.like_count += 1
        db.session.commit()
    elif action == 'unlike':
        current_user.unlike_post(post)
        post.like_count -= 1
        db.session.commit()
    return redirect(url_for('app.post_detail', post_id=post_id))

@bp.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.filter(Post.id==post_id).first()
    post.delete_post()
    return redirect(url_for('app.home'))

@bp.route('/search_posts', methods=['GET', 'POST'])
def search_posts():
    form = SearchPostForm(request.form)
    posts = None
    if request.method == 'POST' and form.validate():
        posts_contents = form.posts_contents.data
        posts = Post.search_by_contents(posts_contents)
    return render_template('search_posts.html', form=form, posts=posts)

@bp.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        author = form.author.data
        content = form.content.data
        date_posted = datetime.datetime.now()
        comment_id = form.comment_id.data
        comment = Comment(
            author,
            content,
            date_posted,
            comment_id
        )
        comment.add_comment()
        return redirect(url_for('app.post_detail', post_id=post_id))
    return render_template('comment.html', form=form, post_id=post_id)

@bp.route('/comment_delete/<int:post_id>/<int:comment_id>')
@login_required
def comment_delete(post_id, comment_id):
    comment = Comment.query.filter(Comment.id==comment_id).first()
    comment.delete_comment()
    post = Post.query.filter(Post.id==post_id).first()
    post_id = post.id
    return redirect(url_for('app.post_detail', post_id=post_id))

@bp.route('/liked_posts/<int:user_id>')
@login_required
def liked_posts(user_id):
    post_likes = PostLike.query.filter(PostLike.user_id==user_id).all()
    liked_posts = []
    page = request.args.get('page', 1, type=int)
    for post_like in post_likes:
        liked_post = Post.query.filter(Post.id==post_like.post_id).first()
        liked_posts.append(liked_post)
    return render_template('liked_posts.html', liked_posts=liked_posts)