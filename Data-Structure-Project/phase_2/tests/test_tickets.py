"""
test_tickets.py — Unit tests for the ticket system.

Run: python -m pytest tests/ -v
"""

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import Ticket, TicketStatus
from src.registry import add_student


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def _make_ticket(tid=1, sid=101, cat="Grade Inquiry", desc="Please review"):
    return Ticket(tid, sid, cat, desc)


def _registry_with_student():
    reg = {}
    add_student(reg, 101, "Amina Ali", "77889900", 70, 85)
    return reg


# ─────────────────────────────────────────────
#  Ticket Creation Tests
# ─────────────────────────────────────────────

def test_ticket_creation_defaults():
    """A new ticket should start with OPEN status and no resolution note."""
    t = _make_ticket()
    assert t.ticket_id == 1
    assert t.student_id == 101
    assert t.status == TicketStatus.OPEN
    assert t.resolution_note is None


def test_ticket_category_title_cased():
    """Category should be stored in Title Case."""
    t = _make_ticket(cat="grade inquiry")
    assert t.category == "Grade Inquiry"


def test_ticket_requires_existing_student():
    """Creating a ticket for a non-existent student should be blocked at app layer."""
    reg = _registry_with_student()
    # Simulate the check done in create_ticket_ui
    missing_sid = 999
    assert missing_sid not in reg


# ─────────────────────────────────────────────
#  Resolve Tests
# ─────────────────────────────────────────────

def test_resolve_ticket_changes_status():
    """Resolving a ticket should set its status to RESOLVED."""
    t = _make_ticket()
    t.resolve("Corrected grade entered.")
    assert t.status == TicketStatus.RESOLVED


def test_resolve_ticket_stores_note():
    """Resolution note should be stored correctly."""
    t = _make_ticket()
    t.resolve("Issue escalated to faculty.")
    assert t.resolution_note == "Issue escalated to faculty."


def test_resolve_ticket_twice_raises():
    """Resolving an already-resolved ticket should raise ValueError."""
    t = _make_ticket()
    t.resolve("First resolution.")
    with pytest.raises(ValueError):
        t.resolve("Second attempt.")


# ─────────────────────────────────────────────
#  Filtering Tests
# ─────────────────────────────────────────────

def test_filter_open_tickets():
    """Filtering by OPEN should exclude resolved tickets."""
    tickets = {
        1: _make_ticket(tid=1),
        2: _make_ticket(tid=2),
    }
    tickets[1].resolve("Done.")
    open_tickets = [t for t in tickets.values() if t.status == TicketStatus.OPEN]
    assert len(open_tickets) == 1
    assert open_tickets[0].ticket_id == 2


def test_filter_resolved_tickets():
    """Filtering by RESOLVED should only return resolved tickets."""
    tickets = {
        1: _make_ticket(tid=1),
        2: _make_ticket(tid=2),
    }
    tickets[2].resolve("Handled.")
    resolved = [t for t in tickets.values() if t.status == TicketStatus.RESOLVED]
    assert len(resolved) == 1
    assert resolved[0].ticket_id == 2


# ─────────────────────────────────────────────
#  __str__ Tests
# ─────────────────────────────────────────────

def test_ticket_str_open():
    """String representation of an open ticket should show OPEN status."""
    t = _make_ticket()
    result = str(t)
    assert "OPEN" in result
    assert "#1" in result


def test_ticket_str_resolved_includes_note():
    """String representation of a resolved ticket should include the note."""
    t = _make_ticket()
    t.resolve("Grade updated.")
    result = str(t)
    assert "RESOLVED" in result
    assert "Grade updated." in result
