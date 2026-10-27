5-Minute Presentation Script

1. Intro
This is a command-line grade tracker. It reads data/students.csv, calculates averages and letter grades, prints a summary, and writes grade_report.txt. It's split into five functions, and main() runs them in order.

It gets a list of raw strings straight from the CSV, like ["78", "82", "", "79"].
It loops through them and skips anything that isn't a usable grade: None (a short row), empty or whitespace-only strings (missing grades), and text that can't become a number, which is caught with try/except ValueError.
Valid grades go into the valid_grades list as floats.
If the list is empty, it returns None, so a student with no grades doesn't cause a divide-by-zero error.
Otherwise it returns round(sum / count, 1).
Returning None lets get_letter_grade turn it into N/A, and generate_report leaves that student out of class stats. Each function's output feeds directly into the next one.

Debugging Example

The sample output didn't match (recommended)
My first test checked my results against the sample in the brief and failed, I got a class average of 79.4, but the sample said 80.1. My distribution also showed B: 4, C: 5 instead of B: 5, C: 4. I checked every student by hand. Only Charlie, Grace, Jack, and Liam are in the 80s, so B is 4. Averaging all 15 student averages gives 79.4. The sample also lists Charlie (86.5) above Grace (86.75), which can't be right. So my code was correct and the sample was off. I updated my tests to use the hand-checked values and wrote it down in the README.


At first calculate_average just did sum / len. Testing it with ["", "", "", ""] raised ZeroDivisionError. I fixed that by checking for an empty list and returning None first.


Output File, Open grade_report.txt,
Class summary: total, average, highest, lowest, top 5 students
Grade distribution, including the N/A count
Every student's average and letter grade. "Bob, Diana, and Henry have missing grades, and their averages use only the grades that exist."

requirements.txt is empty on purpose. The only module I import is csv, which comes with Python, so there's nothing to install and no virtual environment needed.

I am unsure if this is the type of presentation you were looking for or if you were expecting a video. If this presentation meets the assignment requirements, I have attached the file. However, if you would prefer a video, please let me know and I will be happy to create and submit one. I apologize in advance if I misunderstood this portion of the assignment and will gladly make any necessary corrections.Thank you for your time. I am thoroughly enjoying these courses and have already learned a great deal. I look forward to continuing with the upcoming modules.Thank you again, and I hope you have a wonderful day/night!