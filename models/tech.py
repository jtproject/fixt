from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON

class Tech(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    specializations: list[str] = Field(default_factory=list, sa_column=Column(JSON))