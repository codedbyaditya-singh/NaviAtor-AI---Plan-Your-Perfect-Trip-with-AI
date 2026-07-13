from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#Now we’re going to make SQLAlchemy create the users table in PostgreSQL.
from app.models.user import Base
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#We’re going to teach FastAPI how to answer this question:Who is the current logged-in user?
# from fastapi import Header, HTTPException

# from app.core.security import verify_access_token
# from app.models.user import User


# def get_current_user(
#     authorization: str = Header(...),
#     db: Session = Depends(get_db)
# ):

#     token = authorization.replace("Bearer ", "")

#     payload = verify_access_token(token)

#     if payload is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid or expired token"
#         )

#     user = db.get(User, payload["user_id"])

#     if user is None:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )

#     return user