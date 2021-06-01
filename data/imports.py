from password_validator import PasswordValidator
from validate_email import validate_email

from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.templating import Jinja2Templates

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib