"""Add performance indexes on foreign keys and user email

Индексы добавлены для ускорения наиболее частых запросов (ЛР5):
 - task.column_id      — выборка задач по колонке/проекту (get_all_tasks);
 - task_log.task_id    — выборка журнала по задаче (get_all_task_logs);
 - column.project_id   — выборка колонок по проекту (get_all_columns);
 - user.email          — поиск пользователя при логине (get_user_by_email),
                         индекс уникальный, т.к. email не должен повторяться.

Revision ID: a1c2e3f40001
Revises: 2b5810ae639d
Create Date: 2026-05-22 23:30:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a1c2e3f40001'
down_revision: Union[str, None] = '2b5810ae639d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index('ix_task_column_id', 'task', ['column_id'])
    op.create_index('ix_task_log_task_id', 'task_log', ['task_id'])
    op.create_index('ix_column_project_id', 'column', ['project_id'])
    op.create_index('ix_user_email', 'user', ['email'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_column_project_id', table_name='column')
    op.drop_index('ix_task_log_task_id', table_name='task_log')
    op.drop_index('ix_task_column_id', table_name='task')
