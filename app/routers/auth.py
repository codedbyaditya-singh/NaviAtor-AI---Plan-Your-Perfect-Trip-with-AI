# from fastapi import APIRouter
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.database.database import get_db
# from app.models.user import User
# # from app.schemas.user import UserSignup
# from app.schemas.user import UserSignup
# from app.core.security import hash_password
# from sqlalchemy import select
# router = APIRouter()


# # @router.get("/test")
# # def test():
# #     return {
# #         "message": "Authentication Router Working ✅"
# #     }
# @router.post("/signup")
# def signup(user: UserSignup, db: Session = Depends(get_db)):
#     existing_user = db.execute(
#        select(User).where(User.email == user.email)
#     ).scalar_one_or_none()

#     if existing_user:
#        return {
#           "message": "Email already registered."
#        }
#     new_user = User(
#         name=user.name,
#         email=user.email,
#         phone=user.phone,
#         city=user.city,
#         country=user.country,
#         pincode=user.pincode,
#         password=hash_password(user.password)
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {
#         "message": "User registered successfully!"
#     }

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import (
    UserSignup,
    UserLogin,
    UserResponse,
)
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import signup_user, login_user

from app.dependencies.auth import get_current_user
from app.models.user import User
router = APIRouter()


@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    return signup_user(user, db)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    return login_user(
        email=form_data.username,
        password=form_data.password,
        db=db
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "city": current_user.city,
        "country": current_user.country,
    }