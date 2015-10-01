"""
Python script data_loader

Created by Anne Pajon under user 'pajon01' on 23/09/15
"""

"""
Installing SQLAlchemy and activating venv

$ virtualenv venv
$ source venv/bin/activate
$ pip install sqlalchemy

Running the script
$ python data_loader.py
"""

import os
import csv
import json

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Protein(Base):
    __tablename__ = 'protein'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    # Use cascade='delete,all' to propagate the deletion of a Project onto its Proteins
    project = relationship(
        Project,
        backref=backref('proteins', uselist=True, cascade='delete,all'))
    accession = Column(String)
    description = Column(String)
    total_coverage = Column(Float)
    total_num_of_proteins = Column(Integer)
    total_num_of_unique_peptides = Column(Integer)
    total_num_of_peptides = Column(Integer)
    total_num_of_psms = Column(Float)
    num_of_amino_acids = Column(Integer)
    molecular_weight = Column(Float)  # in kDa
    calc_pi = Column(Float)
    json_data = Column(Text)

    def __str__(self):
        return "%s" % self.__dict__

    def __repr__(self):
        return self.__str__()


class Peptide(Base):
    __tablename__ = 'peptide'
    id = Column(Integer, primary_key=True)
    protein_id = Column(Integer, ForeignKey('protein.id'))
    # Use cascade='delete,all' to propagate the deletion of a Protein onto its Peptides
    protein = relationship(
        Protein,
        backref=backref('peptides', uselist=True, cascade='delete,all'))
    sequence = Column(String)
    num_of_psms = Column(Integer)
    num_of_proteins = Column(Integer)
    num_of_protein_groups = Column(Integer)
    mh = Column(Float)  # in Da
    q_value = Column(Float)
    pep = Column(Integer)
    num_of_missed_cleavages = Column(Integer)
    json_data = Column(Text)

    def __str__(self):
        return "%s" % self.__dict__

    def __repr__(self):
        return self.__str__()

sqlite_file = 'proteomics.sqlite'
if os.path.exists(sqlite_file):
    os.remove(sqlite_file)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///%s' % sqlite_file)

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

s = session()

# load data
PROTEIN_HEADERS = ['Accession', 'Description', '_Coverage', '_# Proteins', '_# Unique Peptides', '_# Peptides', '_# PSMs', '# AAs', 'MW [kDa]', 'calc. pI']
PEPTIDES_HEADERS = ['Sequence', '# PSMs', '# Proteins', '# Protein Groups', 'MH+ [Da]', 'q-Value', 'PEP', '# Missed Cleavages']

# create project
project = Project(name='PR526')
s.add(project)
s.commit()

with open('data/PR526_test.txt') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for line in reader:
        # protein header line starting with keyword Accession
        if line[0] == 'Accession':
            protein_headers = line
            for key in PROTEIN_HEADERS:
                if key not in protein_headers:
                    raise KeyError('Protein header %s not found in data file' % key)
        else:
            # first column not empty, it is protein data
            if line[0]:
                # transform data into dictionary using protein headers as keys
                protein_dict = dict(zip(protein_headers, line))
                # remove data from dictionary stored as fields (PROTEIN_HEADERS) before converting into json and storing in DB
                protein_extra_data_dict = {key: protein_dict[key] for key in protein_dict if key not in PROTEIN_HEADERS}
                protein = Protein(project=project,
                                  accession=protein_dict['Accession'],
                                  description=protein_dict['Description'],
                                  total_coverage=protein_dict['_Coverage'],
                                  total_num_of_proteins=protein_dict['_# Proteins'],
                                  total_num_of_unique_peptides=protein_dict['_# Unique Peptides'],
                                  total_num_of_peptides=protein_dict['_# Peptides'],
                                  total_num_of_psms=protein_dict['_# PSMs'],
                                  num_of_amino_acids=protein_dict['# AAs'],
                                  molecular_weight=protein_dict['MW [kDa]'],
                                  calc_pi=protein_dict['calc. pI'],
                                  json_data=json.dumps(protein_extra_data_dict))
                s.add(protein)
                s.commit()
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
                    peptide = Peptide(protein=protein,
                                      sequence=peptide_dict['Sequence'],
                                      num_of_psms=peptide_dict['# PSMs'],
                                      num_of_proteins=peptide_dict['# Proteins'],
                                      num_of_protein_groups=peptide_dict['# Protein Groups'],
                                      mh=peptide_dict['MH+ [Da]'],
                                      q_value=peptide_dict['q-Value'],
                                      pep=peptide_dict['PEP'],
                                      num_of_missed_cleavages=peptide_dict['# Missed Cleavages'],
                                      json_data=json.dumps(peptide_extra_data_dict))
                    s.add(peptide)
                    s.commit()


# Query section:
# get all protein within a project
for protein in s.query(Protein).filter(Project.name == 'PR526').all():
    print protein.accession
    #print json.loads(protein.json_data).keys()
    for peptide in protein.peptides:
        print '\t', peptide.sequence, peptide.num_of_proteins, peptide.q_value

# get all peptides with a certain sequence
for peptide in s.query(Peptide).filter(Peptide.sequence == 'DLYANTVLSGGTTMYPGIADR').all():
    print peptide.protein.project.name, peptide.protein.accession, peptide.sequence

# get all protein with a certain accession and all associated peptides
for protein in s.query(Protein).filter(Protein.accession == 'P63261').all():
    print protein.accession
    for peptide in protein.peptides:
        print '\t', peptide.sequence, peptide.num_of_proteins, peptide.q_value

# Galaxy tool 1: upload proteome into database
# makes tool 1 private https://wiki.galaxyproject.org/UserDefinedToolboxFilters, see example in galaxy-dist/lib/galaxy/tools/toolbox/filters/examples.py.sample
# Galaxy tool 2: query the proteome database
