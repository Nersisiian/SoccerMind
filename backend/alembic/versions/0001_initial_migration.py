"""initial migration

Revision ID: 0001
Revises:
Create Date: 2025-03-01 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('referral_code', sa.String(), unique=True),
    )
    op.create_table('teams',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('country', sa.String()),
        sa.Column('external_id', sa.String(), unique=True),
    )
    op.create_table('players',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('external_id', sa.String(), unique=True),
    )
    op.create_table('competitions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('country', sa.String()),
        sa.Column('season', sa.String()),
        sa.Column('external_id', sa.String(), unique=True),
    )
    op.create_table('matches',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('home_team_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('teams.id'), nullable=False),
        sa.Column('away_team_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('teams.id'), nullable=False),
        sa.Column('competition_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('competitions.id')),
        sa.Column('kickoff', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(), server_default='scheduled'),
        sa.Column('home_score', sa.Integer()),
        sa.Column('away_score', sa.Integer()),
        sa.Column('external_id', sa.String(), unique=True),
    )
    op.create_table('odds',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('match_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('matches.id'), nullable=False),
        sa.Column('bookmaker', sa.String()),
        sa.Column('market', sa.String()),
        sa.Column('home_win', sa.Float()),
        sa.Column('draw', sa.Float()),
        sa.Column('away_win', sa.Float()),
        sa.Column('over', sa.Float()),
        sa.Column('under', sa.Float()),
        sa.Column('btts_yes', sa.Float()),
        sa.Column('btts_no', sa.Float()),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table('predictions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('match_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('matches.id'), nullable=False),
        sa.Column('model_version', sa.String()),
        sa.Column('predicted_home_win', sa.Float()),
        sa.Column('predicted_draw', sa.Float()),
        sa.Column('predicted_away_win', sa.Float()),
        sa.Column('predicted_over_2_5', sa.Float()),
        sa.Column('predicted_btts', sa.Float()),
        sa.Column('predicted_score', postgresql.JSONB()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table('injuries',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('player_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('players.id')),
        sa.Column('team_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('teams.id')),
        sa.Column('match_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('matches.id')),
        sa.Column('description', sa.String()),
        sa.Column('status', sa.String()),
        sa.Column('expected_return', sa.Date()),
    )
    op.create_table('subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('plan_id', sa.String()),
        sa.Column('status', sa.String(), server_default='active'),
        sa.Column('current_period_start', sa.DateTime(timezone=True)),
        sa.Column('current_period_end', sa.DateTime(timezone=True)),
        sa.Column('stripe_subscription_id', sa.String(), unique=True),
    )
    op.create_table('payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('amount', sa.Float()),
        sa.Column('currency', sa.String()),
        sa.Column('payment_method', sa.String()),
        sa.Column('status', sa.String()),
        sa.Column('stripe_payment_intent_id', sa.String(), unique=True),
        sa.Column('telegram_payload', sa.String()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table('referrals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('referrer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('referred_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('reward_credited', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

def downgrade() -> None:
    op.drop_table('referrals')
    op.drop_table('payments')
    op.drop_table('subscriptions')
    op.drop_table('injuries')
    op.drop_table('predictions')
    op.drop_table('odds')
    op.drop_table('matches')
    op.drop_table('competitions')
    op.drop_table('players')
    op.drop_table('teams')
    op.drop_table('users')