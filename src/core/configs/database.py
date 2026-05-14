import logging
import os
from contextlib import contextmanager
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()

logger = logging.getLogger(__name__)

DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "qlsv")

_user = quote_plus(DB_USER)
_password = quote_plus(DB_PASSWORD)
DATABASE_URL = (
    f"mysql+pymysql://{_user}:{_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    "Provide a transactional scope around a series of operations."
    Session = scoped_session(SessionLocal)
    Session()
    try:
        yield Session
        Session.commit()
    except Exception as e:
        logger.exception("Failed during interaction with the db: %s", e)
        Session.rollback()
        raise
    finally:
        Session.remove()
