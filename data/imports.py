from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from password_validator import PasswordValidator
from validate_email import validate_email
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
import itsdangerous as itsdangerous
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
