
from datetime import date, datetime,timedelta
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


ProjectStatus = Literal[
    "planning",
    "started",
    "pending",
    "completed",
    "dropped",
]


class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_name: str = Field(
        min_length=3,
        max_length=100,
    )
    project_description: str | None = Field(
        default=None,
        max_length=500,
    )
    lead_id: int = Field(gt=0)
    start_date: date
    expected_end_date: date

    
    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        minimum_end_date = self.start_date + timedelta(days=7)

        if self.expected_end_date < minimum_end_date:
            raise ValueError(
                "Project duration must be at least 7 days"
            )

        return self



class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )
    project_description: str | None = Field(
        default=None,
        max_length=500,
    )
    start_date: date | None = None
    expected_end_date: date | None = None
    status: ProjectStatus | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if (
            self.start_date is not None
            and self.expected_end_date is not None
            and self.expected_end_date
            < self.start_date + timedelta(days=7)
        ):
            raise ValueError(
                "Project duration must be at least 7 days"
            )

        return self


class ProjectLeadUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lead_id: int = Field(gt=0)


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: int
    project_name: str
    project_description: str | None
    lead_id: int
    start_date: date
    expected_end_date: date
    status: ProjectStatus
    created_by: int
    created_at: datetime
    updated_at: datetime


class PaginatedProjectResponse(BaseModel):
    total: int
    page: int
    size: int
    pages: int
    projects: list[ProjectResponse]
