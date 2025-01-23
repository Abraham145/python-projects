"""Add month_year column

Revision ID: a3eccd5e33df
Revises: 
Create Date: 2025-01-20 15:41:30.149169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3eccd5e33df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'month_year', sa.String(length=7), nullable=True, server_default='2025-01'
            )
        )
    # Ensure all rows are updated before setting NOT NULL
    op.execute('UPDATE expense SET month_year = \'2025-01\' WHERE month_year IS NULL')
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.alter_column('month_year', nullable=False, server_default=None)

def downgrade():
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_column('month_year')
