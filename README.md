# proteomics
Proteomics database project

Three tables: Project, Protein & Peptide


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

### Load test data

```
in2csv data/PR526_test.xlsx | csvformat -T > data/PR526_test.txt
python load_data.py --proteome-name=PR526 --proteome-filename=data/PR526_test.txt
```

### Load 5 proteomes

```
in2csv data/PR526.xlsx | csvformat -T > data/PR526.txt
python load_data.py --proteome-name='PR526' --proteome-filename=data/PR526.txt
```

## Query data

### Using python 

```
python query_data.py
```

### Using pgAdmin SQL query tool

* get all projects in DB
```
select * from project;
```
* get all proteins witin a project
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