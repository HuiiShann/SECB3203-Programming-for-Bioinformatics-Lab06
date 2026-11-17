# SECB3203 Lab 6 - Files and exceptions: bio_io.py and batch.py

Student: Tan Hui Shan, A24CS0197

## Setup
    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Run
    python -m pytest                 # all tests
    ruff check src                   # style check
    python src/batch.py data/river --out results/cli      # the command-line tool

## What is in this repository
- `src/bio_io.py` : FastaFormatError, read_fasta, read_csv_records, write_csv
- `src/batch.py` : process_directory, read_fastq, mean_phred, main (command-line tool)
- `tests/` : visible tests and my own tests (test_lab06_own.py)
- `data/` : raw synthetic data, read-only (amplicons.fasta, river/, qc_records.csv, reads.fastq)
- `results/` : files the tool writes (not committed)
- `AI_USE_LOG.md` : my AI prompt log (or nil return)

## Exit codes of batch.py
**Exit Codes 0:**means completely success. The program ran, found the folder, and processed every single FASTA file perfectly without having to reject a single one.
**Exit Codes 1:**means partial success. The program successfully finished the batch, but it had to reject at least one malformed or empty file along the way.
**Exit Codes 2:**means fatal error. The program couldn't even start the batch process because the input folder the user typed in doesn't exist.
