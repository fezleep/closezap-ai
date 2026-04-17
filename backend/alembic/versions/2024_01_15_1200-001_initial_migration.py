"""Initial migration - Create leads table

Revision ID: 001
Revises:
Create Date: 2024-01-15 12:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create leads table
    op.create_table(
        'leads',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('interest', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('new', 'engaged', 'closed', name='leadstatus'), nullable=False),
        sa.Column('last_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_contact_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index(op.f('ix_leads_id'), 'leads', ['id'], unique=False)
    op.create_index(op.f('ix_leads_name'), 'leads', ['name'], unique=False)
    op.create_index(op.f('ix_leads_phone'), 'leads', ['phone'], unique=True)
    op.create_index(op.f('ix_leads_status'), 'leads', ['status'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_leads_status'), table_name='leads')
    op.drop_index(op.f('ix_leads_phone'), table_name='leads')
    op.drop_index(op.f('ix_leads_name'), table_name='leads')
    op.drop_index(op.f('ix_leads_id'), table_name='leads')

    # Drop table
    op.drop_table('leads')

    # Drop enum type
    op.execute("DROP TYPE IF EXISTS leadstatus")