"""auto allot project lead

Revision ID: eb832bb33e83
Revises: 7c2263fd67e9
Create Date: 2026-11-04 18:42:06.952763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb832bb33e83'
down_revision: Union[str, Sequence[str], None] = '7c2263fd67e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
from alembic import op


def upgrade() -> None:

    # Create trigger function first
    op.execute("""
        CREATE OR REPLACE FUNCTION public.auto_allot_project_lead()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS $$
        BEGIN
            INSERT INTO public.project_allotments (
                project_id,
                employee_id
            )
            VALUES (
                NEW.project_id,
                NEW.lead_id
            );

            RETURN NEW;
        END;
        $$;
    """)

    # Create trigger after function
    op.execute("""
        CREATE TRIGGER trg_auto_allot_project_lead
        AFTER INSERT ON public.projects
        FOR EACH ROW
        EXECUTE FUNCTION public.auto_allot_project_lead();
    """)


def downgrade() -> None:

    op.execute("""
        DROP TRIGGER IF EXISTS trg_auto_allot_project_lead
        ON public.projects;
    """)

    op.execute("""
        DROP FUNCTION IF EXISTS public.auto_allot_project_lead();
    """)