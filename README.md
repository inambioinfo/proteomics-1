# Proteomics database project

This project is to create a three tables: Project, Protein and Peptide database in order to load proteome datasets and ease the query of these datasets.


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

### Move database to production server

- Install Postgres on `bioinf-prot001`

  ```
  ssh bioinf-prot001.cri.camres.org
  sudo su -
  vi /etc/yum.repos.d/CentOS-Base.repo # add exclude=postgresql* in [base] and [updates] sections  
  yum localinstall https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-6-x86_64/pgdg-centos95-9.5-2.noarch.rpm
  yum list postgres*
  yum install postgresql95-server
  # data location
  ls /var/lib/pgsql/9.5/data/
  # initialise database (only needed once)
  service postgresql-9.5 initdb
  # to start postgresql automatically
  chkconfig postgresql-9.5 on
  # to start/stop service
  service postgresql-9.5 start
  ```

- Create proteomics database

  ```
  $ ssh bioinf-gal001.cri.camres.org
  $ sudo su - postgres
  $ createuser proteomics
  $ createdb proteomics
  $ psql -U postgres -d proteomics
  psql (9.5.4)
  Type "help" for help.

  proteomics=# grant all on database proteomics to proteomics;
  GRANT
  proteomics=# \q
  $ vi 9.5/data/pg_hba.conf # add configuration for proteomics and set default lines to trust
  $ vi 9.5/data/postgresql.conf # uncomment listen_addresses = 'localhost'
  exit
  sudo su -
  /etc/init.d/postgresql-9.5 restart
  ```

- Copy database from `bioinf-gal001` to `bioinf-prot001`

  ```
  ssh bioinf-gal001.cri.camres.org
  /usr/pgsql-9.3/bin/pg_dump -h localhost -p 5432 -U proteomics | gzip -f > 20160716-proteomics-db.gz
  gunzip 20160716-proteomics-db.gz
  createdb
  ```
  ```
  ssh bioinf-prot001.cri.camres.org
  scp bioinf-gal001:20160716-proteomics-db.gz .
  sudo su -
  cd /var/lib/pgsql
  mv /home/pajon01/20160716-proteomics-db.gz .
  gunzip 20160716-proteomics-db.gz
  psql -h localhost -p 5432 -U proteomics -d proteomics < /var/lib/pgsql/20160716-proteomics-db
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
