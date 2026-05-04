import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://mego:mego@db:5432/mego')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production-please')