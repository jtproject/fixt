from sqlmodel import SQLModel, Field

class Customer (SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    bill_to: str
    phone: int
    email: str