"""
Python script create_db.py

Created by Anne Pajon under user 'pajon01' on 13/10/15
"""
from sqlalchemy import create_engine

from proteomicsdb.model import Base
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
