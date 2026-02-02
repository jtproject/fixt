from .customer import Customer
from .user import User
from .admin import Admin
from .tech import Tech
from .job import Job
from .timecard import TimeCard
from .expense import Expense

model_register = {
	'customer': Customer,
	'user': User,
	'user': User,
	'admin': Admin,
	'tech': Tech,
	'job': Job,
	'timecard': TimeCard,
	'expense': Expense,
}