"""first migrate

Revision ID: 01db458591bc
Revises: 
Create Date: 2021-02-19 11:09:47.107960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01db458591bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('date_posted', sa.String(), nullable=True),
    sa.Column('content', sa.String(length=600), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('like_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_author'), 'posts', ['author'], unique=False)
    op.create_index(op.f('ix_posts_content'), 'posts', ['content'], unique=False)
    op.create_index(op.f('ix_posts_date_posted'), 'posts', ['date_posted'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('post_like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_like')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_posts_date_posted'), table_name='posts')
    op.drop_index(op.f('ix_posts_content'), table_name='posts')
    op.drop_index(op.f('ix_posts_author'), table_name='posts')
    op.drop_table('posts')
    # ### end Alembic commands ###
