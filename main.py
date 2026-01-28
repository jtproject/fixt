from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import Optional
import jwt

from db import engine, init_db
from models import model_register, User

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')
security = HTTPBearer()

@app.on_event('startup')
def on_startup ():
	init_db()

def get_session ():
	with Session(engine) as session:
		yield session

def use_model (name):
	return model_register[name]

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
	token = credentials.credentials
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		user_id: int = payload.get("sub")
		if user_id is None:
			raise HTTPException(status_code=401, detail="Invalid token")
		return user_id
	except jwt.ExpiredSignatureError:
		raise HTTPException(status_code=401, detail="Token expired")
	except jwt.InvalidTokenError:
		raise HTTPException(status_code=401, detail="Invalid token")

@app.get('/', response_class=HTMLResponse)
def start_app (request: Request, session: Session = Depends(get_session)):
	return templates.TemplateResponse('base.html', { 'request': request })

@app.post('/api/login', response_class=JSONResponse)
async def login(request: Request, session: Session = Depends(get_session)):
	body = await request.json()
	username = body.get('username')
	password = body.get('password')
	
	if not username or not password:
		raise HTTPException(status_code=400, detail="Username and password required")
	
	# Query user by email or name
	user = session.exec(select(User).where((User.email == username) | (User.name == username))).first()
	
	if not user or not user.verify_password(password):
		raise HTTPException(status_code=401, detail="Invalid credentials")
	
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.id, "email": user.email},
		expires_delta=access_token_expires
	)
	
	return JSONResponse(
		content={"access_token": access_token, "token_type": "bearer", "user": user.model_dump()},
		status_code=200
	)

@app.post('/api/logout', response_class=JSONResponse)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
	# In a production app, you might want to blacklist the token
	return JSONResponse(content={"message": "Logged out successfully"}, status_code=200)

@app.get('/api/me', response_class=JSONResponse)
def get_current_user(user_id: int = Depends(verify_token), session: Session = Depends(get_session)):
	user = session.get(User, user_id)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	return JSONResponse(content=user.model_dump(), status_code=200)

@app.get('/api/{model_name}', response_class=JSONResponse)
def read_all (model_name: str, session: Session = Depends(get_session)):
	model = use_model(model_name)
	data = session.exec(select(model)).all()
	return JSONResponse(content=[item.model_dump() for item in data], status_code=200)

@app.get('/api/{model_name}/{id}', response_class=JSONResponse)
def read_one (model_name: str, id: int, session: Session = Depends(get_session)):
	model = use_model(model_name)
	instance = session.get(model, id)
	if not instance:
		raise HTTPException(status_code=404, detail="Item not found")
	return JSONResponse(content=instance.model_dump(), status_code=200)

@app.post('/api/{model_name}', response_class=JSONResponse)
async def create_one (model_name: str, request: Request, session: Session = Depends(get_session)):
	model = use_model(model_name)
	body = await request.json()
	try:
		instance = model(**body)
		session.add(instance)
		session.commit()
		session.refresh(instance)
		return JSONResponse(content=instance.model_dump(), status_code=201)
	except Exception as e:
		session.rollback()
		raise HTTPException(status_code=400, detail=str(e))

@app.put('/api/{model_name}/{id}', response_class=JSONResponse)
async def update_one (model_name: str, id: int, request: Request, session: Session = Depends(get_session)):
	model = use_model(model_name)
	instance = session.get(model, id)
	if not instance:
		raise HTTPException(status_code=404, detail="Item not found")
	body = await request.json()
	try:
		for key, value in body.items():
			if hasattr(instance, key):
				setattr(instance, key, value)
		session.commit()
		session.refresh(instance)
		return JSONResponse(content=instance.model_dump(), status_code=200)
	except Exception as e:
		session.rollback()
		raise HTTPException(status_code=400, detail=str(e))

@app.delete('/api/{model_name}/{id}', response_class=JSONResponse)
def delete_one (model_name: str, id: int, session: Session = Depends(get_session)):
	model = use_model(model_name)
	instance = session.get(model, id)
	if not instance:
		raise HTTPException(status_code=404, detail="Item not found")
	try:
		session.delete(instance)
		session.commit()
		return JSONResponse(content={"deleted": id}, status_code=200)
	except Exception as e:
		session.rollback()
		raise HTTPException(status_code=400, detail=str(e))