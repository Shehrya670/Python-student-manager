import os
import re

# File paths
ADMIN_FILE = "admin.txt"
STUDENTS_FILE = "students.txt"
MARKS_FILE = "marks.txt"
REPORT_DIR = "report_cards"

# Validation functions
def validate_username(username):
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 20:
        return False, "Username cannot exceed 20 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, ""

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if len(password) > 20:
        return False, "Password cannot exceed 20 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*]', password):
        return False, "Password must contain at least one special character (!@#$%^&*)"
    return True, ""

def validate_student_id(student_id):
    if not student_id or len(student_id) < 4:
        return False, "Student ID must be at least 4 characters long"
    if len(student_id) > 10:
        return False, "Student ID cannot exceed 10 characters"
    if not re.match(r'^[A-Z0-9]+$', student_id):
        return False, "Student ID can only contain uppercase letters and numbers"
    return True, ""

def validate_name(name):
    if not name or len(name) < 2:
        return False, "Name must be at least 2 characters long"
    if len(name) > 50:
        return False, "Name cannot exceed 50 characters"
    if not re.match(r'^[a-zA-Z\s]+$', name):
        return False, "Name can only contain letters and spaces"
    return True, ""

def validate_department(dept):
    valid_depts = ['CS', 'EE', 'ME', 'CE', 'IT']
    if not dept or dept.upper() not in valid_depts:
        return False, f"Department must be one of: {', '.join(valid_depts)}"
    return True, ""

def validate_semester(sem):
    try:
        sem_num = int(sem)
        if not 1 <= sem_num <= 8:
            return False, "Semester must be between 1 and 8"
        return True, ""
    except ValueError:
        return False, "Semester must be a number"

# Initialize files
def initialize_files():
    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, 'w') as f:
            f.write("admin,Admin123!\n")  # Updated default admin password to meet new requirements

    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'w') as f:
            f.write("")

    if not os.path.exists(MARKS_FILE):
        with open(MARKS_FILE, 'w') as f:
            f.write("")

    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

# Load admin credentials
def load_admin():
    admin = {}
    try:
        with open(ADMIN_FILE, 'r') as f:
            for line in f:
                username, password = line.strip().split(',')
                admin[username] = password
        return admin
    except:
        return {"admin": "Admin123!"}

# Save admin credentials
def save_admin(admin):
    with open(ADMIN_FILE, 'w') as f:
        for username, password in admin.items():
            f.write(f"{username},{password}\n")

# Load students
def load_students():
    students = {}
    try:
        with open(STUDENTS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    student_id, name, dept, sem, password = parts[:5]
                    # Load courses if present, otherwise empty list
                    courses = parts[5].split(';') if len(parts) > 5 and parts[5] else []
                    students[student_id] = {
                        "name": name,
                        "dept": dept,
                        "sem": sem,
                        "password": password,
                        "courses": courses
                    }
        return students
    except:
        return {}

# Load marks
def load_marks():
    marks = {}
    try:
        with open(MARKS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    student_id, course, score = parts[0], parts[1], parts[2]
                    if student_id not in marks:
                        marks[student_id] = {}
                    marks[student_id][course] = float(score)
        return marks
    except:
        return {}

# Save students
def save_students(students):
    with open(STUDENTS_FILE, 'w') as f:
        for sid, s in students.items():
            # Save courses as semicolon-separated string
            courses_str = ';'.join(s['courses'])
            f.write(f"{sid},{s['name']},{s['dept']},{s['sem']},{s['password']},{courses_str}\n")

# Save marks
def save_marks(marks):
    with open(MARKS_FILE, 'w') as f:
        for sid, courses in marks.items():
            for course, score in courses.items():
                f.write(f"{sid},{course},{score}\n")

# Admin registration
def register_admin():
    admin = load_admin()
    print("\nAdmin Registration")
    username = input("Enter new admin username: ")

    is_valid, message = validate_username(username)
    if not is_valid:
        print(message)
        return

    if username in admin:
        print("Username already exists!")
        return

    password = input("Enter new admin password: ")
    is_valid, message = validate_password(password)
    if not is_valid:
        print(message)
        return

    confirm_password = input("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match!")
        return

    admin[username] = password
    save_admin(admin)
    print("Admin registered successfully!")

# Student registration
def register_student():
    students = load_students()
    print("\nStudent Registration")
    student_id = input("Enter student ID: ")

    is_valid, message = validate_student_id(student_id)
    if not is_valid:
        print(message)
        return

    if student_id in students:
        print("Student ID already exists!")
        return

    name = input("Enter student name: ")
    is_valid, message = validate_name(name)
    if not is_valid:
        print(message)
        return

    dept = input("Enter department (CS/EE/ME/CE/IT): ")
    is_valid, message = validate_department(dept)
    if not is_valid:
        print(message)
        return

    sem = input("Enter semester (1-8): ")
    is_valid, message = validate_semester(sem)
    if not is_valid:
        print(message)
        return

    password = input("Enter student password: ")
    is_valid, message = validate_password(password)
    if not is_valid:
        print(message)
        return

    confirm_password = input("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match!")
        return

    students[student_id] = {
        "name": name,
        "dept": dept.upper(),
        "sem": sem,
        "password": password,
        "courses": []
    }
    save_students(students)
    print("Student registered successfully!")

# Login function
def login(user_type):
    if user_type == "1":  # Admin
        admin = load_admin()
        username = input("Enter admin username: ")
        is_valid, message = validate_username(username)
        if not is_valid:
            print(message)
            return False

        password = input("Enter admin password: ")
        if admin.get(username) == password:
            print("Admin login successful!")
            return True
        else:
            print("Invalid admin credentials!")
            return False
    elif user_type == "2":  # Student
        students = load_students()
        student_id = input("Enter student ID: ")
        is_valid, message = validate_student_id(student_id)
        if not is_valid:
            print(message)
            return False

        password = input("Enter password: ")
        if student_id in students and students[student_id]["password"] == password:
            print("Student login successful!")
            return student_id
        else:
            print("Invalid student credentials!")
            return False
    else:
        print("Invalid user type!")
        return False

# Add student
def add_student():
    register_student()

# Update student
def update_student():
    students = load_students()
    student_id = input("Enter student ID to update: ")
    is_valid, message = validate_student_id(student_id)
    if not is_valid:
        print(message)
        return

    if student_id not in students:
        print("Student not found!")
        return

    name = input("Enter new name (or press Enter to keep unchanged): ")
    if name:
        is_valid, message = validate_name(name)
        if not is_valid:
            print(message)
            return
        students[student_id]["name"] = name

    dept = input("Enter new department (or press Enter to keep unchanged): ")
    if dept:
        is_valid, message = validate_department(dept)
        if not is_valid:
            print(message)
            return
        students[student_id]["dept"] = dept.upper()

    sem = input("Enter new semester (or press Enter to keep unchanged): ")
    if sem:
        is_valid, message = validate_semester(sem)
        if not is_valid:
            print(message)
            return
        students[student_id]["sem"] = sem

    password = input("Enter new password (or press Enter to keep unchanged): ")
    if password:
        is_valid, message = validate_password(password)
        if not is_valid:
            print(message)
            return
        confirm_password = input("Confirm new password: ")
        if password != confirm_password:
            print("Passwords do not match!")
            return
        students[student_id]["password"] = password

    save_students(students)
    print("Student updated successfully!")

# Delete student
def delete_student():
    students = load_students()
    student_id = input("Enter student ID to delete: ")
    is_valid, message = validate_student_id(student_id)
    if not is_valid:
        print(message)
        return

    if student_id not in students:
        print("Student not found!")
        return

    del students[student_id]
    save_students(students)
    marks = load_marks()
    if student_id in marks:
        del marks[student_id]
        save_marks(marks)
    print("Student deleted successfully!")

# Enroll student in course
def enroll_student():
    students = load_students()
    student_id = input("Enter student ID: ")
    is_valid, message = validate_student_id(student_id)
    if not is_valid:
        print(message)
        return

    if student_id not in students:
        print("Student not found!")
        return

    course = input("Enter course code: ")
    if not re.match(r'^[A-Z]{2,3}\d{3}$', course):
        print("Invalid course code format! Use format like CS101")
        return

    if course not in students[student_id]["courses"]:
        students[student_id]["courses"].append(course)
        save_students(students)
        print(f"Student enrolled in {course}!")
    else:
        print("Student already enrolled in this course!")

# Enter marks
def enter_marks():
    students = load_students()
    marks = load_marks()
    student_id = input("Enter student ID: ")
    is_valid, message = validate_student_id(student_id)
    if not is_valid:
        print(message)
        return

    if student_id not in students:
        print("Student not found!")
        return

    course = input("Enter course code: ")
    if not re.match(r'^[A-Z]{2,3}\d{3}$', course):
        print("Invalid course code format! Use format like CS101")
        return

    if course not in students[student_id]["courses"]:
        print("Student not enrolled in this course!")
        return

    score = input("Enter marks (0-100): ")
    try:
        score = float(score)
        if not 0 <= score <= 100:
            print("Marks must be between 0 and 100!")
            return
    except ValueError:
        print("Invalid marks input! Must be a number.")
        return

    if student_id not in marks:
        marks[student_id] = {}
    marks[student_id][course] = score
    save_marks(marks)
    print("Marks entered successfully!")

# Compute grade
def compute_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"

# Generate report card
def generate_report_card(student_id):
    students = load_students()
    marks = load_marks()
    is_valid, message = validate_student_id(student_id)
    if not is_valid:
        print(message)
        return

    if student_id not in students:
        print("Student not found!")
        return

    student = students[student_id]
    report = f"Report Card for {student['name']} (ID: {student_id})\n"
    report += f"Department: {student['dept']}\n"
    report += f"Semester: {student['sem']}\n"
    report += "Courses and Grades:\n"
    report += "-" * 40 + "\n"

    total_marks = 0
    count = 0
    for course in student["courses"]:
        score = marks.get(student_id, {}).get(course, 0)
        grade = compute_grade(score)
        report += f"Course: {course}, Marks: {score}, Grade: {grade}\n"
        total_marks += score
        count += 1

    percentage = (total_marks / count) if count > 0 else 0
    report += f"Percentage: {percentage:.2f}%\n"

    report_path = os.path.join(REPORT_DIR, f"{student_id}_report.txt")
    with open(report_path, 'w') as f:
        f.write(report)

    print(report)
    print(f"Report card saved to {report_path}")

# View all students
def view_students():
    students = load_students()
    if not students:
        print("No students found!")
        return
    for sid, s in students.items():
        print(f"ID: {sid}, Name: {s['name']}, Dept: {s['dept']}, Semester: {s['sem']}")

# Admin menu
def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Register New Admin")
        print("2. Add Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Enroll Student in Course")
        print("6. Enter Marks")
        print("7. View All Students")
        print("8. Generate Report Card")
        print("9. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            register_admin()
        elif choice == "2":
            add_student()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            enroll_student()
        elif choice == "6":
            enter_marks()
        elif choice == "7":
            view_students()
        elif choice == "8":
            student_id = input("Enter student ID: ")
            generate_report_card(student_id)
        elif choice == "9":
            print("Logged out!")
            break
        else:
            print("Invalid choice!")

# Student menu
def student_menu(student_id):
    students = load_students()
    while True:
        print("\nStudent Menu:")
        print("1. View Profile")
        print("2. View Courses")
        print("3. View Grades")
        print("4. View Report Card")
        print("5. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            s = students[student_id]
            print(f"ID: {student_id}, Name: {s['name']}, Dept: {s['dept']}, Semester: {s['sem']}")
        elif choice == "2":
            print("Courses:", ", ".join(students[student_id]["courses"]))
        elif choice == "3":
            marks = load_marks()
            for course in students[student_id]["courses"]:
                score = marks.get(student_id, {}).get(course, 0)
                grade = compute_grade(score)
                print(f"Course: {course}, Marks: {score}, Grade: {grade}")
        elif choice == "4":
            generate_report_card(student_id)
        elif choice == "5":
            print("Logged out!")
            break
        else:
            print("Invalid choice!")

# Main program
def main():
    initialize_files()
    while True:
        try:
            print("\nStudent Management System")
            print("1. Admin Login")
            print("2. Student Login")
            print("3. Student Registration")
            print("4. Exit")
            user_type = input("Select user type: ")

            if user_type == "1":
                if login(user_type):
                    admin_menu()
            elif user_type == "2":
                student_id = login(user_type)
                if student_id:
                    student_menu(student_id)
            elif user_type == "3":
                register_student()
            elif user_type == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")
        except KeyboardInterrupt:
            print("\nProgram terminated by user. Goodbye!")
            break

if __name__ == "__main__":
    main()