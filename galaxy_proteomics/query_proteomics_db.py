import psycopg2
from psycopg2.extras import RealDictCursor
import configparser
import argparse
import csv

PROJECT_QUERY = """
select * from project
"""
PROTEIN_QUERY = """
select project.name as project_name,
        protein.accession as protein_accession,
        protein.description as protein_description,
        protein.total_coverage as protein_total_coverage,
        protein.total_num_of_proteins as protein_total_num_of_proteins,
        protein.total_num_of_unique_peptides as protein_total_num_of_unique_peptides,
        protein.total_num_of_peptides as protein_total_num_of_peptides,
        protein.total_num_of_psms as protein_total_num_of_psms,
        protein.num_of_amino_acids as protein_num_of_amino_acids,
        protein.molecular_weight as protein_molecular_weight,
        protein.calc_pi as protein_calc_pi,
        peptide.sequence as peptide_sequence,
        peptide.num_of_psms as peptide_num_of_psms,
        peptide.num_of_proteins as peptide_num_of_proteins,
        peptide.num_of_protein_groups as peptide_num_of_protein_groups,
        peptide.mh as peptide_mh,
        peptide.q_value as peptide_q_value,
        peptide.pep as peptide_pep,
        peptide.num_of_missed_cleavages as peptide_num_of_missed_cleavages
from project, protein, peptide
where protein.project_id = project.id
and peptide.protein_id = protein.id
and protein.accession = '%s'
"""

PROTEIN_FIELDNAMES = ['project_name',
                      'protein_accession',
                      'protein_description',
                      'protein_total_coverage',
                      'protein_total_num_of_proteins',
                      'protein_total_num_of_unique_peptides',
                      'protein_total_num_of_peptides',
                      'protein_total_num_of_psms',
                      'protein_num_of_amino_acids',
                      'protein_molecular_weight',
                      'protein_calc_pi',
                      'peptide_sequence',
                      'peptide_num_of_psms',
                      'peptide_num_of_proteins',
                      'peptide_num_of_protein_groups',
                      'peptide_mh',
                      'peptide_q_value',
                      'peptide_pep',
                      'peptide_num_of_missed_cleavages'
                      ]

def main():
    # command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", dest="config", action="store", help="The configuration file.", required=True)
    parser.add_argument("--protein", dest="protein_accession", action="store", help="The protein accession to query e.g. 'P63261'.", required=True)
    parser.add_argument("--output", dest="output", action="store", help="Output file.", required=True)
    options = parser.parse_args()

    # read config from ini file
    config = configparser.ConfigParser()
    config.read(options.config)
    db_config = config['ProteomicsDB']

    # database connection
    db_connection = psycopg2.connect(database='proteomics', user="readonly", password="readonly", host=db_config['host'], cursor_factory=RealDictCursor)
    db = db_connection.cursor()
    db.execute(PROTEIN_QUERY % options.protein_accession)
    results = db.fetchall()

    with open(options.output, 'w') as f:
        w = csv.DictWriter(f, delimiter='\t', fieldnames=PROTEIN_FIELDNAMES)
        w.writeheader()
        for r in results:
            w.writerow(r)


if __name__ == "__main__":
    main()
