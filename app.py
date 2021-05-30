import uuid

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, UUID4
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import re

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def check(email):
    if re.search(regex, email):
        return True
    else:
        return False


class UserCreate(BaseModel):
    email: str
    password1: str
    password2: str


class User(UserCreate):
    id: UUID4


TOKEN_URL = "/auth/token"
DB = {
    "users": {}
}
app = FastAPI()
manager = LoginManager('very_secret',TOKEN_URL)


@manager.user_loader
def get_user(email: str):
    return DB["users"].get(email)


@app.get("/log")
def index():
    with open("./templates/login.html", 'r') as l:
        return HTMLResponse(content=l.read())


@app.get("/reg")
def index():
    with open("./templates/register.html", 'r') as r:
        return HTMLResponse(content=r.read())


@app.post("/auth/register")
def register(user: UserCreate):
    if user.email in DB["users"]:
        raise HTTPException(status_code=400, detail="A user with this email already exists")
    if user.password1 != user.password2:
        raise HTTPException(status_code=400, detail="The passwords differ")
    if not re.search(regex, user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    else:
        db_user = User(**user.dict(), id=uuid.uuid4())
        DB["users"][db_user.email] = db_user
        return {"detail": "Successfull registered"}


@app.post(TOKEN_URL)
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    user = get_user(email)
    if not user:
        raise InvalidCredentialsException
    elif password != user.password1:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get("/private")
def private_route(user=Depends(manager)):
    return {"detail": f"Welcome {user.email}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app")
