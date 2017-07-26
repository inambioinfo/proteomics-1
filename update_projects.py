import sqlalchemy
from datetime import datetime
import argparse
import pandas

from proteomicsdb.model import Base
from proteomicsdb.model import Project
from config import DATABASE_URI


def main():

    # get the options
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", dest="file", action="store", help="path to excel file e.g. 'PR526.xlsx'", required=True)

    options = parser.parse_args()

    engine = sqlalchemy.create_engine(DATABASE_URI)
    Base.metadata.bind = engine
    dbsession = sqlalchemy.orm.sessionmaker(bind=engine)
    dbsession = dbsession()

    try:
        sheet = pandas.read_excel(options.file, sheetname=0, header=0, index_col=None)
        sheet = sheet.where((pandas.notnull(sheet)), None)
        for i, data in enumerate(sheet.itertuples(), 1):
            project = dbsession.query(Project).filter(Project.proteomics_id == data.proteomics_id).one()
            if project:
                project.completion_date = datetime.strptime(data.completion_date, '%d.%m.%y')
                project.description = data.description
                project.experiment_type = data.experiment_type
                project.researcher = data.researcher
                project.research_group = data.research_group
                project.cell_or_tissue_type = data.cell_or_tissue_type
                project.species = data.species
                project.instrument = data.instrument
                project.experimental_details = data.experimental_details
                print 'Project', project.proteomics_id, 'updated'
        dbsession.commit()
    except Exception as e:
        dbsession.rollback()
        print e
    finally:
        dbsession.close()


if __name__ == '__main__':
    main()
