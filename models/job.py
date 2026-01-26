from sqlmodel import SQLModel, Field

class Job (SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	customer_id: int = Field(foreign_key="customer.id")
	description: str
	status: str = Field(default="pending")  # e.g., 'pending', 'in_progress', 'completed'
	go_to: str
	contact: str  # changed to str, assuming phone or name
	callback: str
	details: str
	notes: str  # changed to str, as list might not serialize well
	bonus_eligible: bool = Field(default=False)
	bonus_amount: float | None = Field(default=None)