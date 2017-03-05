"""All blast commands used by aTRAM."""

import os
import re
import sys
import glob
import subprocess


# Try to get the sequence name and which end it is from the fasta header
PARSE_HEADER = re.compile(r'^ [>@] \s* ( .* ) ( [\s/._] [12] ) \s* $',
                          re.VERBOSE)

# Parse blast hits file
PARSE_RESULTS = re.compile(r'^ ( .* ) ( [\s\/_] [12] )', re.VERBOSE)


def create_db(fasta_file, blast_db):
    """Create a blast DB."""

    cmd = 'makeblastdb -dbtype nucl -in {} -out {}'
    cmd = cmd.format(fasta_file, blast_db)
    subprocess.check_call(cmd, shell=True)


def against_sra(args, blast_db, query, hits_file, iteration):
    """Blast the query sequences against an SRA blast DB."""

    cmd = []

    if args['protein'] and iteration == 1:
        cmd.append('tblastn')
        cmd.append('-db_gencode {}'.format(args['db_gencode']))
    else:
        cmd.append('blastn')
        cmd.append('-evalue {}'.format(args['evalue']))

    cmd.append("-outfmt '10 sseqid'")
    cmd.append('-max_target_seqs {}'.format(args['max_target_seqs']))
    cmd.append('-out {}'.format(hits_file))
    cmd.append('-db {}'.format(blast_db))
    cmd.append('-query {}'.format(query))

    command = ' '.join(cmd)
    subprocess.check_call(command, shell=True)


def against_contigs(args, blast_db, query, hits_file):
    """Blast the query sequence against the contings. The blast output
    will have the scores for later processing.
    """

    cmd = []

    if args.protein:
        cmd.append('tblastn')
        cmd.append('-db_gencode {}'.format(args.db_gencode))
    else:
        cmd.append('blastn')

    cmd.append('-db {}'.format(blast_db))
    cmd.append('-query {}'.format(query))
    cmd.append('-out {}'.format(hits_file))
    cmd.append(
        "-outfmt '10 qseqid sseqid bitscore qstart qend sstart send slen'")

    command = ' '.join(cmd)
    subprocess.check_call(command, shell=True)


def shard_name(work_dir, blast_db, shard_index):
    """Create the BLAST shard DB names."""

    file_name = '{}.blast_{:03d}'.format(blast_db, shard_index + 1)
    return os.path.join(work_dir, file_name)


def all_shard_names(work_dir, blast_db):
    """Get all of the BLAST DB names built by the preprocessor."""

    shard_pattern = '{}.blast_*.nhr'.format(blast_db)
    pattern = os.path.join(work_dir, shard_pattern)

    files = glob.glob(pattern)
    if not files:
        print(('No blast shards found. Looking for "{}"\n'
               'Verify the --work-dir and --file-prefix options.').format(
                   pattern[:-4]))
        sys.exit()

    return sorted([f[:-4] for f in files])


def output_file(work_dir, temp_dir, blast_db, name, iteration):
    """Create a file name for blast results."""

    file_name = '{}.{}.{}.fasta'.format(name, blast_db, iteration)

    return os.path.join(work_dir, temp_dir, file_name)


def temp_db(work_dir, temp_dir, blast_db, iteration):
    """Generate a name for the temp DB used to filter the contigs."""

    file_name = '{}.blast.{:02d}'.format(blast_db, iteration)
    return os.path.join(work_dir, temp_dir, file_name)
