"""
Python script model.py

Created by Anne Pajon under user 'pajon01' on 13/10/15
"""

from sqlalchemy import Column, Date, String, Integer, ForeignKey, Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    experiment_type = Column(String(32))
    source = Column(String(32))
    research_group = Column(String(64))
    completion_date = Column(Date)
    description = Column(String(1024))


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
    pep = Column(Float)
    num_of_missed_cleavages = Column(Integer)
    json_data = Column(Text)

    def __str__(self):
        return "%s" % self.__dict__

    def __repr__(self):
        return self.__str__()
