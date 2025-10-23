
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'inquiry_types',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('keywords', sa.Text),
    )
    op.create_table(
        'email_templates',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('subject', sa.String(255), nullable=False),
        sa.Column('body_html', sa.Text),
        sa.Column('body_text', sa.Text, nullable=False),
        sa.Column('inquiry_type_id', sa.Integer, sa.ForeignKey('inquiry_types.id')),
    )
    op.create_table(
        'automation_rules',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('trigger_condition', sa.String(255), nullable=False),
        sa.Column('action', sa.String(255), nullable=False),
    )

def downgrade():
    op.drop_table('automation_rules')
    op.drop_table('email_templates')
    op.drop_table('inquiry_types')

