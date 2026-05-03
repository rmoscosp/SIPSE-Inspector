from fastapi import APIRouter, HTTPException
from src.models.user_model import UserRegister, UserLogin
from src.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register(user: UserRegister):
    try:
        return UserService.register(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin):
    try:
        return UserService.login(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))