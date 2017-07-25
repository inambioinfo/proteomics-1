"""rename project columns

Revision ID: 2f3ff3f82630
Revises: d31b0fd1533a
Create Date: 2017-07-25 16:42:05.486710

"""

# revision identifiers, used by Alembic.
revision = '2f3ff3f82630'
down_revision = 'd31b0fd1533a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('cell_or_tissue_type', sa.String(length=32), nullable=True))
    op.add_column('project', sa.Column('project_id', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'project', ['project_id'])
    op.drop_column('project', 'cell_tissue_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('cell_tissue_type', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'project', type_='unique')
    op.drop_column('project', 'project_id')
    op.drop_column('project', 'cell_or_tissue_type')
    # ### end Alembic commands ###