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
def update_college(index, data):
    if any(not d.strip() for d in data):
        return False, "All fields are required"

    rows = read_csv(COLLEGE_FILE)
    if not (0 <= index < len(rows)):
        return False, "Invalid index"

   
    for i, row in enumerate(rows):
        if i != index and row[0] == data[0]:
            return False, "College code already exists"
            
    old_code = rows[index][0]
    new_code = data[0]

    rows[index] = data
    write_csv(COLLEGE_FILE, rows)


    if old_code != new_code:
        prog_rows = read_csv(PROGRAM_FILE)
        changed = False
        for r in prog_rows:
            if r[2] == old_code:
                r[2] = new_code
                changed = True
        if changed:
            write_csv(PROGRAM_FILE, prog_rows)
            
    return True, ""


def update_program(index, data):
    if any(not d.strip() for d in data):
        return False, "All fields are required"

    if not college_exists(data[2]):
        return False, "College code does not exist"

    rows = read_csv(PROGRAM_FILE)
    if not (0 <= index < len(rows)):
        return False, "Invalid index"


    for i, row in enumerate(rows):
        if i != index and row[0] == data[0]:
            return False, "Program code already exists"
            
    old_code = rows[index][0]
    new_code = data[0]

    rows[index] = data
    write_csv(PROGRAM_FILE, rows)


    if old_code != new_code:
        stu_rows = read_csv(STUDENT_FILE)
        changed = False
        for r in stu_rows:
            if r[3] == old_code:
                r[3] = new_code
                changed = True
        if changed:
            write_csv(STUDENT_FILE, stu_rows)

    return True, ""


def delete_college(index):
    rows = read_csv(COLLEGE_FILE)
    if not (0 <= index < len(rows)):
        return False, "Invalid index"
    
 
    college_code = rows[index][0]
    

    prog_rows = read_csv(PROGRAM_FILE)
    if any(p[2] == college_code for p in prog_rows):
        return False, f"Cannot delete '{college_code}': There are programs currently assigned to this college. Please reassign or delete them first."


    rows.pop(index)
    write_csv(COLLEGE_FILE, rows)
    return True, ""


def delete_program(index):
    rows = read_csv(PROGRAM_FILE)
    if not (0 <= index < len(rows)):
        return False, "Invalid index"
    

    program_code = rows[index][0]
    

    student_rows = read_csv(STUDENT_FILE)
    if any(s[3] == program_code for s in student_rows):
        return False, f"Cannot delete '{program_code}': There are students currently enrolled in this program. Please reassign or delete them first."


    rows.pop(index)
    write_csv(PROGRAM_FILE, rows)
    return True, ""
