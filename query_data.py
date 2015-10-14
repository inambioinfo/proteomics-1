"""
Python script query_data.py

Created by Anne Pajon under user 'pajon01' on 14/10/15
"""

import model


def query_data(session):
    # get all proteins within a project
    for protein in session.query(model.Protein).filter(model.Project.name == 'PR526').all():
        print protein.accession
        #print json.loads(protein.json_data).keys()
        for peptide in protein.peptides:
            print '\t', peptide.sequence, peptide.num_of_proteins, peptide.q_value

    # get all peptides with a certain sequence
    for peptide in session.query(model.Peptide).filter(model.Peptide.sequence == 'DLYANTVLSGGTTMYPGIADR').all():
        print peptide.protein.project.name, peptide.protein.accession, peptide.sequence

    # get all proteins with a certain accession and all associated peptides
    for protein in session.query(model.Protein).filter(model.Protein.accession == 'P63261').all():
        print protein.accession
        for peptide in protein.peptides:
            print '\t', peptide.sequence, peptide.num_of_proteins, peptide.q_value


from config import DATABASE_URI
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URI)

from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)
session = session()

try:
    query_data(session)
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()
