from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from db import engine, init_db
from models import model_register

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

@app.on_event('startup')
def on_startup ():
	init_db()

def get_session ():
	with Session(engine) as session:
		yield session

def use_model (name):
	return model_register[name]

@app.get('/', response_class=HTMLResponse)
def start_app (request: Request, session: Session = Depends(get_session)):
	return templates.TemplateResponse('base.html', { 'request': request })

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