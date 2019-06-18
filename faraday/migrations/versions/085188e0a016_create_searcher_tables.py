"""create searcher's tables

Revision ID: 085188e0a016
Revises: 2db31733fb78
Create Date: 2019-06-18 18:07:41.834191+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '085188e0a016'
down_revision = '2db31733fb78'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'rule',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('model', sa.String, nullable=False),
        sa.Column('parent', sa.String, nullable=True),
        sa.Column('fields', sa.JSON, nullable=True),
        sa.Column('object', sa.JSON, nullable=False)
    )

    op.create_table(
        'action',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=True),
        sa.Column('command', sa.String, nullable=False),
        sa.Column('field', sa.String, nullable=True),
        sa.Column('value', sa.String, nullable=True)
    )

    op.create_table(
        'rule_action',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('rule_id', sa.Integer, primary_key=True),
        sa.Column('action_id', sa.Integer, primary_key=True)
    )

    op.create_foreign_key(
        'rule_action_rule_id_fkey',
        'rule_action',
        'rule', ['rule_id'], ['id']
    )

    op.create_foreign_key(
        'rule_action_action_id_fkey',
        'rule_action',
        'action', ['action_id'], ['id']
    )

    op.create_table(
        'condition',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('field', sa.String, nullable=False),
        sa.Column('value', sa.String, nullable=False),
        sa.Column('operator', sa.String, nullable=True),
        sa.Column('rule_id', sa.Integer, nullable=False)
    )

    op.create_foreign_key(
        'condition_rule_id_fkey',
        'condition',
        'rule', ['rule_id'], ['id']
    )

    op.create_table(
        'rule_execution',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('start', sa.DateTime, nullable=True),
        sa.Column('end', sa.DateTime, nullable=True),
        sa.Column('rule_id', sa.Integer, nullable=False)
    )

    op.create_foreign_key(
        'rule_execution_rule_id_fkey',
        'rule_execution',
        'rule', ['rule_id'], ['id']
    )


def downgrade():
    op.drop_table('rule_execution')
    op.drop_table('condition')
    op.drop_table('rule_action')
    op.drop_table('action')
    op.drop_table('rule')
