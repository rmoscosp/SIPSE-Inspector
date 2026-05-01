from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role: Optional[str]

class UserLogin(BaseModel):
    email: Optional[str]
    password: Optional[str]