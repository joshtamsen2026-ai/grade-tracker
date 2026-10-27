Student Grade Tracker

A command-line Python program that reads student grades from a CSV file, calculates each student's average and letter grade, prints a class summary, and writes a full report to grade_report.txt.

Requirements

Python 3.8 or newer
No external packages. The program uses only Python's built-in csv module, so requirements.txt is intentionally empty and no virtual environment is needed.

Project Structure

grade-tracker/
-- data/
   -- students.csv         # Input data (student_name, math, science, english, history)
-- grade_tracker.py         # Main program
-- test_grade_tracker.py    # Automated tests (built-in unittest)
-- requirements.txt         # Empty: no external dependencies
-- README.md

How to Run

From inside the project folder

The program prints a summary and top-five ranking to the terminal, and creates grade_report.txt with the summary, top-five ranking, and individual results.

Run it from the project folder, because the data path data/students.csv is relative to where you run the command.

How to Run the Tests
python -m unittest -v


How It Works

load_students(filepath), Reads the CSV with csv.DictReader and returns a list of dictionaries. Returns [] with a helpful message if the file is missing, calculate_average(grades), Skips empty or invalid values, averages the rest, rounds to 1 decimal. Returns None if no valid grades. 
get_letter_grade(average) Maps an average to A/B/C/D/F, or N/A for None, generate_report(students), Builds a summary dictionary: totals, class average, highest/lowest, grade distribution, per-student results, and the five highest averages.
write_report(report, filepath) Writes the formatted report, including the top-five ranking, to a text file.

Helpers: get_grade_values(student) pulls the subject grades out of one row, and format_average(average) displays None as N/A.

Error Handling

Missing CSV file: prints an error and exits cleanly instead of crashing.
Missing grades (empty cells): skipped, and the average uses only valid grades.
Student with no valid grades: average is None, letter grade is N/A, and they are excluded from class statistics.
Non-numeric grade (for example abc): skipped with a warning.
Report file cannot be written: prints an error instead of crashing.

Verification

Results were checked by hand against the CSV. For example:

Bob Smith: (78 + 82 + 79) / 3 = 79.7 → C (the empty English grade is skipped)
Diana Prince: (72 + 68) / 2 = 70.0 → C
Class average: mean of the 15 student averages = 79.4

Note: the sample output in the project brief shows a class average of 80.1, a distribution of B: 5 / C: 4, and Charlie Brown (86.5) ranked above Grace Lee (86.8). Hand calculation of the provided data gives 79.4, B: 4 / C: 5, and Grace ranked above Charlie. The program's output matches the hand calculations.
