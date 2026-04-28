"""
models.py — Data models for the Student Service Desk application.

Contains:
    Student      — one student record with behaviour (term_grade, to_dict).
    TicketStatus — enum for ticket state (OPEN / RESOLVED).
    Ticket       — one service request linked to a student.
"""

from enum import Enum


# ─────────────────────────────────────────────
#  Student
# ─────────────────────────────────────────────

class Student:
    """
    Represents one student record.

    Attributes:
        student_id (int):  Unique positive integer identifier.
        name       (str):  Full name in Title Case.
        phone      (str):  Digits-only phone string.
        midterm    (float): Midterm exam score [0, 100].
        final      (float): Final exam score [0, 100].
    """

    def __init__(
        self,
        student_id: int,
        name: str,
        phone: str,
        midterm: float,
        final: float,
    ):
        self.student_id = student_id
        self.name = name
        self.phone = phone
        self.midterm = midterm
        self.final = final

    # ── Behaviour ────────────────────────────

    def term_grade(self, w_mid: float = 0.40, w_final: float = 0.60) -> float:
        """
        Return the weighted term grade.

        Formula: term = midterm * w_mid + final * w_final
        Default weights: midterm 40 %, final 60 %.

        Args:
            w_mid   (float): Weight for midterm score (default 0.40).
            w_final (float): Weight for final score   (default 0.60).
        Returns:
            float: Weighted term grade in [0, 100].
        """
        return round(self.midterm * w_mid + self.final * w_final, 2)

    def letter_grade(self) -> str:
        """
        Return the letter grade based on the term grade.

        Returns:
            str: One of 'A', 'B', 'C', 'D', or 'F'.
        """
        tg = self.term_grade()
        if tg >= 90:
            return "A"
        if tg >= 80:
            return "B"
        if tg >= 70:
            return "C"
        if tg >= 60:
            return "D"
        return "F"

    def passed(self, passing_grade: float = 60.0) -> bool:
        """Return True if the student's term grade is >= passing_grade."""
        return self.term_grade() >= passing_grade

    # ── Display ──────────────────────────────

    def __str__(self) -> str:
        return (
            f"ID={self.student_id} | {self.name} | Phone: {self.phone} | "
            f"Midterm: {self.midterm}  Final: {self.final}  "
            f"Term: {self.term_grade():.1f} ({self.letter_grade()})"
        )

    def to_dict(self) -> dict:
        """Return a plain dictionary representation of the student."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "phone": self.phone,
            "midterm": self.midterm,
            "final": self.final,
        }


# ─────────────────────────────────────────────
#  TicketStatus
# ─────────────────────────────────────────────

class TicketStatus(Enum):
    """Possible states for a service ticket."""
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"


# ─────────────────────────────────────────────
#  Ticket
# ─────────────────────────────────────────────

class Ticket:
    """
    Represents a service request linked to a student.

    Attributes:
        ticket_id       (int):          Auto-incremented unique identifier.
        student_id      (int):          ID of the student who raised the request.
        category        (str):          Short category label (e.g. 'Grade inquiry').
        description     (str):          Detailed request description.
        status          (TicketStatus): Current state (OPEN or RESOLVED).
        resolution_note (str | None):   Note added when the ticket is resolved.
    """

    def __init__(
        self,
        ticket_id: int,
        student_id: int,
        category: str,
        description: str,
    ):
        self.ticket_id = ticket_id
        self.student_id = student_id
        self.category = category.strip().title()
        self.description = description.strip()
        self.status = TicketStatus.OPEN
        self.resolution_note: str | None = None

    # ── Behaviour ────────────────────────────

    def resolve(self, note: str) -> None:
        """
        Mark this ticket as RESOLVED and store the resolution note.

        Args:
            note (str): A short explanation of how the issue was handled.
        Raises:
            ValueError: If the ticket is already resolved.
        """
        if self.status == TicketStatus.RESOLVED:
            raise ValueError(f"Ticket #{self.ticket_id} is already resolved.")
        self.status = TicketStatus.RESOLVED
        self.resolution_note = note.strip()

    # ── Display ──────────────────────────────

    def __str__(self) -> str:
        base = (
            f"Ticket #{self.ticket_id} | Student ID: {self.student_id} | "
            f"[{self.category}] | Status: {self.status.value}\n"
            f"   Description: {self.description}"
        )
        if self.resolution_note:
            base += f"\n   Resolution : {self.resolution_note}"
        return base
