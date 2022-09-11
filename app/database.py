from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os

# DATABASE_URL = "mysql+mysqlconnector://furraylogic:'FurrayL@2AVEl'@34.71.20.154:3306/bkgpal"
load_dotenv()

DB = {
    'drivername': 'mysql+mysqlconnector',
    'host': os.getenv('DB_ADDRESS'),
    'port': '3306',
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PWD'),
    'database': os.getenv('DB_SCHEMA'),
    'query': {'charset':'utf8'}
}

engine = create_engine(URL.create(**DB), pool_size=20, max_overflow=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
print(f"{engine.pool.status()}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
