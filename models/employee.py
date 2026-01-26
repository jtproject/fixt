from sqlmodel import SQLModel, Field

class Employee(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    hire_date: str  # or datetime