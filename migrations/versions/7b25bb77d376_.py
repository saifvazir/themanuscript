"""empty message

Revision ID: 7b25bb77d376
Revises: 
Create Date: 2016-12-20 02:38:57.329883

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7b25bb77d376'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Books', sa.Column('Content_Id', sa.String(length=30), nullable=True))
    op.alter_column('Books', 'Author_id',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)
    op.alter_column('Books', 'Coverpage',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('Books', 'Tags',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.drop_column('Books', 'Content_id')
    op.add_column('Users', sa.Column('tokens', sa.String(length=300), nullable=True))
    op.alter_column('Users', 'Date_entry',
               existing_type=mysql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text(u'CURRENT_TIMESTAMP'))
    op.alter_column('Users', 'Genres',
               existing_type=mysql.VARCHAR(length=60),
               nullable=False)
    op.alter_column('Users', 'Languages',
               existing_type=mysql.VARCHAR(length=60),
               nullable=False)
    op.alter_column('Users', 'Password',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)
    op.create_index(op.f('ix_Users_Email_id'), 'Users', ['Email_id'], unique=True)
    op.create_index(op.f('ix_Users_Username'), 'Users', ['Username'], unique=True)
    op.drop_index('User_id', table_name='Users')
    op.drop_column('test', 'password')
    op.drop_column('test', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('name', mysql.VARCHAR(length=20), nullable=False))
    op.add_column('test', sa.Column('password', mysql.VARCHAR(length=20), nullable=False))
    op.create_index('User_id', 'Users', ['User_id'], unique=True)
    op.drop_index(op.f('ix_Users_Username'), table_name='Users')
    op.drop_index(op.f('ix_Users_Email_id'), table_name='Users')
    op.alter_column('Users', 'Password',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)
    op.alter_column('Users', 'Languages',
               existing_type=mysql.VARCHAR(length=60),
               nullable=True)
    op.alter_column('Users', 'Genres',
               existing_type=mysql.VARCHAR(length=60),
               nullable=True)
    op.alter_column('Users', 'Date_entry',
               existing_type=mysql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text(u'CURRENT_TIMESTAMP'))
    op.drop_column('Users', 'tokens')
    op.add_column('Books', sa.Column('Content_id', mysql.VARCHAR(length=30), nullable=False))
    op.alter_column('Books', 'Tags',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('Books', 'Coverpage',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('Books', 'Author_id',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)
    op.drop_column('Books', 'Content_Id')
    # ### end Alembic commands ###