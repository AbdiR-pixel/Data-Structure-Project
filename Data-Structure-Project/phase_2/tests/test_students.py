"""
test_students.py — Unit tests for student registry operations.

Run: python -m pytest tests/ -v
"""

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import Student
from src.registry import add_student, update_student, delete_student, find_by_id, search_by_name
from src.validation import (
    StudentNotFoundError,
    DuplicateStudentError,
    ValidationError,
)
from src.reports import compute_statistics


# ─────────────────────────────────────────────
#  Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def empty_registry():
    return {}


@pytest.fixture
def registry_with_two():
    reg = {}
    add_student(reg, 101, "Amina Ali",     "77889900", 70, 85)
    add_student(reg, 102, "Youssouf Omar", "77112233", 85, 100)
    return reg


# ─────────────────────────────────────────────
#  Add Student Tests
# ─────────────────────────────────────────────

def test_add_student_valid(empty_registry):
    """Adding a student with valid data should return a Student object."""
    s = add_student(empty_registry, 101, "Amina Ali", "77889900", 70, 85)
    assert isinstance(s, Student)
    assert s.student_id == 101
    assert s.name == "Amina Ali"
    assert s.phone == "77889900"


def test_add_student_normalises_name(empty_registry):
    """Name should be stored in Title Case regardless of input casing."""
    s = add_student(empty_registry, 201, "amina ali", "77889900", 70, 85)
    assert s.name == "Amina Ali"


def test_add_student_strips_phone(empty_registry):
    """Spaces and dashes in phone should be removed automatically."""
    s = add_student(empty_registry, 202, "Test User", "77-88 99 00", 60, 70)
    assert s.phone == "77889900"


def test_add_student_duplicate_raises(registry_with_two):
    """Adding a student with an existing ID should raise DuplicateStudentError."""
    with pytest.raises(DuplicateStudentError):
        add_student(registry_with_two, 101, "Another", "11111111", 50, 50)


def test_add_student_duplicate_overwrite(registry_with_two):
    """overwrite=True should silently replace the existing record."""
    s = add_student(registry_with_two, 101, "New Name", "99999999", 90, 90, overwrite=True)
    assert s.name == "New Name"


def test_add_student_invalid_grade_above_100(empty_registry):
    """Grade above 100 should raise ValidationError."""
    with pytest.raises(ValidationError):
        add_student(empty_registry, 301, "Test", "11111111", 105, 80)


def test_add_student_invalid_grade_below_0(empty_registry):
    """Negative grade should raise ValidationError."""
    with pytest.raises(ValidationError):
        add_student(empty_registry, 302, "Test", "11111111", -5, 80)


def test_add_student_invalid_phone(empty_registry):
    """Non-digit characters in phone (besides spaces/dashes) should raise ValidationError."""
    with pytest.raises(ValidationError):
        add_student(empty_registry, 303, "Test", "abc123xyz", 70, 80)


# ─────────────────────────────────────────────
#  Update Student Tests
# ─────────────────────────────────────────────

def test_update_student_name(registry_with_two):
    """Updating a name should store the normalised value."""
    s = update_student(registry_with_two, 101, "name", "new name here")
    assert s.name == "New Name Here"


def test_update_student_invalid_grade(registry_with_two):
    """Setting midterm > 100 via update should raise ValidationError."""
    with pytest.raises(ValidationError):
        update_student(registry_with_two, 101, "midterm", 110)


def test_update_student_missing_id(registry_with_two):
    """Updating a non-existent student should raise StudentNotFoundError."""
    with pytest.raises(StudentNotFoundError):
        update_student(registry_with_two, 999, "name", "Ghost")


def test_update_student_invalid_field(registry_with_two):
    """Using an unknown field name should raise ValidationError."""
    with pytest.raises(ValidationError):
        update_student(registry_with_two, 101, "gpa", "3.5")


# ─────────────────────────────────────────────
#  Delete Student Tests
# ─────────────────────────────────────────────

def test_delete_student_valid(registry_with_two):
    """Deleting an existing student should remove them from the registry."""
    removed = delete_student(registry_with_two, 101)
    assert removed.student_id == 101
    assert 101 not in registry_with_two


def test_delete_student_missing_id(registry_with_two):
    """Deleting a non-existent ID should raise StudentNotFoundError."""
    with pytest.raises(StudentNotFoundError):
        delete_student(registry_with_two, 999)


# ─────────────────────────────────────────────
#  Search Tests
# ─────────────────────────────────────────────

def test_search_by_name_found(registry_with_two):
    """Partial name search should return matching students."""
    results = search_by_name(registry_with_two, "ali")
    assert len(results) == 1
    assert results[0].student_id == 101


def test_search_by_name_case_insensitive(registry_with_two):
    """Search should ignore case differences."""
    results = search_by_name(registry_with_two, "AMINA")
    assert len(results) == 1


def test_search_by_name_no_match(registry_with_two):
    """Search with no matching name should return an empty list."""
    results = search_by_name(registry_with_two, "zzznomatch")
    assert results == []


# ─────────────────────────────────────────────
#  Term Grade Tests
# ─────────────────────────────────────────────

def test_term_grade_default_weights():
    """term_grade() with defaults: 40% midterm + 60% final."""
    s = Student(1, "Test", "00000000", 70, 85)
    assert s.term_grade() == pytest.approx(70 * 0.4 + 85 * 0.6)


def test_term_grade_custom_weights():
    """term_grade() should respect custom weight arguments."""
    s = Student(1, "Test", "00000000", 80, 100)
    assert s.term_grade(0.5, 0.5) == pytest.approx(90.0)


# ─────────────────────────────────────────────
#  Report Tests
# ─────────────────────────────────────────────

def test_report_average(registry_with_two):
    """Average should equal the mean of term grades for all students."""
    stats = compute_statistics(registry_with_two)
    tg1 = registry_with_two[101].term_grade()
    tg2 = registry_with_two[102].term_grade()
    assert stats["average"] == pytest.approx((tg1 + tg2) / 2, abs=0.01)


def test_report_empty_registry(empty_registry):
    """Statistics for an empty registry should return count=0 and None metrics."""
    stats = compute_statistics(empty_registry)
    assert stats["count"] == 0
    assert stats["average"] is None
