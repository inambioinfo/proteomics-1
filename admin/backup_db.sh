#!/bin/bash

NOW=$(date +"%Y-%m-%d")
BKP_DIR="/data/backups/bioinf-prot001"

# Create database backup file name
DB_FILE="${BKP_DIR}/proteomics_db_${NOW}.gz"
next=0
while [[ -e $DB_FILE ]]
  do
  ((next++))
  DB_FILE="${BKP_DIR}/proteomics_db_${NOW}_${next}.gz"
done

# Do backup as proteomicsdb on bioinf-prot001 with DB password stored in
# ~/.pgpass
echo "Creating database backup..."
pg_dump -h bioinf-prot001.cri.camres.org -p 5432 -U proteomics -d proteomics | gzip -f > $DB_FILE
echo "${DB_FILE} created"

echo "Cleaning old backup files..."
find $BKP_DIR -maxdepth 1 -type f -name "proteomics_*gz" -mtime +7 -delete
