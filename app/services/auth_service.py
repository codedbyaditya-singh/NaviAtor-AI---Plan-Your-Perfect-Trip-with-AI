from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserSignup
# from app.core.security import hash_password , verify_password

from app.schemas.user import UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

def signup_user(user: UserSignup, db: Session):

    existing_user = db.execute(
        select(User).where(User.email == user.email)
    ).scalar_one_or_none()

    if existing_user:
        return {
            "message": "Email already registered."
        }

    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        city=user.city,
        country=user.country,
        pincode=user.pincode,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully!"
    }

def login_user(email: str, password: str, db: Session):

    existing_user = db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not existing_user:
        return {
            "message": "User not found."
        }

    if not verify_password(password, existing_user.password):
        return {
            "message": "Invalid password."
        }

    access_token = create_access_token(
       {
           "user_id": existing_user.id,
           "email": existing_user.email
       }
    )

    return {
       "access_token": access_token,
       "token_type": "bearer"
    }