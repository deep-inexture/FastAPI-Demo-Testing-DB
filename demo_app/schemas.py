from pydantic import BaseModel
from typing import Optional, List
import datetime

"""
Following File contains BaseModel for each table to make it visible in json format while building APIs.'
Each of them can be called as per requirements in response_model in routers.
"""


class User(BaseModel):
    """User UseCase: Registration Schema requirements for User"""
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserRegister(User):
    """User UseCase: Field required for users, but not needed in database. therefore different class
       via inheriting above class."""
    confirm_password: str

    class Config:
        orm_mode = True


class ShowUserBase(BaseModel):
    """
    User UseCase: Common Schema so that it can be viewed while accessing Foreign Key elements
    and values
    """
    username: str
    email: str

    class Config:
        orm_mode = True


class ShowUser(ShowUserBase):
    """User UseCase: Schema that shows Shipping Info details including user details from Above."""
    shipping_info: List[ShowUserBase] = []

    class Config:
        orm_mode = True


class Login(BaseModel):
    """User/Admin UseCase: Login Criteria to be fulfilled to access particular endpoints."""
    username: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    """User/Admin UseCase: Create Token and let user get their access_token for verification."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """User UseCase: for verifying above data email is mandatory to get user data."""
    email: Optional[str] = None


class ForgotPassword(BaseModel):
    """User UseCase: To recover password endpoint will require email to verify again."""
    email: str


class ResetPassword(BaseModel):
    """User UseCase: User will get again new token to recover password valid for some time."""
    password: str
    confirm_password: str