import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA", "charging_station")

if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    raise EnvironmentError(
        "Missing required database environment variables to build the connection string"
    )

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        try:
            _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        except SQLAlchemyError as e:
            print(f"Error creating DB engine: {e}")
            raise

        @event.listens_for(_engine, "connect")
        def set_search_path(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            except Exception as e:
                print(f"Error setting search_path: {e}")
                raise
            finally:
                cursor.close()

    return _engine


def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        try:
            _SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=get_engine()
            )
        except SQLAlchemyError as e:
            print(f"Error creating SessionLocal: {e}")
            raise
    return _SessionLocal


def get_db() -> Session:
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
