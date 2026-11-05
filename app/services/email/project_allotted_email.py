from app.core.config import get_settings
from app.services.email.base_email import BaseEmail


class ProjectAllottedEmail(BaseEmail):

    def __init__(self, project_id: int, lead_name: str):
        self.project_id = project_id
        self.lead_name = lead_name
        settings = get_settings()

        super().__init__(
            sender_email=settings.team_lead_sender_email
        )

    def build_message(self, full_name: str) -> tuple[str, str]:

        subject = "You have been allotted to a project"

        body = f"""
            Hello {full_name},

                You have been successfully allotted to a project.

                Project ID: {self.project_id}
                Allotted By: {self.lead_name}

                Please log in to the Project Management System
                to view your project details.

            Regards,
            Project Management Team
            """

        return subject, body