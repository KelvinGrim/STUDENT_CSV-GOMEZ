import csv
import os
import re

STUDENT_FILE = "students.csv"
PROGRAM_FILE = "programs.csv"
COLLEGE_FILE = "colleges.csv"

STUDENT_HEADERS = ["ID", "First Name", "Last Name", "Program", "Year", "Gender"]
PROGRAM_HEADERS = ["Code", "Name", "College"]
COLLEGE_HEADERS = ["Code", "Name"]


def ensure_file(file, headers):
    if not os.path.exists(file):
        with open(file, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(headers)


ensure_file(STUDENT_FILE, STUDENT_HEADERS)
ensure_file(PROGRAM_FILE, PROGRAM_HEADERS)
ensure_file(COLLEGE_FILE, COLLEGE_HEADERS)


def read_csv(file):
    with open(file, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))[1:] 


def write_csv(file, rows):
    if file == STUDENT_FILE:
        headers = STUDENT_HEADERS
    elif file == PROGRAM_FILE:
        headers = PROGRAM_HEADERS
    else:
        headers = COLLEGE_HEADERS

    with open(file, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)

def valid_id(sid):
    return bool(re.fullmatch(r"\d{4}-\d{4}", sid))


def program_exists(code):
    return any(row[0] == code for row in read_csv(PROGRAM_FILE))


def college_exists(code):
    return any(row[0] == code for row in read_csv(COLLEGE_FILE))


ALLOWED_GENDERS = ["male", "female", "non-binary"]


def gender_exists(gender):
    return gender.lower() in ALLOWED_GENDERS


def add_student(data):
    if any(not d.strip() for d in data):
        return False, "All fields are required"

    if not valid_id(data[0]):
        return False, "ID Format is Invalid"

    if not program_exists(data[3]):
        return False, "Program code does not exist"

    if not gender_exists(data[5]):
        return False, "No Gender Selected"

    rows = read_csv(STUDENT_FILE)

    if any(r[0] == data[0] for r in rows):
        return False, "Student ID already exists"

    rows.append(data)
    write_csv(STUDENT_FILE, rows)
    return True, ""


def update_student(index, data):
    rows = read_csv(STUDENT_FILE)

    if not (0 <= index < len(rows)):
        return False, "Invalid student index"

    if any(not d.strip() for d in data):
        return False, "All fields are required"

    if not valid_id(data[0]):
        return False, "ID Format is Invalid"

    if not program_exists(data[3]):
        return False, "Program code does not exist"

    if not gender_exists(data[5]):
        return False, "No Gender Selected"


    for i, row in enumerate(rows):
        if i != index and row[0] == data[0]:
            return False, "Student ID already exists"

    rows[index] = data
    write_csv(STUDENT_FILE, rows)
    return True, ""


def delete_student(index):
    rows = read_csv(STUDENT_FILE)

    if not (0 <= index < len(rows)):
        return False, "Invalid student index"

    rows.pop(index)
    write_csv(STUDENT_FILE, rows)
    return True, ""


def add_college(data):
    if any(not d.strip() for d in data):
        return False, "All fields are required"

    rows = read_csv(COLLEGE_FILE)

    if any(r[0] == data[0] for r in rows):
        return False, "College code already exists"

    rows.append(data)
    write_csv(COLLEGE_FILE, rows)
    return True, ""


def add_program(data):
    if any(not d.strip() for d in data):
        return False, "All fields are required"

    if not college_exists(data[2]):
        return False, "College code does not exist"

    rows = read_csv(PROGRAM_FILE)

    if any(r[0] == data[0] for r in rows):
        return False, "Program code already exists"

    rows.append(data)
    write_csv(PROGRAM_FILE, rows)
    return True, ""
