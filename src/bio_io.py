"""Week 6 - reading FASTA and CSV safely."""
import csv
from collections.abc import Iterator
from pathlib import Path


class FastaFormatError(ValueError):
    """Raised when a FASTA file does not follow the format."""
    

def _finish(record_id: str, chunks: list[str], path) -> tuple[str, str]:
    sequence = "".join(chunks).upper()
    if not sequence:
        raise FastaFormatError(f"File {path}: record '{record_id}' has no sequence.")
    return record_id, sequence
    


def read_fasta(path) -> Iterator[tuple[str, str]]:
    """Yield (record_id, sequence) for every record in a FASTA file.

    The id is the first word of the header. Wrapped lines are joined and the
    sequence is upper-cased. Records are produced one at a time, so large
    files do not have to fit in memory.

    Raises:
        FileNotFoundError: if the file does not exist.
        FastaFormatError: for data before the first header, an empty header
            or a record without sequence.
    """
    current_id = None
    chunks = []
    
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue 
                
            if line.startswith(">"):
                if current_id is not None:
                    yield _finish(current_id, chunks, path)
                    
                header_text = line[1:].strip()
                if not header_text:
                    raise FastaFormatError(f"File {path}: empty header line found.")
                
                current_id = header_text.split()[0]
                chunks = []  
                
            else:
                # Sequence line processing
                if current_id is None:
                    raise FastaFormatError(f"File {path}: sequence data before the first header.")
                chunks.append(line)
                
    # Yield the very last record when the file ends
    if current_id is not None:
        yield _finish(current_id, chunks, path)
    


def read_csv_records(path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dictionaries (all values are strings)."""
    with open(path, encoding="utf-8", newline="") as f:
        # Create a csv.DictReader object to read the CSV file
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(rows: list[dict], path, fieldnames: list[str]) -> None:
    """Write rows to a CSV file, creating the parent folder if needed."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    # mode="w" goes INSIDE the parentheses here:
    with open(path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
