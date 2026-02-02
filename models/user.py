from sqlmodel import SQLModel, Field
from passlib.context import CryptContext
from sqlalchemy import Column, JSON

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class User(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	first_name: str
	last_name: str
	username: str
	email: str
	phone: int
	password_hash: str | None = None
	companies: list[str] = Field(default_factory=list, sa_column=Column(JSON))
	
	def set_password(self, password: str) -> None:
		self.password_hash = pwd_context.hash(password)
	
	def verify_password(self, password: str) -> bool:
		return pwd_context.verify(password, self.password_hash or "")