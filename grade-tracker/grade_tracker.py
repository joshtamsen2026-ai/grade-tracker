"""
Student Grade Tracker
=====================

Reads student grade data from a CSV file, calculates each student's average
and letter grade, prints a class summary to the terminal, and writes a full
formatted report to a text file.

Uses only Python's built-in modules (csv), so no external packages are needed.
"""

import csv

# The subject columns we expect in the CSV. Keeping them in one place means
# adding a new subject only requires changing this list.
SUBJECTS = ["math", "science", "english", "history"]

# Letter grades in display order. Used to build the distribution dictionary.
LETTER_GRADES = ["A", "B", "C", "D", "F", "N/A"]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_grade_values(student):
    """Return the raw grade values for one student, in SUBJECTS order.

    Uses .get() so a row with a missing column returns "" instead of raising
    a KeyError.
    """
    return [student.get(subject, "") for subject in SUBJECTS]


def format_average(average):
    """Format an average for display, showing 'N/A' when there is none."""
    return f"{average:.1f}" if average is not None else "N/A"


# ---------------------------------------------------------------------------
# Required functions
# ---------------------------------------------------------------------------

def load_students(filepath):
    """Read the CSV at filepath and return a list of student dictionaries.

    Each dictionary maps column headers to values, for example:
        {"student_name": "Alice Johnson", "math": "92", ...}

    If the file does not exist, print a helpful message and return [].
    """
    try:
        # newline="" is recommended by the csv module docs so line endings
        # inside the file are handled correctly on every operating system.
        with open(filepath, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            return [row for row in reader]
    except FileNotFoundError:
        print(f"  Error: Could not find '{filepath}'.")
        print("  Make sure you are running the program from the project folder")
        print("  and that the data file exists.")
        return []


def calculate_average(grades):
    """Return the average of the valid grades, rounded to 1 decimal place.

    Empty strings (missing grades) are skipped. Values that are not numbers
    are also skipped so one bad cell cannot crash the program.
    Returns None if there are no valid grades.
    """
    valid_grades = []

    for grade in grades:
        # None can appear if a CSV row is shorter than the header row.
        if grade is None:
            continue

        grade = str(grade).strip()
        if grade == "":
            continue  # Missing grade: skip it

        try:
            valid_grades.append(float(grade))
        except ValueError:
            # Non-numeric value such as "abc": skip it instead of crashing.
            print(f"  Warning: Skipping invalid grade value '{grade}'.")

    if not valid_grades:
        return None

    return round(sum(valid_grades) / len(valid_grades), 1)


def get_letter_grade(average):
    """Convert a numeric average to a letter grade ("N/A" if None)."""
    if average is None:
        return "N/A"
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def generate_report(students):
    """Build and return a summary dictionary for the whole class.

    Returned keys:
        total_students     - number of student records
        class_average      - average of all student averages (None if none)
        highest_average    - best student average (None if none)
        lowest_average     - lowest student average (None if none)
        grade_distribution - count of students per letter grade
        students           - list of {"name", "average", "letter_grade"}
        top_students       - up to five students with the highest averages
    """
    results = []
    distribution = {letter: 0 for letter in LETTER_GRADES}

    for student in students:
        name = student.get("student_name", "").strip() or "Unknown"
        average = calculate_average(get_grade_values(student))
        letter = get_letter_grade(average)

        results.append({
            "name": name,
            "average": average,
            "letter_grade": letter,
        })
        distribution[letter] += 1

    # Only students with a real average count toward class statistics.
    valid_averages = [r["average"] for r in results if r["average"] is not None]
    top_students = sorted(
        (result for result in results if result["average"] is not None),
        key=lambda result: result["average"],
        reverse=True,
    )[:5]

    if valid_averages:
        class_average = round(sum(valid_averages) / len(valid_averages), 1)
        highest_average = max(valid_averages)
        lowest_average = min(valid_averages)
    else:
        class_average = highest_average = lowest_average = None

    return {
        "total_students": len(students),
        "class_average": class_average,
        "highest_average": highest_average,
        "lowest_average": lowest_average,
        "grade_distribution": distribution,
        "students": results,
        "top_students": top_students,
    }


def write_report(report, filepath):
    """Write the full formatted report to a text file at filepath."""
    divider = "=" * 50
    line = "-" * 50

    lines = [
        divider,
        "STUDENT GRADE REPORT".center(50),
        divider,
        "",
        "CLASS SUMMARY",
        line,
        f"Total students:   {report['total_students']}",
        f"Class average:    {format_average(report['class_average'])}",
        f"Highest average:  {format_average(report['highest_average'])}",
        f"Lowest average:   {format_average(report['lowest_average'])}",
        "",
        "GRADE DISTRIBUTION",
        line,
    ]

    for letter, count in report["grade_distribution"].items():
        lines.append(f"  {letter:<4} {count}")

    lines += [
        "",
        "TOP 5 STUDENTS",
        line,
        f"{'Student':<22}{'Average':>8}   {'Grade':<5}",
        line,
    ]

    if report["top_students"]:
        for result in report["top_students"]:
            lines.append(
                f"{result['name']:<22}"
                f"{format_average(result['average']):>8}   "
                f"{result['letter_grade']:<5}"
            )
    else:
        lines.append("  No students with valid grades.")

    lines += [
        "",
        "INDIVIDUAL RESULTS",
        line,
        f"{'Student':<22}{'Average':>8}   {'Grade':<5}",
        line,
    ]

    for result in report["students"]:
        lines.append(
            f"{result['name']:<22}"
            f"{format_average(result['average']):>8}   "
            f"{result['letter_grade']:<5}"
        )

    lines += ["", divider]

    try:
        with open(filepath, "w", encoding="utf-8") as report_file:
            report_file.write("\n".join(lines) + "\n")
    except OSError as error:
        print(f"  Error: Could not write report to '{filepath}': {error}")


# ---------------------------------------------------------------------------
# Program entry point (provided - do not modify)
# ---------------------------------------------------------------------------

def main():
    print("Loading student data...")
    students = load_students("data/students.csv")

    if not students:
        print("No student data found. Exiting.")
        return

    print(f"  Loaded {len(students)} students.\n")

    print("Generating report...\n")
    report = generate_report(students)

    print("--- Summary ---")
    print(f"Total students:   {report['total_students']}")
    print(f"Class average:    {report['class_average']}")
    print(f"Highest average:  {report['highest_average']}")
    print(f"Lowest average:   {report['lowest_average']}")

    print("\nGrade Distribution:")
    for letter, count in report["grade_distribution"].items():
        print(f"  {letter}: {count}")

    print("\nTop 5 students:")
    for s in report["top_students"]:
        print(f"  {s['name']:<20} {s['average']:>5.1f}  ({s['letter_grade']})")

    write_report(report, "grade_report.txt")
    print("\nReport written to grade_report.txt")


if __name__ == "__main__":
    main()
