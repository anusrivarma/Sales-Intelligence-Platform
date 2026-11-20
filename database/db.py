"""PostgreSQL connection helper.

Set DATABASE_URL as an environment variable, for example:
postgresql+psycopg2://username:password@localhost:5432/sales_intelligence
"""
import os
from sqlalchemy import create_engine

def get_engine():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("Set DATABASE_URL before connecting to PostgreSQL.")
    return create_engine(url)
