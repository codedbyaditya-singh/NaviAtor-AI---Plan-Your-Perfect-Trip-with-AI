from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    name: str
    email: EmailStr
    phone: str
    city: str
    country: str
    pincode: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    city: str
    country: str
    pincode: str

    model_config = {
        "from_attributes": True
    }