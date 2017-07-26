# Proteomics Admin ReadMe

## Database prototype creation

Currently on galaxy dev server:

```
ssh bioinf-gal001.cri.camres.org
sudo su -
sudo su - postgres
createuser proteomics
createdb proteomics
psql -U postgres -d proteomics
proteomics=# grant all on database proteomics to proteomics;
proteomics=> ALTER USER proteomics WITH PASSWORD 'proteomics';
proteomics=# \q
cd 9.3/data/
emacs pg_hba.conf
# host  proteomics        proteomics      10.20.0.0/0            md5
# local proteomics        proteomics                             md5

emacs postgresql.conf
# listen_addresses = '*'

exit
/etc/init.d/postgresql-9.3 restart
```

## Move database to production server

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
  $ ssh bioinf-prot001.cri.camres.org
  $ sudo su - postgres
  $ createuser proteomics
  $ createuser readonly
  $ createdb proteomics
  $ psql -U postgres -d proteomics
  psql (9.5.4)
  Type "help" for help.

  proteomics=# grant all on database proteomics to proteomics;
  GRANT
  proteomics=# grant select on all tables in schema public to readonly;
  GRANT
  proteomics=# alter user proteomics with encrypted password 'proteomics';
  ALTER ROLE
  proteomics=# alter user readonly with encrypted password 'readonly';
  ALTER ROLE
  proteomics=# \q

  $ vi 9.5/data/pg_hba.conf # add configuration for proteomics and set default lines to trust
  $ vi 9.5/data/postgresql.conf # uncomment listen_addresses = '*'
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

- Create database backups

  ```
  ssh bioinf-nfs001
  sudo su -
  mkdir /data/backups/bioinf-prot001
  cd /data/backups/bioinf-prot001
  git clone https://github.com/crukci-bioinformatics/proteomics.git git-proteomics

  rpm -Uvh http://yum.postgresql.org/9.5/redhat/rhel-6-x86_64/pgdg-redhat95-9.5-2.noarch.rpm
  yum install postgresql95

  useradd -g users proteomicsdb
  passwd proteomicsdb
  chown -R proteomicsdb /data/backups/bioinf-prot001

  su proteomicsdb -c "pg_dump -h bioinf-prot001.cri.camres.org -p 5432 -U proteomics -d proteomics | gzip -f > /data/backups/bioinf-prot001/proteomics_db_2016-10-28.gz
  ```

  Adding commands into cron onto the backup server bioinf-nfs001:
  ```
  chmod a+x /data/backups/bioinf-prot001/git-proteomics/admin/backup_db.sh
  su proteomicsdb -c /data/backups/bioinf-prot001/git-proteomics/admin/backup_db.sh
  ```

  ```
  # ProteomicsDB backups
  00 03 * * * /bin/su proteomicsdb -c /data/backups/bioinf-prot001/git-proteomics/admin/backup_db.sh >& /data/backups/bioinf-prot001/last_backup.log
  30 06 * * * find /data/backups/bioinf-prot001 -maxdepth 1 -type f -ctime +14 -delete
  ```

- Create test database

## Delete test data from the database

```
delete from peptide where protein_id in (select protein.id from protein, project where protein.project_id=project.id and project.proteomics_id='TEST');
delete from protein where project_id in (select id from project where proteomics_id='TEST');
delete from project where proteomics_id='TEST';
```


## Database migration

Using alembic http://alembic.zzzcomputing.com/en/latest/index.html

### Creating an environment

```bash
alembic init alembic
# add export PYTHONPATH=$HOME/workspace/git-proteomics into venv/bin/activate
```

### Creating and running a migration script

```bash
# modify model.py and automatically generate the changes
alembic revision --autogenerate -m 'add columns to project'

alembic upgrade head
```
