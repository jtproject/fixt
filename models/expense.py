from sqlmodel import SQLModel, Field

class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timecard_id: int = Field(foreign_key="timecard.id")
    type: str  # 'expense', 'health_insurance', 'bonus', etc.
    amount: float
    description: str = Field(default="")
    date_incurred: str  # or datetime.date