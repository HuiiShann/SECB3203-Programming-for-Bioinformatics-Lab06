"""Week 6 extension - batch processing, logging, FASTQ and a command-line tool."""
import argparse
import logging
import sys
from collections.abc import Iterator
from pathlib import Path

from bio_io import FastaFormatError, read_fasta, write_csv

LOG = logging.getLogger("batch")


class FastqFormatError(ValueError):
    """Raised when a FASTQ file is malformed."""
    

def process_directory(in_dir, out_csv, log_path=None) -> dict[str, int]:
    """Read every *.fasta file in in_dir; one bad file never stops the batch.

    Writes one row per file (file, records, status, reason) to out_csv and
    returns {'processed': ..., 'rejected': ..., 'records': ...}.
    """
    # Set up our counting variables and the list that will hold our CSV rows
    processed = 0
    rejected = 0
    total_records = 0
    rows = []
    
    # --- LOGGING SETUP ---
    handler = None
    if log_path:
        # Create the file handler to write logs to the specified path
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        # Set the format of the log messages (time, level, message)
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
        # Attach the handler to our LOG object
        LOG.addHandler(handler)
        # Set the minimum alert level to INFO so we capture both successes and warnings
        LOG.setLevel(logging.INFO)
    
    # --- BATCH PROCESSING ---
    try:
        # sorted() ensures files are processed in exact alphabetical order on every computer
        for fasta_path in sorted(Path(in_dir).glob("*.fasta")):
            if not fasta_path.is_file():
                continue

            # The inner try/except protects the batch: if one file fails, it just jumps 
            # to the 'except' block, records the failure, and moves to the next file.
            try:
                # Convert the generator to a list so we can easily count the records
                records = list(read_fasta(fasta_path))
                record_count = len(records)

                status = "processed"
                reason = ""
                if record_count == 0:
                    status = "rejected"
                    reason = "empty file"
                rows.append({
                    "file": fasta_path.name,  # .name gets just the file name, not the whole path
                    "records": record_count,
                    "status": status,
                    "reason": reason,
                })

                if record_count == 0:
                    rejected += 1
                    if handler:
                        LOG.warning(f"rejected {fasta_path.name}: {reason}")
                else:
                    processed += 1
                    total_records += record_count
                    if handler:
                        LOG.info(f"processed {fasta_path.name}")
                    
            # Catch file, encoding, and formatting errors
            except (OSError, UnicodeDecodeError, FastaFormatError) as e:
                # Record the failure
                rows.append({
                    "file": fasta_path.name,
                    "records": 0,
                    "status": "rejected",
                    "reason": str(e),
                })
                rejected += 1
                
                # Write a WARNING log for the rejected file (not ERROR, per lab sheet rules)
                if handler:
                    LOG.warning(f"rejected {fasta_path.name}: {e}")
                    
    # --- CLEANUP & EXPORT ---
    finally:
        # This runs no matter what, ensuring the log file is closed properly
        if handler:
            LOG.removeHandler(handler)
            handler.close()

    # Call your Task 2 function to save the 'rows' list into the out_csv file
    write_csv(rows, out_csv, ["file", "records", "status", "reason"])
    
    # Return the final summary counts back to whoever called the function
    return {'processed': processed, 'rejected': rejected, 'records': total_records}


def read_fastq(path) -> Iterator[tuple[str, str, str]]:
    """Yield (read_id, sequence, quality) for each 4-line FASTQ record."""
    with open(path, encoding="utf-8") as f:
        # Create an iterator that automatically strips whitespace and newlines from every line
        line_iterator = (line.strip() for line in f)
        
        # Loop through the iterator
        for line in line_iterator:
            # Safely skip any blank lines between records
            if not line:
                continue  
                
            # The first non-blank line we hit must be the header
            header = line
            
            try:
                # Grab the next 3 exact lines from the iterator for this record
                sequence = next(line_iterator)
                plus_line = next(line_iterator)
                quality = next(line_iterator)
            except StopIteration:
                # If the file runs out of lines before we get all 4, it is malformed
                raise FastqFormatError(f"Truncated record in {path}")
                
            # Validate the strict FASTQ formatting rules
            if not header.startswith("@"):
                raise FastqFormatError("Header must start with @")
            if not plus_line.startswith("+"):
                raise FastqFormatError("Third line must start with +")
            if len(sequence) != len(quality):
                raise FastqFormatError("Sequence and quality lengths do not match")
                
            # Extract the ID (everything after '@' up to the first space)
            read_id = header[1:].split()[0]
            
            # Yield the final data tuple
            yield read_id, sequence, quality


def mean_phred(quality: str, offset: int = 33) -> float:
    """Mean Phred score of a quality string (Phred+33 by default)."""
    # Protect against dividing by zero if the string is empty
    if not quality:
        raise ValueError("Quality string cannot be empty")
        
    # sum() loops over every character 'c' in the quality string.
    # ord(c) gets the ASCII number, and we subtract the offset to get the Phred score.
    total_score = sum(ord(c) - offset for c in quality)
    
    # Calculate and return the average
    return total_score / len(quality)


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point. Exit code 0 = all good, 1 = some files rejected, 2 = bad input."""
    # Initialize the command line parser
    parser = argparse.ArgumentParser(description="Batch process FASTA files.")
    
    # Add 'in_dir' as a required positional argument (the user must provide it)
    parser.add_argument("in_dir")
    
    # Add '--out' as an optional argument that defaults to the "results" folder
    parser.add_argument("--out", default="results")
    
    # Parse the arguments typed into the terminal
    args = parser.parse_args(argv)
    
    # Convert the text paths into pathlib Objects
    in_dir = Path(args.in_dir)
    out_dir = Path(args.out)
    
    # If the provided input directory doesn't exist, print an error and exit with code 2
    if not in_dir.is_dir():
        print(f"Error: {in_dir} is not a directory.", file=sys.stderr)
        return 2
        
    # Build the exact file paths for our outputs
    out_csv = out_dir / "processing_log.csv"
    log_path = out_dir / "batch.log"
    
    # Run our batch processor and save the dictionary it returns into 'summary'
    summary = process_directory(in_dir, out_csv, log_path)
    
    # Print the exact formatted string required by the automated marker
    print(f"processed={summary['processed']} rejected={summary['rejected']} records={summary['records']}")
    
    # Return exit code 1 if any files were rejected, otherwise 0 for total success
    if summary['rejected'] > 0:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
