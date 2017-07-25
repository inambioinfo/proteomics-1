"""update project columns

Revision ID: d31b0fd1533a
Revises: 58d661e1c431
Create Date: 2017-07-25 12:12:14.141011

"""

# revision identifiers, used by Alembic.
revision = 'd31b0fd1533a'
down_revision = '58d661e1c431'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('cell_tissue_type', sa.String(length=32), nullable=True))
    op.add_column('project', sa.Column('experimental_details', sa.String(length=1024), nullable=True))
    op.add_column('project', sa.Column('instrument', sa.String(length=32), nullable=True))
    op.add_column('project', sa.Column('researcher', sa.String(length=64), nullable=True))
    op.add_column('project', sa.Column('species', sa.String(length=32), nullable=True))
    op.drop_column('project', 'source')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('source', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.drop_column('project', 'species')
    op.drop_column('project', 'researcher')
    op.drop_column('project', 'instrument')
    op.drop_column('project', 'experimental_details')
    op.drop_column('project', 'cell_tissue_type')
    # ### end Alembic commands ###
