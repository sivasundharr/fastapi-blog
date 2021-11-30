import psycopg2
import time
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


#while True:
#
#   try:
#        conn = psycopg2.connect(host='localhost',database='socialapp',user='postgres',password='siva123',
#           cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#        print("Database connected")
#       break
#    except Exception as error:
#        print("Connecting to database failed")
#        print(error)
#       time.sleep(3)