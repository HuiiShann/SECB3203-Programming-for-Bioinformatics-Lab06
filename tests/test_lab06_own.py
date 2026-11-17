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
    result = batch.main(["fake_missing_folder_path"])
    assert result == 2
    
    
    