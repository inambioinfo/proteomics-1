"""
Python script config.py

Created by Anne Pajon under user 'pajon01' on 13/10/15
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLITE_DATABASE_FILE = os.path.join(basedir, 'proteomics.sqlite')
SQLITE_DATABASE_URI = 'sqlite:///' + SQLITE_DATABASE_FILE

POSTGRESQL_DATABASE_URI = 'postgresql://proteomics@bioinf-gal001.cri.camres.org:5432/proteomics'

DATABASE_URI = POSTGRESQL_DATABASE_URI