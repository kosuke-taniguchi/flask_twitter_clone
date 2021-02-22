from flaskr import db
from flaskr import login_manager
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True)
    email = db.Column(db.String(), unique=True, index=True)
    password = db.Column(db.String(64))
    likes = db.relationship('PostLike', backref='posts', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def add_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def select_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(), index=True)
    date_posted = db.Column(db.String(), index=True)
    content = db.Column(db.String(600), index=True)
    user_id = db.Column(db.Integer)
    like_count = db.Column(db.Integer)

    def __init__(self, author, date_posted, content, user_id, like_count):
        self.author = author
        self.date_posted = date_posted.strftime('%Y年%m月%d日 %H:%M:%S')
        self.content = content
        self.user_id = user_id
        self.like_count = like_count

    def add_post(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    def delete_post(self):
        with db.session.begin(subtransactions=True):
            db.session.delete(self)
        db.session.commit()

    @classmethod
    def search_by_contents(cls, posts_contents):
        return cls.query.filter(
            cls.content.like(f'%{posts_contents}%'),
        ).with_entities(
            cls.id, cls.author, cls.date_posted, cls.content, cls.user_id, cls.like_count
        ).all()


class PostLike(db.Model):

    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(), index=True)
    content = db.Column(db.String(600), index=True)
    date_posted = db.Column(db.String(), index=True)
    comment_id = db.Column(db.Integer)

    def __init__(self, author, content, date_posted, comment_id):
        self.author = author
        self.content = content
        self.date_posted = date_posted.strftime('%Y年%m月%d日 %H:%M:%S')
        self.comment_id = comment_id

    def add_comment(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        with db.session.begin(subtransactions=True):
            db.session.delete(self)
        db.session.commit()