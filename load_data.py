# -*- coding: utf-8 -*-

import json
import argparse
import codecs

import proteomicsdb.model as model


def load_data_v21(session, project_name, project_filename):
    PROTEIN_HEADERS = ['Accession', 'Description', 'Coverage', '# Protein Groups', '# Unique Peptides', '# Peptides', '# PSMs', '# AAs', 'MW [kDa]', 'calc. pI']
    PEPTIDES_HEADERS = ['Annotated Sequence', '# PSMs', '# Proteins', '# Protein Groups', 'Theo. MH+ [Da]', 'Percolator q-Value Sequest HT', 'Percolator PEP Sequest HT', '# Missed Cleavages']

    if not session.query(model.Project).filter(model.Project.proteomics_id == project_name).count() > 0:
        # create project
        project = model.Project(proteomics_id=project_name)
        session.add(project)

        with codecs.open(project_filename, encoding='utf-8') as f:
            for line in f:
                line = line.rstrip().split('\t')
                if line and len(line) > 1:
                    # protein header line starting with keyword Checked in 1st column
                    if line[0] == 'Checked' and line[1].startswith('Protein'):
                        protein_headers = line
                        for key in PROTEIN_HEADERS:
                            if key not in protein_headers:
                                print protein_headers
                                raise KeyError('Protein header %s not found in data file' % key)
                    else:
                        # first column not empty, it is protein data
                        if line[0]:
                            # transform data into dictionary using protein headers as keys
                            protein_dict = dict(zip(protein_headers, line))
                            # remove data from dictionary stored as fields (PROTEIN_HEADERS) before converting into json and storing in DB
                            protein_extra_data_dict = {key: protein_dict[key] for key in protein_dict if key not in PROTEIN_HEADERS}
                            protein = model.Protein(project=project,
                                              accession=protein_dict['Accession'],
                                              description=protein_dict['Description'],
                                              total_coverage=protein_dict['Coverage'],
                                              total_num_of_proteins=protein_dict['# Protein Groups'],
                                              total_num_of_unique_peptides=protein_dict['# Unique Peptides'],
                                              total_num_of_peptides=protein_dict['# Peptides'],
                                              total_num_of_psms=protein_dict['# PSMs'],
                                              num_of_amino_acids=protein_dict['# AAs'],
                                              molecular_weight=protein_dict['MW [kDa]'],
                                              calc_pi=protein_dict['calc. pI'],
                                              json_data=json.dumps(protein_extra_data_dict))
                            session.add(protein)
                        # first column empty, it is peptide data associated to protein
                        else:
                            # peptide header line starting with keyword Checked in 2nd column
                            if line[1] == 'Checked':
                                peptide_headers = line
                                for key in PEPTIDES_HEADERS:
                                    if key not in peptide_headers:
                                        raise KeyError('Peptide header %s not found in data file' % key)
                            else:
                                # transform data into dictionary using peptide headers as keys
                                peptide_dict = dict(zip(peptide_headers, line))
                                peptide_extra_data_dict = {key: protein_dict[key] for key in protein_dict if key not in PEPTIDES_HEADERS}
                                peptide = model.Peptide(protein=protein,
                                                  sequence=peptide_dict['Annotated Sequence'],
                                                  num_of_psms=peptide_dict['# PSMs'],
                                                  num_of_proteins=peptide_dict['# Proteins'],
                                                  num_of_protein_groups=peptide_dict['# Protein Groups'],
                                                  mh=peptide_dict['Theo. MH+ [Da]'],
                                                  q_value=peptide_dict['Percolator q-Value Sequest HT'],
                                                  pep=peptide_dict['Percolator PEP Sequest HT'],
                                                  num_of_missed_cleavages=peptide_dict['# Missed Cleavages'],
                                                  json_data=json.dumps(peptide_extra_data_dict))
                                session.add(peptide)
        print 'Project %s loaded in DB' % project_name
    else:
        print 'Project %s already exists' % project_name


def load_data_v14(session, project_name, project_filename):
    PROTEIN_HEADERS = ['Accession', 'Description', u'ΣCoverage', u'Σ# Proteins', u'Σ# Unique Peptides', u'Σ# Peptides', u'Σ# PSMs', '# AAs', 'MW [kDa]', 'calc. pI']
    PEPTIDES_HEADERS = ['Sequence', '# PSMs', '# Proteins', '# Protein Groups', 'MH+ [Da]', 'q-Value', 'PEP', '# Missed Cleavages']

    if not session.query(model.Project).filter(model.Project.proteomics_id == project_name).count() > 0:
        # create project
        project = model.Project(proteomics_id=project_name)
        session.add(project)

        with codecs.open(project_filename, encoding='utf-8') as f:
            for line in f:
                line = line.rstrip().split('\t')
                if line and len(line) > 1:
                    # protein header line starting with keyword Accession
                    if line[0] == 'Accession':
                        protein_headers = line
                        for key in PROTEIN_HEADERS:
                            if key not in protein_headers:
                                print protein_headers
                                raise KeyError('Protein header %s not found in data file' % key)
                    else:
                        # first column not empty, it is protein data
                        if line[0]:
                            # transform data into dictionary using protein headers as keys
                            protein_dict = dict(zip(protein_headers, line))
                            # remove data from dictionary stored as fields (PROTEIN_HEADERS) before converting into json and storing in DB
                            protein_extra_data_dict = {key: protein_dict[key] for key in protein_dict if key not in PROTEIN_HEADERS}
                            protein = model.Protein(project=project,
                                              accession=protein_dict['Accession'],
                                              description=protein_dict['Description'],
                                              total_coverage=protein_dict[u'ΣCoverage'],
                                              total_num_of_proteins=protein_dict[u'Σ# Proteins'],
                                              total_num_of_unique_peptides=protein_dict[u'Σ# Unique Peptides'],
                                              total_num_of_peptides=protein_dict[u'Σ# Peptides'],
                                              total_num_of_psms=protein_dict[u'Σ# PSMs'],
                                              num_of_amino_acids=protein_dict['# AAs'],
                                              molecular_weight=protein_dict['MW [kDa]'],
                                              calc_pi=protein_dict['calc. pI'],
                                              json_data=json.dumps(protein_extra_data_dict))
                            session.add(protein)
                        # first column empty, it is peptide data associated to protein
                        else:
                            # peptide header line starting with keyword Sequence
                            if line[1] == 'Sequence':
                                peptide_headers = line
                                for key in PEPTIDES_HEADERS:
                                    if key not in peptide_headers:
                                        raise KeyError('Peptide header %s not found in data file' % key)
                            else:
                                # transform data into dictionary using peptide headers as keys
                                peptide_dict = dict(zip(peptide_headers, line))
                                peptide_extra_data_dict = {key: protein_dict[key] for key in protein_dict if key not in PEPTIDES_HEADERS}
                                peptide = model.Peptide(protein=protein,
                                                  sequence=peptide_dict['Sequence'],
                                                  num_of_psms=peptide_dict['# PSMs'],
                                                  num_of_proteins=peptide_dict['# Proteins'],
                                                  num_of_protein_groups=peptide_dict['# Protein Groups'],
                                                  mh=peptide_dict['MH+ [Da]'],
                                                  q_value=peptide_dict['q-Value'],
                                                  pep=peptide_dict['PEP'],
                                                  num_of_missed_cleavages=peptide_dict['# Missed Cleavages'],
                                                  json_data=json.dumps(peptide_extra_data_dict))
                                session.add(peptide)
        print 'Project %s loaded in DB' % project_name
    else:
        print 'Project %s already exists' % project_name


def main():

    # get the options
    parser = argparse.ArgumentParser()
    parser.add_argument("--proteome-name", dest="name", action="store", help="Proteome name e.g. 'PR526'", required=True)
    parser.add_argument("--proteome-filename", dest="filename", action="store", help="path to proteome file e.g. 'data/PR526_test.txt'", required=True)
    parser.add_argument("--version", dest="version", action="store", help="version of proteome file, default to v2.1", default='v2.1', choices=['v1.4', 'v2.1'])

    options = parser.parse_args()

    from config import DATABASE_URI
    from sqlalchemy import create_engine
    engine = create_engine(DATABASE_URI)

    from sqlalchemy.orm import sessionmaker
    session = sessionmaker(bind=engine)
    session = session()

    try:
        if options.version == 'v1.4':
            load_data_v14(session, options.name, options.filename)
        else:
            load_data_v21(session, options.name, options.filename)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == '__main__':
    main()
