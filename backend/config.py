from dotenv import load_dotenv
import os

load_dotenv()

class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_CONFIG')