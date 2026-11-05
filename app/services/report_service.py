from app.exceptions.project_exception import ProjectNotFoundError
from app.repositories.interfaces.report_repository_interface import (
    ReportRepositoryInterface,
)


class ReportService:

    def __init__(self, repository: ReportRepositoryInterface):
        self.repository = repository

    async def get_project_report(self, project_id: int):

        project = await self.repository.get_project(project_id)

        if not project:
            raise ProjectNotFoundError()

        total_employees = sum(
            1 for allotment in project.allotments
            if allotment.is_active
        )

        tasks = [
            task
            for allotment in project.allotments
            for task in allotment.tasks
        ]

        total_tasks = len(tasks)

        completed_tasks = sum(
            1 for task in tasks
            if task.status == "completed"
        )

        completion_percentage = (
            round(completed_tasks / total_tasks * 100, 2)
            if total_tasks > 0
            else 0.0
        )

        overall_progress_percentage = (
            round(
                sum(task.progress_percentage or 0 for task in tasks)
                / len(tasks),
                2
            )
            if tasks else 0.0
        )

        return {
            "project": project,
            "total_employees": total_employees,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_percentage": completion_percentage,
            "overall_progress_percentage":overall_progress_percentage,
        }