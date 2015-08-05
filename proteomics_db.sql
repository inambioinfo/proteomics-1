-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.8.1
-- PostgreSQL version: 9.3
-- Project Site: pgmodeler.com.br
-- Model Author: ---

-- object: proteomics | type: ROLE --
-- DROP ROLE IF EXISTS proteomics;
CREATE ROLE proteomics WITH 
	INHERIT
	LOGIN
	ENCRYPTED PASSWORD '********';
-- ddl-end --

-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: proteomics | type: DATABASE --
-- -- DROP DATABASE IF EXISTS proteomics;
-- CREATE DATABASE proteomics
-- 	ENCODING = 'UTF8'
-- 	LC_COLLATE = 'en_US.UTF8'
-- 	LC_CTYPE = 'en_US.UTF8'
-- 	TABLESPACE = pg_default
-- 	OWNER = postgres
-- ;
-- -- ddl-end --
-- 

-- object: public.project | type: TABLE --
-- DROP TABLE IF EXISTS public.project CASCADE;
CREATE TABLE public.project(
	project_id smallint NOT NULL,
	project_lims_id text,
	project_name text,
	CONSTRAINT project_id_pk PRIMARY KEY (project_id)

);
-- ddl-end --
ALTER TABLE public.project OWNER TO proteomics;
-- ddl-end --

-- object: public.protein | type: TABLE --
-- DROP TABLE IF EXISTS public.protein CASCADE;
CREATE TABLE public.protein(
	protein_id smallint NOT NULL,
	project_id smallint NOT NULL,
	accession text,
	description smallint,
	sum_coverage double precision,
	sum_num_of_proteins smallint,
	sum_num_of_unique_peptides smallint,
	sum_num_of_peptides smallint,
	sum_num_of_psms double precision,
	num_of_amino_acids smallint,
	"molecular_weight_kDa" double precision,
	"calc_pI" double precision,
	CONSTRAINT protein_id_pk PRIMARY KEY (protein_id)

);
-- ddl-end --
ALTER TABLE public.protein OWNER TO proteomics;
-- ddl-end --

-- object: public.protein_tag | type: TABLE --
-- DROP TABLE IF EXISTS public.protein_tag CASCADE;
CREATE TABLE public.protein_tag(
	protein_tag_id smallint NOT NULL,
	protein_id smallint NOT NULL,
	name text,
	ratio double precision,
	count smallint,
	variability smallint,
	CONSTRAINT protein_tag_id_pk PRIMARY KEY (protein_tag_id)

);
-- ddl-end --
ALTER TABLE public.protein_tag OWNER TO proteomics;
-- ddl-end --

-- object: public.protein_score | type: TABLE --
-- DROP TABLE IF EXISTS public.protein_score CASCADE;
CREATE TABLE public.protein_score(
	protein_score_id smallint NOT NULL,
	protein_id smallint NOT NULL,
	name smallint,
	search_engine_name smallint,
	score smallint,
	coverage double precision,
	num_of_peptides smallint,
	num_of_psm smallint,
	CONSTRAINT protein_score_id_pk PRIMARY KEY (protein_score_id)

);
-- ddl-end --
ALTER TABLE public.protein_score OWNER TO proteomics;
-- ddl-end --

-- object: public.peptide | type: TABLE --
-- DROP TABLE IF EXISTS public.peptide CASCADE;
CREATE TABLE public.peptide(
	peptide_id smallint NOT NULL,
	protein_id smallint NOT NULL,
	sequence text,
	num_of_psms smallint,
	num_of_proteins smallint,
	num_of_protein_groups smallint,
	"mh_Da" float,
	qvalue float,
	pep smallint,
	num_of_missed_cleavages smallint,
	CONSTRAINT peptide_id_pk PRIMARY KEY (peptide_id)

);
-- ddl-end --
ALTER TABLE public.peptide OWNER TO postgres;
-- ddl-end --

-- object: public.peptide_protein_group_accession | type: TABLE --
-- DROP TABLE IF EXISTS public.peptide_protein_group_accession CASCADE;
CREATE TABLE public.peptide_protein_group_accession(
	peptide_protein_group_accession_id smallint NOT NULL,
	peptide_id smallint NOT NULL,
	accession text,
	CONSTRAINT peptide_protein_group_accession_id_pk PRIMARY KEY (peptide_protein_group_accession_id)

);
-- ddl-end --
ALTER TABLE public.peptide_protein_group_accession OWNER TO postgres;
-- ddl-end --

-- object: public.peptide_modification | type: TABLE --
-- DROP TABLE IF EXISTS public.peptide_modification CASCADE;
CREATE TABLE public.peptide_modification(
	peptide_modification_id smallint NOT NULL,
	peptide_id smallint NOT NULL,
	modification text,
	CONSTRAINT peptide_modification_id_pk PRIMARY KEY (peptide_modification_id)

);
-- ddl-end --
ALTER TABLE public.peptide_modification OWNER TO postgres;
-- ddl-end --

-- object: project_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.protein DROP CONSTRAINT IF EXISTS project_id_fk CASCADE;
ALTER TABLE public.protein ADD CONSTRAINT project_id_fk FOREIGN KEY (project_id)
REFERENCES public.project (project_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: protein_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.protein_tag DROP CONSTRAINT IF EXISTS protein_id_fk CASCADE;
ALTER TABLE public.protein_tag ADD CONSTRAINT protein_id_fk FOREIGN KEY (protein_id)
REFERENCES public.protein (protein_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: protein_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.protein_score DROP CONSTRAINT IF EXISTS protein_id_fk CASCADE;
ALTER TABLE public.protein_score ADD CONSTRAINT protein_id_fk FOREIGN KEY (protein_id)
REFERENCES public.protein (protein_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: protein_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.peptide DROP CONSTRAINT IF EXISTS protein_id_fk CASCADE;
ALTER TABLE public.peptide ADD CONSTRAINT protein_id_fk FOREIGN KEY (protein_id)
REFERENCES public.protein (protein_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: peptide_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.peptide_protein_group_accession DROP CONSTRAINT IF EXISTS peptide_id_fk CASCADE;
ALTER TABLE public.peptide_protein_group_accession ADD CONSTRAINT peptide_id_fk FOREIGN KEY (peptide_id)
REFERENCES public.peptide (peptide_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: peptide_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.peptide_modification DROP CONSTRAINT IF EXISTS peptide_id_fk CASCADE;
ALTER TABLE public.peptide_modification ADD CONSTRAINT peptide_id_fk FOREIGN KEY (peptide_id)
REFERENCES public.peptide (peptide_id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


