import pytest
import bio_io
import batch

def test_missing_fasta(tmp_path):
    # Create a temporary directory and a path to a non-existent file
    fasta_path = tmp_path / "nonexistent.fasta"
    
    # Attempt to read the non-existent FASTA file and expect a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        list(bio_io.read_fasta(fasta_path))
    
def test_empty_fasta(tmp_path):
    test_file = tmp_path / "empty.fasta"
    test_file.write_text("")
    assert list(bio_io.read_fasta(test_file)) == []
    
def test_record_no_sequence(tmp_path):
    test_file = tmp_path / "bad.fasta"
    test_file.write_text(">gene_A\n")
    with pytest.raises(bio_io.FastaFormatError):
        list(bio_io.read_fasta(test_file))
    
def test_main_missing_dir(tmp_path):
    result = batch.main([str(tmp_path / "missing")])
    assert result == 2
    
def test_log_overwritten(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.fasta").write_text(">sample\nACGT\n")
    log_path = tmp_path / "logs" / "batch.log"

    batch.process_directory(input_dir, tmp_path / "output.csv", log_path)
    batch.process_directory(input_dir, tmp_path / "output.csv", log_path)

    log_lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(log_lines) == 1
    assert "processed sample.fasta" in log_lines[0]
    