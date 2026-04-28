"""
registry.py — Core CRUD operations for the student registry.

All functions operate on a plain dict keyed by student_id (int) whose
values are Student objects.  Business logic (validation) lives in
validation.py; display / UI logic lives in app.py.

"""
from src.models import Student
from src.validation import (
    StudentNotFoundError,
    DuplicateStudentError,
    ValidationError,
    validate_name,
    validate_phone,
    validate_grade,
    validate_student_ID,
)

def add_student(students: dict, student_id: int, name: str, phone: str, midterm: float, final: float, overwrite: bool = False) -> Student:
    """
    Add a new student to the registry.

    Args:
        students   (dict): The registry dict {student_id: Student}.
        student_id (int):  Unique ID for the new student.
        name       (str):  Student's full name (will be normalised).
        phone      (str):  Phone number (spaces/dashes stripped, digits only).
        midterm    (float): Midterm score [0, 100].
        final      (float): Final score [0, 100].
        overwrite  (bool): If True, silently replace an existing record.
    Returns:
        Student: The newly created Student object.
    Raises:
        DuplicateStudentError: If the ID already exists and overwrite=False.
        ValidationError: If any field fails validation.
    """
    sid=validate_student_ID(student_id)
    if sid in students and not overwrite:
        raise DuplicateStudentError(
            f"Student ID {sid} already exists. "
            "Use update_student() to change fields, or confirm overwrite."
        )
    cleaned_name=validate_name(name)
    cleaned_phone=validate_phone(phone)
    validated_mid=validate_grade(midterm, "Midterm")
    validated_fin=validate_grade(final, "Final")
    student = Student(sid, cleaned_name, cleaned_phone, validated_mid, validated_fin)
    students[sid] = student
    return student

# ─────────────────────────────────────────────
#  Update
# ─────────────────────────────────────────────

_UPDATABLE_FIELDS = {"name", "phone", "midterm", "final"}


def update_student(
    students: dict,
    student_id: int,
    field: str,
    new_value,
) -> Student:
    """
    Update a single field of an existing student record.

    Args:
        students   (dict): The registry dict.
        student_id (int):  ID of the student to update.
        field      (str):  One of 'name', 'phone', 'midterm', 'final'.
        new_value        : The new value (str for name/phone, numeric for grades).
    Returns:
        Student: The updated Student object.
    Raises:
        StudentNotFoundError: If student_id is not in the registry.
        ValidationError: If the field name is invalid or the value fails checks.
    """
    if student_id not in students:
        raise StudentNotFoundError(f"No student with ID {student_id}.")

    field = field.strip().lower()
    if field not in _UPDATABLE_FIELDS:
        raise ValidationError(
            f"'{field}' is not a valid field. "
            f"Choose one of: {', '.join(sorted(_UPDATABLE_FIELDS))}."
        )

    student = students[student_id]

    if field == "name":
        student.name = validate_name(str(new_value))
    elif field == "phone":
        student.phone = validate_phone(str(new_value))
    elif field == "midterm":
        student.midterm = validate_grade(float(new_value), "Midterm")
    elif field == "final":
        student.final = validate_grade(float(new_value), "Final")

    return student

# ─────────────────────────────────────────────
#  Delete
# ─────────────────────────────────────────────

def delete_student(students: dict, student_id: int) -> Student:
    """
    Remove a student record from the registry.

    Args:
        students   (dict): The registry dict.
        student_id (int):  ID of the student to remove.
    Returns:
        Student: The deleted Student object (for undo / logging purposes).
    Raises:
        StudentNotFoundError: If student_id is not in the registry.
    """
    if student_id not in students:
        raise StudentNotFoundError(f"No student with ID {student_id}.")
    return students.pop(student_id)

# ─────────────────────────────────────────────
#  Find / Search
# ─────────────────────────────────────────────

def find_by_id(students: dict, student_id: int) -> Student:
    """
    Look up a student by their exact ID.

    Args:
        students   (dict): The registry dict.
        student_id (int):  The ID to search for.
    Returns:
        Student: The matching Student object.
    Raises:
        StudentNotFoundError: If no student has that ID.
    """
    if student_id not in students:
        raise StudentNotFoundError(f"No student with ID {student_id}.")
    return students[student_id]


def search_by_name(students: dict, query: str) -> list:
    """
    Return all students whose name contains the query (case-insensitive).

    Uses str.lower(), str.strip(), and the 'in' operator to match partial names.

    Args:
        students (dict): The registry dict.
        query    (str):  Substring to search for (e.g. 'ali').
    Returns:
        list[Student]: All matching Student objects (may be empty).
    """
    needle = query.strip().lower()
    return [s for s in students.values() if needle in s.name.lower()]
