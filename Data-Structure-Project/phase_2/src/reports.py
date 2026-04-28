"""
reports.py — Class report calculations and formatted output.

All functions receive the students dict and return / print summaries.
"""

from src.models import Student


# ─────────────────────────────────────────────
#  Calculation helpers
# ─────────────────────────────────────────────

def compute_statistics(students: dict) -> dict:
    """
    Compute class-wide statistics from the student registry.

    Args:
        students (dict): The registry dict {student_id: Student}.
    Returns:
        dict with keys:
            count         (int)   - total students
            average       (float) - mean term grade
            highest       (float) - max term grade
            lowest        (float) - min term grade
            top_student   (Student)
            bottom_student(Student)
            pass_rate     (float) - % with term grade >= 60
            grade_dist    (dict)  - {'A':n, 'B':n, 'C':n, 'D':n, 'F':n}
        Returns None values for grade metrics if the registry is empty.
    """
    if not students:
        return {
            "count": 0,
            "average": None,
            "highest": None,
            "lowest": None,
            "top_student": None,
            "bottom_student": None,
            "pass_rate": None,
            "grade_dist": None,
        }

    grades = [(s, s.term_grade()) for s in students.values()]

    count   = len(grades)
    average = sum(g for _, g in grades) / count
    top     = max(grades, key=lambda x: x[1])
    bottom  = min(grades, key=lambda x: x[1])

    pass_count = sum(1 for _, g in grades if g >= 60)
    pass_rate  = pass_count / count * 100

    dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for s, _ in grades:
        dist[s.letter_grade()] += 1

    return {
        "count": count,
        "average": round(average, 2),
        "highest": round(top[1], 2),
        "lowest": round(bottom[1], 2),
        "top_student": top[0],
        "bottom_student": bottom[0],
        "pass_rate": round(pass_rate, 1),
        "grade_dist": dist,
    }


# ─────────────────────────────────────────────
#  Formatted Report
# ─────────────────────────────────────────────

def print_class_report(students: dict) -> None:
    """
    Print a formatted class summary to stdout.

    Includes: class size, average term grade, top / bottom students,
    pass rate, and letter-grade distribution.

    Args:
        students (dict): The registry dict {student_id: Student}.
    """
    stats = compute_statistics(students)

    print("\n" + "═" * 50)
    print("         CLASS REPORT — Student Registry")
    print("═" * 50)

    if stats["count"] == 0:
        print("  No students in the registry yet.")
        print("═" * 50)
        return

    top: Student    = stats["top_student"]
    bottom: Student = stats["bottom_student"]
    dist: dict      = stats["grade_dist"]

    print(f"  Class size    : {stats['count']}")
    print(f"  Average grade : {stats['average']:.1f}")
    print(f"  Highest grade : {stats['highest']:.1f}  → {top.name} (ID {top.student_id})")
    print(f"  Lowest grade  : {stats['lowest']:.1f}  → {bottom.name} (ID {bottom.student_id})")
    print(f"  Pass rate (≥60): {stats['pass_rate']:.1f}%")
    print()
    print("  Grade Distribution:")
    for letter in ("A", "B", "C", "D", "F"):
        bar = "█" * dist[letter]
        print(f"    {letter}: {bar}  ({dist[letter]})")
    print("═" * 50)
