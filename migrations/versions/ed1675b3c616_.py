"""empty message

Revision ID: ed1675b3c616
Revises: c26b00840856
Create Date: 2024-05-14 15:36:35.066103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed1675b3c616'
down_revision = 'c26b00840856'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Placeholder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('madlib_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['madlib_id'], ['Madlib.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Madlib', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Madlib', schema=None) as batch_op:
        batch_op.drop_column('id')

    op.drop_table('Placeholder')
    # ### end Alembic commands ###
