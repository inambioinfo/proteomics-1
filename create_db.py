"""
Python script create_db.py

Created by Anne Pajon under user 'pajon01' on 13/10/15
"""
import os
from model import Base

from config import DATABASE_URI

from sqlalchemy import create_engine
engine = create_engine(DATABASE_URI)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
