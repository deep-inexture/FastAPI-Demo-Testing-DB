import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import re
import uuid
from demo_app.repository import emailUtil, messages, emailFormat
from demo_app import models, tokens
from demo_app.hashing import Hash

"""
This File does all validations related stuff for Login, Register, & Forgot Password.
All Database query stuff also takes place here.
"""


def register(request, db: Session):
    """
    Function provides validation and authentication before registering for endpoint.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Fetch key data to fetch values from user
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Registered Data of the user
    """
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=409, detail=messages.Email_exists_409(request.email))
    if not re.fullmatch(r"^[a-z\d]+[\._]?[a-z\d]+[@]\w+[.]\w{2,3}$", request.email):
        raise HTTPException(status_code=401, detail=messages.INVALID_EMAIL_401)
    if request.password != request.confirm_password:
        raise HTTPException(status_code=401, detail=messages.PASSWORD_MISMATCH_401)
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', request.password):
        raise HTTPException(status_code=401, detail=messages.PASSWORD_FORMAT_401)

    new_user = models.User(
        id=1,
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # user_id = db.query(models.User.id).filter(models.User.email == request.email).first()
    # user_wallet = models.MyWallet(user_id=user_id[0])
    # db.add(user_wallet)
    # db.commit()
    # db.refresh(user_wallet)

    return messages.json_status_response(200, "User Registered Successfully")


def login(request, db: Session):
    """
    Check Validation and password along with token to let access to other endpoints.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Fetch data for login requirements
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Access and Refresh Tokens
    """
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.INCORRECT_CREDENTIALS_404)
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.INCORRECT_PASSWORD_404)

    access_token = tokens.create_access_token(data={"sub": user.email})
    refresh_token = tokens.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}


def get_all_user(db):
    """
    Create New Access Token from Refresh Token and replace with Access Token
    Parameters
    ----------------------------------------------------------
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Generates new access token from refresh token
    """
    user = db.query(models.User).all()
    return {'Users': user}
