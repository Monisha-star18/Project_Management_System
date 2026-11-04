
from app.services.email.base_email import BaseEmail


class EmployeeCreatedEmail(BaseEmail):

    def build_message(self, full_name: str) -> tuple[str, str]:

        subject = "Welcome to The Company "

        body = f"""
                Hello {full_name},

                Welcome to the Company !

                Your employee account has been successfully created.

                You can now access the system using your registered
                credentials.

                You will receive further notifications when:
                - You are allotted to a project.
                - A task is assigned to you.

                Regards,
                Admin Team
                """

        return subject, body
