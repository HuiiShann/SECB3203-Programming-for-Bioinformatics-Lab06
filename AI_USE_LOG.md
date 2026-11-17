# AI USE LOG


- Course: SECB3203
- Assessment: Lab 6
- Student name: Tan Hui Shan
- Matric no: A24CS0197
- Group ID: n/a
- AI level: 1
- Tools cited: Google (2026). Gemini. Retrieved 17 November 2026 from https://gemini.google.com

## Declaration (tick exactly one)

- [ ] NIL RETURN: I did not use any generative AI tool for this assessment.
- [x] I used AI. Every interaction that influenced my work is logged below. The log is true and complete.

## Entry 1

- Date: 17 November 2026 1:45PM
- Tool: Google (2026). Gemini. Retrieved 17 November 2026 from https://gemini.google.com
- Purpose: explain
- Prompt: What is the use of _finish() function here?
- Output: Explained it acts as a helper function to process a parsed FASTA record by joining sequence chunks, checking for empty sequences, and returning a clean tuple.
- Verified by: ran pytest
- My change: accepted the explanation to better understand the starter code logic
- Used in: src/bio_io.py, _finish()

## Entry 2

- Date: 17 November 2026 2:10PM
- Tool: Google (2026). Gemini. Retrieved 17 November 2026 from https://gemini.google.com
- Purpose: hint
- Prompt: What is the keyword I need to use to open the file? How the statement looks like?
- Output: Advised using the `with` keyword alongside `open()`, explicitly specifying `mode="w"`, `encoding="utf-8"`, and `newline=""`.
- Verified by: ran pytest
- My change: rewrote my file opening statements to include the correct mode and newline arguments to avoid FileNotFoundError.
- Used in: src/bio_io.py, read_fasta(), write_csv(), and read_csv_records()

## Entry 3

- Date: 17 November 2026 2:23PM
- Tool: Google (2026). Gemini. Retrieved 17 November 2026 from https://gemini.google.com
- Purpose: explain
- Prompt: Explain this line to me: Path(path).parent.mkdir(parents=True, exist_ok=True)
- Output: Clarified that it uses the pathlib module to grab the target directory and safely create it without crashing if the folder already exists.
- Verified by: ran the command-line tool (python src/batch.py)
- My change: accepted the explanation and kept the line to ensure output directories generate properly.
- Used in: src/bio_io.py, write_csv()

## Entry 4

- Date: 17 November 2026 2:30PM
- Tool: Google (2026). Gemini. Retrieved 17 November 2026 from https://gemini.google.com
- Purpose: explain
- Prompt: How do I use csv.DictReader & csv.DictWrites
- Output: Explained initializing DictReader/Writer with the file object and using `writeheader()` and `writerows()` to process a list of dictionaries.
- Verified by: ran pytest
- My change: applied the syntax to correctly read the raw records and write the batch logs.
- Used in: src/bio_io.py, read_csv_records() and write_csv()

## Entry 5

- Date: 17 November 2026 6:50PM
- Tool: Google (2026). Gemini. Retrieved 17 November 2026 from https://gemini.google.com
- Purpose: hint
- Prompt: How do I catch specific errors for a bad file without stopping the whole batch process in Task 3?
- Output: Advised placing the try/except block inside the for-loop iterating over the files so only the bad file fails while the loop continues.
- Verified by: ran pytest (test_batch_survives_one_bad_file passed)
- My change: shifted my try/except block inside the loop to isolate error handling per file.
- Used in: src/batch.py, process_directory()

## Entry 6

- Date: 17 November 2026 7:05PM
- Tool: Google (2026). Gemini. Retrieved 17 November 2026 from https://gemini.google.com
- Purpose: tests-plan
- Prompt: How do I test the command-line tool's exit code 2 when a folder is missing using the tmp_path fixture?
- Output: Suggested passing a fake folder string to `batch.main(["fake_path"])` and asserting the return value equals the integer 2.
- Verified by: ran pytest
- My change: wrote the `test_main_missing_dir` test function based on the logic provided.
- Used in: tests/test_lab06_own.py, test_main_missing_dir()