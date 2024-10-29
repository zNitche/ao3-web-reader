from sqlalchemy.orm import declarative_base

Base = declarative_base()

from ao3_web_reader.db.database import Database
from ao3_web_reader.db.pagination import Pagination
