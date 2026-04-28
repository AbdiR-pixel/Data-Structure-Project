"""
validation.py — Reusable input validation helpers and custom exceptions.

All input-reading functions raise ValidationError on bad input so that
the UI layer can catch it and show a friendly message without crashing.
"""
class StudentNotFoundError(Exception):
    """raised when a student ID is not found in the registry"""
    pass

class DuplicateStudentError(Exception):
    """raised when a student ID is already existing in the registry"""
    pass

class TicketNotFoundError(Exception):
    """raised when Ticket Id is not found in the registry"""
    pass

class ValidationError(Exception):
    """raised when the entry is not validated correctly"""
    
    
    
# ─────────────────────────────────────────────
#  Safe Input Readers
# ─────────────────────────────────────────────


def read_int(prompt: str) -> int:
    """
    Prompt the user and return an integer.

    Args:
        prompt: The message shown to the user.
    Returns:
        int: The parsed integer value.
    Raises:
        ValidationError: If the input cannot be converted to int.
    """
    text=input(prompt).strip()
    try:
        return int(text)
    except ValueError:
        raise ValidationError(f"expected an integer. got {text}")
    
def read_float(prompt: str) -> float:
    """
    Prompt the user and return a float.

    Args:
        prompt: The message shown to the user.
    Returns:
        float: The parsed float value.
    Raises:
        ValidationError: If the input cannot be converted to float.
    """
    text=input(prompt).strip()
    try:
        return float(text)
    except ValueError:
        raise ValidationError(f"expected a float. got {text}")
    
def read_non_empty(prompt: str) -> str:
    """
    Prompt the user and return a float.

    Args:
        prompt: The message shown to the user.
    Returns:
        float: The parsed float value.
    Raises:
        ValidationError: If the input cannot be converted to float.
    """
    text=input(prompt).strip()
    try:
        return str(text)
    except ValueError:
        raise ValidationError(f"expected a float. got {text}")
    
# ─────────────────────────────────────────────
#  Field Validators 
# ─────────────────────────────────────────────

def validate_name(name: str) -> str:
    """
    Validate and normalise a student name (strip + title-case).

    Args:
        name: Raw name string from user input.
    Returns:
        str: Cleaned, title-cased name.
    Raises:
        ValidationError: If the resulting name is empty.
    """
    cleaned=name.strip().title() 
    if not cleaned:
        raise ValidationError("Name must not be empty bro")
    return cleaned 

def validate_phone(phone: int) -> int:
    """
    Validate and normalise a phone number to digits only.

    Removes spaces and dashes, then verifies only digits remain.

    Args:
        phone: Raw phone string from user input.
    Returns:
        str: Digits-only phone string.
    Raises:
        ValidationError: If the cleaned string contains non-digit characters
        or is empty.
    """
    cleaned=phone.strip().replace(" ", "").replace("-", "")
    if not cleaned:
        raise ValidationError("Phone must not be empty twin")
    if not cleaned.isdigit():
        raise ValidationError("You Dumb nigga? Enter digits only bitch")
    return cleaned

def validate_grade(score: float, label:str="Grade") -> float:
    """
    Validate that a numeric grade is within [0, 100].

    Args:
        value: The numeric grade to check.
        label: Human-readable label used in error messages.
    Returns:
        float: The validated grade.
    Raises:
        ValidationError: If the value is outside [0, 100].
    """
    if not (0 <= score <= 100):
        raise ValidationError(f"{label} must be between 0 and 100 (got {score})")
    return score
def validate_student_ID(student_ID: int) -> int:
    """
    Validate that a student ID is a positive integer.

    Args:
        sid: The student ID to check.
    Returns:
        int: The validated student ID.
    Raises:
        ValidationError: If the ID is not positive.
    """
    if student_ID <= 0:
        raise ValidationError(f"Student Id must be a positive integer (got{student_ID})")
    return student_ID
    