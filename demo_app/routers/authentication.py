from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from demo_app import schemas, database, oauth2
from demo_app.repository import authentication
from dotenv import load_dotenv

"""
It includes Authentication routers for both User & Admin. First Point Router Before Handing any other
routing processes.
"""

load_dotenv()

router = APIRouter(
    tags=["Authentication"]
)
get_db = database.get_db


@router.post('/register')
def registration(request: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Registration User Authentication Requirements
    Call Register function in repository directory to validate credentials & validations.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Fetch key data to fetch values from user
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Registered Data of the user
    """
    return authentication.register(request, db)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    """
    Login Process for both Admin and User.
    Call Login function in repository directory to validate credentials and provide access token.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Fetch data for login requirements
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Access and Refresh Tokens
    """
    return authentication.login(request, db)


@router.get('/get_user')
def new_access_token(db: Session = Depends(get_db)):
    """
    Router to Create New Access Token by taking Refresh Token
    Parameters
    ----------------------------------------------------------
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Generates new access token from refresh token
    """

    return authentication.get_all_user(db)