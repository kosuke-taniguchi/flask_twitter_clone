from wtforms import Form
from wtforms.fields import StringField, PasswordField, TextAreaField, SubmitField, HiddenField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email


class SignupForm(Form):
    username = StringField('ユーザー名: ', validators=[DataRequired()])
    email = StringField('メールアドレス: ', validators=[Email(), DataRequired()])
    password = PasswordField('パスワード: ', validators=[DataRequired(), EqualTo('confirm_password', message='パスワードが一致しません')])
    confirm_password = PasswordField('確認用パスワード: ', validators=[DataRequired()])
    submit = SubmitField('登録')


class LoginForm(Form):
    email = StringField('メールアドレス: ', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード: ', validators=[DataRequired()])
    submit = SubmitField('ログイン')


class PostForm(Form):
    author = HiddenField('', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])
    user_id = HiddenField('', validators=[DataRequired()])
    submit = SubmitField('投稿')


class SearchPostForm(Form):
    posts_contents = StringField('', validators=[DataRequired()])
    submit = SubmitField('検索')

class CommentForm(Form):
    author = HiddenField('', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])
    comment_id = HiddenField('', validators=[DataRequired()])
    submit = SubmitField('コメントする')