from app.core.config import get_settings
from app.services.email.base_email import BaseEmail


class TaskAssignedEmail(BaseEmail):

    def __init__(
        self,
        project_id: int,
        task_title: str,
        priority: str,
        start_date,
        due_date,
        lead_name: str,
    ):
        self.project_id = project_id
        self.task_title = task_title
        self.priority = priority
        self.start_date = start_date
        self.due_date = due_date
        self.lead_name = lead_name
        settings = get_settings()

        super().__init__(
            sender_email=settings.team_lead_sender_email
        )

    def build_message(self, full_name: str) -> tuple[str, str]:

        subject = "New Task Assigned"

        body = f"""
                Hello {full_name},

                    A new task has been assigned to you.

                    Project ID: {self.project_id}
                    Task: {self.task_title}
                    Priority: {self.priority}
                    Start Date: {self.start_date}
                    Due Date: {self.due_date}
                    Assigned By: {self.lead_name}

                    Please log in to the Project Management System
                    to view your task and update its progress.

                Regards,
                Project Management Team
                """

        return subject, body