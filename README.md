# Student Management System
This is a console-based student management system built with Python. The application is designed to handle student and administrator accounts, manage course enrollment, and track grades. All user and academic data are stored securely in local text files.

# Features
User Authentication: Separate login sections for administrators and students.

Student Registration: Allows new students to register with a unique ID, ensuring strong password validation.

Course Management: Students can enroll in courses, and administrators can manage course data.

Grade Management: Administrators can add or update student marks for various courses.

Academic Reports: Students can view their grades and generate a detailed report card in a dedicated directory.

Data Persistence: All user accounts, course data, and grades are saved in text files, ensuring data is not lost when the program closes.

# Prerequisites
To run this project, you need to have Python 3.x installed on your system. No external libraries are required.

How to Run
Save the file: Save the provided code in a file named main.py.

Open a terminal: Navigate to the directory where you saved the file.

Run the application: Execute the script using the following command:

python main.py

The program will automatically create the necessary data files (admin.txt, students.txt, marks.txt) and a report_cards directory upon its first run.

# File Structure
The project creates and uses the following files and directories to manage its data:

admin.txt: Stores administrator credentials.

students.txt: Stores information about registered students.

marks.txt: Stores student marks for each course.

report_cards/: A directory where student report cards are generated and saved as .txt files.
