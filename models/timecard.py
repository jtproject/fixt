from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON

class TimeCard(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    job_id: int = Field(foreign_key="job.id")
    hours: float
    hourly_rate: float = Field(default=0.0)
    date: str  # or use datetime.date
    description: str = Field(default="")
    auxiliary_payments: list[dict] = Field(default_factory=list, sa_column=Column(JSON))  # list of {'type': str, 'amount': float}