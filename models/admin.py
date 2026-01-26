from sqlmodel import SQLModel, Field

class Admin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    admin_level: str  # e.g., 'senior', 'junior'