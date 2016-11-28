# Proteomics database project

This project is to create a database in order to load proteome datasets and ease the query of these datasets.


## Install dependencies in a virtual environment

Python 2.7 and git must be installed.

Postgres needs to be installed too, if you wish to create your own database.

* On Mac install Postgres using http://postgresapp.com/ for OSX which is straight forward and standard Mac app and add /Applications/Postgres.app/Contents/Versions/X.X/bin/ to your path

* On Centos6

```
sudo yum install python-devel postgresql-devel
```

### Clone github project

```
git clone https://github.com/crukci-bioinformatics/proteomics.git
cd proteomics
```

### Install python libraries

```
virtualenv venv
source venv/bin/activate
pip install sqlalchemy
pip install psycopg2
pip install csvkit
```

## Create the database

If the database already exists, all tables will be dropped.

```
python create_db.py
```

## Load data

Convert data into tab separated file using csvkit.

### Load test data (by default loading v2.1)

```
in2csv data/PR688_v21_test.xlsx | cvsformat -T > data/PR688_v21_test.txt
python load_data.py --proteome-name=TEST-PR688 --proteome-filename=data/PR688_v21_test.txt
```

```
in2csv data/PR526_test.xlsx | csvformat -T > data/PR526_test.txt
python load_data.py --proteome-name=TEST-PR526 --proteome-filename=data/PR526_test.txt --version='v1.4'
```

### Delete test data from the database

```
delete from peptide where protein_id in (select protein.id from protein, project where protein.project_id=project.id and project.name='TEST-PR688');
delete from protein where project_id in (select id from project where name='TEST-PR688');
delete from project where name='TEST-PR688';
```

### Load 5 proteomes

```
in2csv data/PR526.xlsx | csvformat -T > data/PR526.txt
python load_data.py --proteome-name='PR526' --proteome-filename=data/PR526.txt
```

## Query data

### Accessing the proteomics database

See wiki page [Accessing the proteomics database](https://github.com/crukci-bioinformatics/proteomics/wiki#accessing-the-proteomics-database)

### Using SQL

* get all projects in DB
```
select * from project;
```
* get all proteins within a project
```
select *
from project, protein
where protein.project_id = project.id
and project.name = 'PR526';
```
* get all peptides with a certain sequence
```
select *
from project, protein, peptide
where protein.project_id = project.id
and peptide.protein_id = protein.id
and peptide.sequence = 'DLYANTVLSGGTTMYPGIADR';
```
* get all proteins with a certain accession and all associated peptides
```
select *
from project, protein, peptide
where protein.project_id = project.id
and peptide.protein_id = protein.id
and protein.accession = 'P63261'
```

### Using python

```
python query_data.py
```

### Using Galaxy

See [README](galaxy_proteomics/README.md)
