from data.imports import *
from data.classes import *
from data.cparams import *


class Page:
    main_page = open("./data/templates/index.html", 'r')
    register_page = open("./data/templates/register.html", 'r')
    login_page = open("./data/templates/login.html", 'r')
    validation_page = open("./data/templates/validation.html", 'r')


schema = PasswordValidator()
schema.min(8).max(100)\
    .has().uppercase().has().lowercase()\
    .has().digits().has().no().spaces()

app = FastAPI()
manager = LoginManager(SECRET, TOKEN_URL)
pages = Page
confirmation_tool = itsdangerous.URLSafeTimedSerializer(SECRET)
# Somehow wrap this up


@app.get("/")
async def index():
    return HTMLResponse(content=pages.main_page.read())


@app.get("/log")
async def index():
    return HTMLResponse(content=pages.login_page.read())


@app.get("/reg")
async def index():
    return HTMLResponse(content=pages.register_page.read())


@app.get("/reg/validate")
async def index():
    return HTMLResponse(content=pages.validation_page.read())


@manager.user_loader
async def get_user(email: str):
    return DB["users"].get(email)


@app.post("/auth/register")
async def register(user: UserCheck):
    if user.email in DB["users"]:
        raise HTTPException(status_code=400, detail="This email already exists")
    if not schema.validate(user.password1):
        raise HTTPException(status_code=400, detail="The password is too weak")
    if user.password1 != user.password2:
        raise HTTPException(status_code=400, detail="The passwords differ")
    if not validate_email(user.email, verify=True):
        raise HTTPException(status_code=400, detail="Invalid email")
    else:
        db_user = User(**user.dict(), id=uuid.uuid4())
        DB["users"][db_user.email] = db_user
        return {"detail": "Success"}


@app.post("/auth/validate")
async def validate(user: UserCheck):
    # FINISH
    code = None
    sender = await MIMEMultipart('alternative')
    sender['Subject'] = "Email Validation"
    sender['From'] = email_from
    sender['To'] = user.email
    html = f"""\
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               How are you?<br>
               Here is the {code} you wanted.
            </p>
          </body>
        </html>
        """
    part2 = await MIMEText(html, 'html')
    sender.attach(part2)
    step = await smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    step.sendmail(email_from, user.email, sender.as_string())
    step.quit()
    pass




@app.post(TOKEN_URL)
async def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    user = await get_user(email)
    if not user:
        raise InvalidCredentialsException
    elif password != user.password1:
        raise InvalidCredentialsException

    access_token = await manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get("/private")
def private_route(user=Depends(manager)):
    return {"detail": f"Welcome {user.email}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app")
