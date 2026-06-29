from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
import uvicorn
import hashlib
import aiosqlite
import asyncio
from fastapi.staticfiles import StaticFiles
from jose import jwt

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static",StaticFiles(directory="static"),name="static")
SECRET_KEY = "6478bd6bv6d94876dbvfbn06cvn26-54nc222n45c82c4525c-,k526bnc56"

async def init_db():
	async with aiosqlite.connect("ToDo.db") as db:
		await db.execute('''CREATE TABLE IF NOT EXISTS users(
			id INTEGER PRIMARY KEY,
			login UNIQUE,
			password TEXT)''')
		await db.commit()
	return("INFO: выполнен вход в базу данных!")

async def get_token(request):
	retrun True


class Test():
	async def registr_test(login:str,password:str):
		password_h = hashlib.sha256(password.encode()).hexdigest()
		try:
			async with aiosqlite.connect("ToDo.db") as db:
				await db.execute('''INSERT INTO users(login,password) 
					VALUES (?,?)''',(login,password_h,))
				await db.commit()
				return True
		except aiosqlite.IntegrityError:
			return False

	async def login_test(login:str,password:str):
				password_h = hashlib.sha256(password.encode()).hexdigest()
				async with aiosqlite.connect("ToDo.db") as db:
					async with db.execute("SELECT login FROM users WHERE login = ?",(login,)) as log:
						login_true = await log.fetchone()
						if not login_true:
							return False
						async with db.execute("SELECT password FROM users WHERE password = ?",(password_h,)) as pas_cur:
							password_true = await pas_cur.fetchone()
							if not password_true:
								return False
				return True

@app.get("/",response_class=HTMLResponse)
async def home_page(request:Request):
	template = templates.get_template("home.html")
	content = template.render({"request":request})
	return HTMLResponse(content=content)

@app.get("/registr",response_class=HTMLResponse)
async def get_reg_from(request:Request):
	template = templates.get_template("reg.html")
	content = template.render({"request":request})
	return HTMLResponse(content=content)

@app.post("/registration",response_class=HTMLResponse)
async def reg(request:Request,
	login:str=Form(...),
	password:str=Form(...)):
		password_h = hashlib.sha256(password.encode()).hexdigest()
		try:
			async with aiosqlite.connect("ToDo.db") as db:
				await db.execute('''INSERT INTO users(login,password) 
					VALUES (?,?)''',(login,password_h,))
				await db.commit()
			return RedirectResponse(url="/SignIn",status_code=303)
		except aiosqlite.IntegrityError:
			template = templates.get_template("error.html")
			content = template.render({"request":request,
				"status_code":402,
				"detail":"аккаунт с данным логином уже существует"})
			return HTMLResponse(content=content)

@app.get("/SignIn",response_class=HTMLResponse)
async def SignIn_form(request:Request):
	template = templates.get_template("SignIn.html")
	content = template.render({"request":request})
	return HTMLResponse(content=content)

@app.post("/login",response_class=HTMLResponse)
async def signIIn(request:Request,
	login:str=Form(...),
	password:str=Form(...)):
		password_h = hashlib.sha256(password.encode()).hexdigest()
		async with aiosqlite.connect("ToDo.db") as db:
			async with db.execute("SELECT login FROM users WHERE login = ?",(login,)) as log:
				login_true = await log.fetchone()
				if not login_true:
					template = templates.get_template("error.html")
					content = template.render({"request":request,
						"status_code":402,
						"detail":"данный аккаунт не существует"})
					return HTMLResponse(content=content)
				async with db.execute("SELECT password FROM users WHERE password = ?",(password_h,)) as pas_cur:
					password_true = await pas_cur.fetchone()
					if not password_true:
						template = templates.get_template("error.html")
						content = template.render({"request":request,
							"status_code":402,
							"detail":"неверный пороль"})
						return HTMLResponse(content=content)
		token = jwt.encode({"login":login},"SECRET_KEY",algorithm="HS256")
		response = RedirectResponse(url="/",status_code=303)
		response.set_cookie(key="access_token",value=token,httponly=True)
		return response


if __name__ == "__main__":
	asyncio.run(init_db())
	uvicorn.run(app)
	





