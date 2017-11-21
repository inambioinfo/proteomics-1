# -*- coding: utf-8 -*-
import json
import argparse
from collections import OrderedDict
import pandas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
import proteomicsdb.model as model


PROTEIN_HEADER = {
    'v21': OrderedDict([('Accession', 'accession'),
                        ('Description', 'description'),
                        ('Coverage', 'total_coverage'),
                        ('# Protein Groups', 'total_num_of_proteins'),
                        ('# Unique Peptides', 'total_num_of_unique_peptides'),
                        ('# Peptides', 'total_num_of_peptides'),
                        ('# PSMs', 'total_num_of_psms'),
                        ('# AAs', 'num_of_amino_acids'),
                        ('MW [kDa]', 'molecular_weight'),
                        ('calc. pI', 'calc_pi')]),
    'v14': OrderedDict([('Accession', 'accession'),
                        ('Description', 'description'),
                        (u'ΣCoverage', 'total_coverage'),
                        (u'Σ# Proteins', 'total_num_of_proteins'),
                        (u'Σ# Unique Peptides', 'total_num_of_unique_peptides'),
                        (u'Σ# Peptides', 'total_num_of_peptides'),
                        (u'Σ# PSMs', 'total_num_of_psms'),
                        ('# AAs', 'num_of_amino_acids'),
                        ('MW [kDa]', 'molecular_weight'),
                        ('calc. pI', 'calc_pi')]),
}

PEPTIDE_HEADER = {
    'v21': OrderedDict([('Annotated Sequence', 'sequence'),
                        ('# PSMs', 'num_of_psms'),
                        ('# Proteins', 'num_of_proteins'),
                        ('# Protein Groups', 'num_of_protein_groups'),
                        ('Theo. MH+ [Da]', 'mh'),
                        ('Percolator q-Value Sequest HT', 'q_value'),
                        ('Percolator PEP Sequest HT', 'pep'),
                        ('# Missed Cleavages', 'num_of_missed_cleavages')]),
    'v14': OrderedDict([('Sequence', 'sequence'),
                        ('# PSMs', 'num_of_psms'),
                        ('# Proteins', 'num_of_proteins'),
                        ('# Protein Groups', 'num_of_protein_groups'),
                        ('MH+ [Da]', 'mh'),
                        ('q-Value', 'q_value'),
                        ('PEP', 'pep'),
                        ('# Missed Cleavages', 'num_of_missed_cleavages')]),
}


def load_data(dbsession, project_proteomics_id, workbook_file, version='v21', clean_if_exists=False):
    protein_header = list(PROTEIN_HEADER[version].keys())
    peptide_header = list(PEPTIDE_HEADER[version].keys())

    project = dbsession.query(model.Project).filter(model.Project.proteomics_id == project_proteomics_id).first()
    if project:
        if clean_if_exists:
            print "Already have a project %s in db" % project.proteomics_id
            print "Removing this project and its associated data..."
            dbsession.delete(project)
            dbsession.flush()
            print "Project removed"
        else:
            raise Exception("Already have project %s. Use --clean option on the command line to overwrite it." % project.proteomics_id)

    if not workbook_file:
        return
    sheet = pandas.read_excel(workbook_file, sheetname=0, header=None, index_col=None)
    sheet = sheet.where((pandas.notnull(sheet)), None)

    # create project
    project = model.Project(proteomics_id=project_proteomics_id)
    dbsession.add(project)
    print "Project %s added" % project.proteomics_id
    this_protein_header = None
    this_peptide_header = None
    # load data
    for i, row in enumerate(sheet.iterrows(), 1):
        index, data = row
        data = data.tolist()
        print '>>> loading data for project', project.proteomics_id, 'row', i
        print data
        if data and len(data) > 1:
            if (version == 'v21' and data[0] == 'Checked' and data[1].startswith('Protein')) or (version == 'v14' and data[0] == 'Accession'):
                this_protein_header = data
                for key in protein_header:
                    if key not in this_protein_header:
                        raise KeyError('Protein header key %s not found in file for version %s.' % (key, version))
            else:
                # first column not empty, it is equal to TRUE OR FALSE (converted by pandas into a boolean) then it is protein data
                if (data[0] is True) or (data[0] is False):
                    if not this_protein_header:
                        raise Exception('Protein header not found in file, check the version. Current is %s.' % version)
                    # transform data into dictionary using protein header as keys
                    protein_dict = dict(zip(this_protein_header, data))
                    # extra data from unmaped fields in PROTEIN_HEADER before converting into json and storing in DB
                    protein_extra_data_dict = {key: protein_dict[key] for key in protein_dict if key not in protein_header}
                    # convert protein header field to standard one before storing into DB
                    protein_std_dict = {PROTEIN_HEADER[version][key]: protein_dict[key] for key in protein_dict if key in protein_header}
                    # create protein
                    protein = model.Protein(project=project,
                                            accession=protein_std_dict['accession'],
                                            description=protein_std_dict['description'],
                                            total_coverage=protein_std_dict['total_coverage'],
                                            total_num_of_proteins=protein_std_dict['total_num_of_proteins'],
                                            total_num_of_unique_peptides=protein_std_dict['total_num_of_unique_peptides'],
                                            total_num_of_peptides=protein_std_dict['total_num_of_peptides'],
                                            total_num_of_psms=protein_std_dict['total_num_of_psms'],
                                            num_of_amino_acids=protein_std_dict['num_of_amino_acids'],
                                            molecular_weight=protein_std_dict['molecular_weight'],
                                            calc_pi=protein_std_dict['calc_pi'],
                                            json_data=json.dumps(protein_extra_data_dict))
                    dbsession.add(protein)
                # first column empty, it is peptide data associated to protein
                else:
                    if (version == 'v21' and data[1] == 'Checked') or (version == 'v14' and data[1] == 'Sequence'):
                        this_peptide_header = data
                        for key in peptide_header:
                            if key not in this_peptide_header:
                                raise KeyError('Peptide header key %s not found in file for version %s' % (key, version))
                    else:
                        if not this_peptide_header:
                            raise Exception('Peptide header not found in file, check the version. Current is %s.' % version)
                        # transform data into dictionary using peptide header as keys
                        peptide_dict = dict(zip(this_peptide_header, data))
                        peptide_extra_data_dict = {key: peptide_dict[key] for key in peptide_dict if key not in peptide_header}
                        # convert peptide header field to standard one before storing into DB
                        peptide_std_dict = {PEPTIDE_HEADER[version][key]: peptide_dict[key] for key in peptide_dict if key in peptide_header}
                        # create peptide
                        peptide = model.Peptide(protein=protein,
                                                sequence=peptide_std_dict['sequence'],
                                                num_of_psms=peptide_std_dict['num_of_psms'],
                                                num_of_proteins=peptide_std_dict['num_of_proteins'],
                                                num_of_protein_groups=peptide_std_dict['num_of_protein_groups'],
                                                mh=peptide_std_dict['mh'],
                                                q_value=peptide_std_dict['q_value'],
                                                pep=peptide_std_dict['pep'],
                                                num_of_missed_cleavages=peptide_std_dict['num_of_missed_cleavages'],
                                                json_data=json.dumps(peptide_extra_data_dict))
                        dbsession.add(peptide)

    print 'Project %s created and data loaded in DB' % project.proteomics_id


def main():

    # get the options
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", dest="id", action="store", help="Proteomics ID of the project e.g. 'PR526'", required=True)
    parser.add_argument("--file", dest="file", action="store", help="path to excel data file e.g. 'PR526.xlsx'")
    parser.add_argument("--version", dest="version", action="store", help="version of proteome file, default to v21", default='v21', choices=['v14', 'v21'])
    parser.add_argument("--clean", dest="clean", action="store_true", default=False, help="Delete project before loading?")

    options = parser.parse_args()

    engine = create_engine(DATABASE_URI)
    session = sessionmaker(bind=engine)
    session = session()

    try:
        load_data(session, options.id, options.file, options.version, options.clean)
        session.commit()
    except Exception as e:
        session.rollback()
        print 'ERROR!', e
    finally:
        session.close()


if __name__ == '__main__':
    main()
