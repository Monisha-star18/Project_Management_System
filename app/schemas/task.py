from datetime import date, datetime
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

TaskStatus = Literal['todo', 'in_progress', 'completed', 'on_hold']
TaskPriority = Literal['low', 'medium', 'high', 'urgent']


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    employee_id: int = Field(gt=0, description='Employee currently allotted to this project')
    task_title: str = Field(min_length=1, max_length=150)
    description: str | None = None
    priority: TaskPriority = 'medium'
    start_date: date
    due_date: date

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.due_date < self.start_date:
            raise ValueError('due_date must be on or after start_date')
        return self


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    employee_id: int | None = Field(default=None, gt=0)
    task_title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    priority: TaskPriority | None = None
    start_date: date | None = None
    due_date: date | None = None
    remarks: str | None = None


class TaskProgressUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    progress_percentage: int = Field(ge=0, le=100)
    status: TaskStatus | None = None
    remarks: str | None = None

    @model_validator(mode='after')
    def check_progress(self) -> Self:
        if self.status == 'completed' and self.progress_percentage != 100:
            raise ValueError('Completed tasks must have 100% progress')
        if self.status in ('todo', 'in_progress', 'on_hold') and self.progress_percentage == 100:
            raise ValueError('100% progress requires completed status')
        return self


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    task_id: int
    allotment_id: int
    project_id: int
    employee_id: int
    task_title: str
    description: str | None
    assigned_by: int
    priority: TaskPriority
    start_date: date
    due_date: date
    status: TaskStatus
    progress_percentage: int
    remarks: str | None
    created_at: datetime
    updated_at: datetime
