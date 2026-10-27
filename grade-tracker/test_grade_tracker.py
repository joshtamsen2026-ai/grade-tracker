"""Tests for grade_tracker.py. Run with:  python -m unittest -v"""

import os
import tempfile
import unittest

from grade_tracker import (
    calculate_average,
    generate_report,
    get_letter_grade,
    load_students,
    write_report,
)


class TestCalculateAverage(unittest.TestCase):
    def test_all_grades_present(self):
        self.assertEqual(calculate_average(["92", "88", "95", "91"]), 91.5)

    def test_skips_missing_grades(self):
        self.assertEqual(calculate_average(["78", "82", "", "79"]), 79.7)

    def test_no_valid_grades_returns_none(self):
        self.assertIsNone(calculate_average(["", "", "", ""]))

    def test_empty_list_returns_none(self):
        self.assertIsNone(calculate_average([]))

    def test_skips_none_whitespace_and_text(self):
        self.assertEqual(calculate_average(["90", None, "  ", "abc", "80"]), 85.0)


class TestGetLetterGrade(unittest.TestCase):
    def test_boundaries(self):
        cases = [(100, "A"), (90, "A"), (89.9, "B"), (80, "B"), (79.9, "C"),
                 (70, "C"), (69.9, "D"), (60, "D"), (59.9, "F"), (0, "F")]
        for average, expected in cases:
            with self.subTest(average=average):
                self.assertEqual(get_letter_grade(average), expected)

    def test_none_is_na(self):
        self.assertEqual(get_letter_grade(None), "N/A")


class TestLoadStudents(unittest.TestCase):
    def test_loads_provided_csv(self):
        students = load_students("data/students.csv")
        self.assertEqual(len(students), 15)
        self.assertEqual(students[0]["student_name"], "Alice Johnson")

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(load_students("data/does_not_exist.csv"), [])


class TestGenerateReport(unittest.TestCase):
    def setUp(self):
        self.report = generate_report(load_students("data/students.csv"))

    # Expected values were verified by hand (see README "Verification").
    # Note: the sample output in the project brief shows 80.1 and B: 5 / C: 4,
    # but hand calculation of the provided CSV gives 79.4 and B: 4 / C: 5.
    def test_class_statistics(self):
        self.assertEqual(self.report["total_students"], 15)
        self.assertEqual(self.report["class_average"], 79.4)
        self.assertEqual(self.report["highest_average"], 95.2)
        self.assertEqual(self.report["lowest_average"], 58.2)

    def test_grade_distribution(self):
        self.assertEqual(self.report["grade_distribution"],
                         {"A": 3, "B": 4, "C": 5, "D": 2, "F": 1, "N/A": 0})

    def test_partial_grades_students(self):
        results = {r["name"]: r for r in self.report["students"]}
        self.assertEqual(results["Bob Smith"]["average"], 79.7)     # 239 / 3
        self.assertEqual(results["Diana Prince"]["average"], 70.0)  # 140 / 2
        self.assertEqual(results["Henry Davis"]["average"], 78.7)   # 236 / 3

    def test_top_five_students_are_ranked_by_average(self):
        self.assertEqual(
            [student["name"] for student in self.report["top_students"]],
            [
                "Eve Williams",
                "Noah Garcia",
                "Alice Johnson",
                "Jack Taylor",
                "Grace Lee",
            ],
        )

    def test_student_with_no_grades(self):
        report = generate_report([{"student_name": "Empty", "math": "",
                                   "science": "", "english": "", "history": ""}])
        self.assertEqual(report["students"][0]["letter_grade"], "N/A")
        self.assertEqual(report["grade_distribution"]["N/A"], 1)
        self.assertIsNone(report["class_average"])
        self.assertEqual(report["top_students"], [])

    def test_empty_student_list(self):
        report = generate_report([])
        self.assertEqual(report["total_students"], 0)
        self.assertIsNone(report["class_average"])


class TestWriteReport(unittest.TestCase):
    def test_writes_all_sections(self):
        report = generate_report(load_students("data/students.csv"))
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "report.txt")
            write_report(report, path)
            with open(path, encoding="utf-8") as f:
                text = f.read()
        for expected in ["CLASS SUMMARY", "GRADE DISTRIBUTION",
                         "TOP 5 STUDENTS", "Eve Williams", "Grace Lee",
                         "INDIVIDUAL RESULTS", "Olivia White", "79.4"]:
            self.assertIn(expected, text)


if __name__ == "__main__":
    unittest.main()
