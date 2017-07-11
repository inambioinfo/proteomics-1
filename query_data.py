"""
Python script query_data.py

Created by Anne Pajon under user 'pajon01' on 14/10/15
"""
import argparse
import proteomicsdb.model as model

QUERIES = ['proteome', 'sequence', 'protein']


def query_data(session, query, value):

    print '\t'.join(['proteome', 'protein_accession', 'peptide_sequence'])
    if query == 'proteome':
        # get all proteins within a project
        for protein in session.query(model.Protein).filter(model.Project.name == value).all():
            for peptide in protein.peptides:
                print '\t'.join([protein.project.name, protein.accession, peptide.sequence])

    if query == 'sequence':
        # get all peptides with a certain sequence
        for peptide in session.query(model.Peptide).filter(model.Peptide.sequence == value).all():
            print '\t'.join([peptide.protein.project.name, peptide.protein.accession, peptide.sequence])

    if query == 'protein':
        # get all proteins with a certain accession and all associated peptides
        for protein in session.query(model.Protein).filter(model.Protein.accession == value).all():
            for peptide in protein.peptides:
                print '\t'.join([protein.project.name, protein.accession, peptide.sequence])


def main():

    # get the options
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", dest="query", action="store", choices=QUERIES, help="Possible queries, e.g. %s" % QUERIES, required=True)
    parser.add_argument("--value", dest="value", action="store", help="Value to search, e.g. proteome 'PR526' or protein accession 'P63261' or peptide sequence e.g. 'DLYANTVLSGGTTMYPGIADR'", required=True)

    options = parser.parse_args()

    from config import DATABASE_URI
    from sqlalchemy import create_engine
    engine = create_engine(DATABASE_URI)

    from sqlalchemy.orm import sessionmaker
    session = sessionmaker(bind=engine)
    session = session()

    try:
        query_data(session, options.query, options.value)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == '__main__':
    main()
