"""Initial database

Revision ID: 7c3929047190
Revises:
Create Date: 2021-03-13 13:22:38.768112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c3929047190'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('hostname', sa.String(length=80), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.Column('boilerplate', sa.UnicodeText(), nullable=True),
    sa.Column('resources', sa.UnicodeText(), nullable=True),
    sa.Column('logo_url', sa.String(length=255), nullable=True),
    sa.Column('custom_css', sa.UnicodeText(), nullable=True),
    sa.Column('webpage_url', sa.String(length=255), nullable=True),
    sa.Column('community_url', sa.String(length=255), nullable=True),
    sa.Column('community_embed', sa.UnicodeText(), nullable=True),
    sa.Column('certificate_path', sa.String(length=1024), nullable=True),
    sa.Column('starts_at', sa.DateTime(), nullable=False),
    sa.Column('ends_at', sa.DateTime(), nullable=False),
    sa.Column('is_hidden', sa.Boolean(), nullable=True),
    sa.Column('is_current', sa.Boolean(), nullable=True),
    sa.Column('lock_editing', sa.Boolean(), nullable=True),
    sa.Column('lock_starting', sa.Boolean(), nullable=True),
    sa.Column('lock_resources', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('webpage_url', sa.String(length=128), nullable=True),
    sa.Column('sso_id', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('cardtype', sa.String(length=80), nullable=True),
    sa.Column('carddata', sa.String(length=255), nullable=True),
    sa.Column('my_story', sa.UnicodeText(), nullable=True),
    sa.Column('my_goals', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.Column('logo_color', sa.String(length=7), nullable=True),
    sa.Column('logo_icon', sa.String(length=20), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_visible', sa.Boolean(), nullable=True),
    sa.Column('progress_tip', sa.Integer(), nullable=True),
    sa.Column('source_url', sa.String(length=2048), nullable=True),
    sa.Column('download_url', sa.String(length=2048), nullable=True),
    sa.Column('summary', sa.String(length=140), nullable=True),
    sa.Column('sync_content', sa.UnicodeText(), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users_roles',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('summary', sa.String(length=120), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('source_url', sa.String(length=255), nullable=True),
    sa.Column('webpage_url', sa.String(length=2048), nullable=True),
    sa.Column('is_webembed', sa.Boolean(), nullable=True),
    sa.Column('contact_url', sa.String(length=255), nullable=True),
    sa.Column('autotext_url', sa.String(length=255), nullable=True),
    sa.Column('is_autoupdate', sa.Boolean(), nullable=True),
    sa.Column('autotext', sa.UnicodeText(), nullable=True),
    sa.Column('longtext', sa.UnicodeText(), nullable=False),
    sa.Column('hashtag', sa.String(length=40), nullable=True),
    sa.Column('logo_color', sa.String(length=7), nullable=True),
    sa.Column('logo_icon', sa.String(length=40), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_hidden', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('progress', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Enum('create', 'update', 'star', name='activity_type'), nullable=True),
    sa.Column('action', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('project_progress', sa.Integer(), nullable=True),
    sa.Column('project_score', sa.Integer(), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activities')
    op.drop_table('projects')
    op.drop_table('users_roles')
    op.drop_table('resources')
    op.drop_table('categories')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('events')
    # ### end Alembic commands ###