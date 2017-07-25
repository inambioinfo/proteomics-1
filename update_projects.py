import sqlalchemy
from datetime import datetime
import csv

from proteomicsdb.model import Base
from proteomicsdb.model import Project
from config import DATABASE_URI

engine = sqlalchemy.create_engine(DATABASE_URI)
Base.metadata.bind = engine
dbsession = sqlalchemy.orm.sessionmaker(bind=engine)
dbsession = dbsession()

with open('update_project.txt', 'rU') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for line in reader:
        project = dbsession.query(Project).filter(Project.proteomics_id == line['proteomics_id']).one()
        if project:
            project.completion_date = datetime.strptime(line['completion_date'], '%d.%m.%y')
            project.description = line['description']
            project.experiment_type = line['experiment_type']
            project.researcher = line['researcher']
            project.research_group = line['research_group']
            project.cell_or_tissue_type = line['cell_tissue_type']
            project.species = line['species']
            project.instrument = line['instrument']
            #project.experimental_details = line['experimental_details']
            print project.proteomics_id, 'updated'

dbsession.commit()
