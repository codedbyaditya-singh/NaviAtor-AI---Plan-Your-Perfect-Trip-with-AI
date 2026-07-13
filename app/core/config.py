from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
#JWT 
SECRET_KEY = "your_super_secret_key_change_this_later"
ALGORITHM = "HS256"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")