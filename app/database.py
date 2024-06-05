from sqlalchemy					import create_engine
from sqlalchemy.ext.declarative	import declarative_base
from sqlalchemy.orm				import sessionmaker

import psycopg
from psycopg.rows   import dict_row
import time

from .config import settings


SQLALCHEMY_DATABASE_URL =	f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}/{settings.DB_NAME}"
engine                  =	create_engine( SQLALCHEMY_DATABASE_URL )
SessionLocal            =	sessionmaker( autocommit=False , autoflush=False , bind=engine )
Base                    =   declarative_base()


# Dependency
def get_db () :

    db	=	SessionLocal()

    try:
        yield db
    finally:
        db.close()



while True :

    try:
        
        conn    =   psycopg.connect( host=settings.DB_HOSTNAME , dbname=settings.DB_NAME , user=settings.DB_USER , password=settings.DB_PASSWORD , row_factory=dict_row )
        cursor  =   conn.cursor()

        print( "Database connection was succesfull!" )

        break

    except Exception as error:

        print( "Database connection failed!" )
        print( "Error: " , error )

        time.sleep( 2 )
