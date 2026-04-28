# Student Service Desk & Registry (Phase 1 + Phase 2)

## How to run
```bash
python main.py
```

No external dependencies — only the Python standard library is used.  
Tests require **pytest**: `pip install pytest`

---

## Features implemented

### Phase 1 (Data Modelling)
- Add / Update / Delete student records
- Find student by ID
- Search by name (case-insensitive substring)
- Class report: size, average, top/bottom student, pass rate, grade distribution

### Phase 2 (OOP + Exceptions + Tickets)
- All Phase 1 features refactored into `Student` / `Ticket` classes
- Service ticket system: Create → List (filter) → Resolve
- Robust menu loop (never crashes on bad input)
- Custom exceptions: `StudentNotFoundError`, `DuplicateStudentError`,
  `TicketNotFoundError`, `ValidationError`

---

## Project structure
```
project_phase2/
├── main.py               ← entry point (loads sample data + starts menu)
├── README.md
├── src/
│   ├── models.py         ← Student, Ticket, TicketStatus
│   ├── registry.py       ← CRUD operations (add/update/delete/find/search)
│   ├── validation.py     ← custom exceptions + field validators + safe readers
│   ├── reports.py        ← statistics & formatted class report
│   └── app.py            ← ServiceDeskApp controller + run_menu()
└── tests/
    ├── test_students.py  ← 18 student-registry tests
    └── test_tickets.py   ← 10 ticket-system tests
```

---

## Example interactions

### 1 — Add a student with messy phone input
```
Choice: 1
Student ID   : 201
Name         : fatima hassan
Phone        : 77-33 44 55
Midterm score: 72
Final score  : 88
✔  Student added: ID=201 | Fatima Hassan | Phone: 77334455 | Midterm: 72.0  Final: 88.0  Term: 81.6 (B)
```

### 2 — Search by partial name
```
Choice: 5
Enter name (or part of it): ali
Found 1 result(s) for 'ali':
  ID=101 | Amina Ali | Phone: 77889900 | Midterm: 70.0  Final: 85.0  Term: 79.0 (C)
```

### 3 — Class report
```
Choice: 6
══════════════════════════════════════════════════
         CLASS REPORT — Student Registry
══════════════════════════════════════════════════
  Class size    : 5
  Average grade : 72.5
  Highest grade : 93.0  → Ibrahim Warsame (ID 104)
  Lowest grade  : 48.0  → Hodan Abdi (ID 105)
  Pass rate (≥60): 60.0%

  Grade Distribution:
    A: █  (1)
    B: ██  (2)
    C: █  (1)
    D: (0)
    F: █  (1)
```

### 4 — Create + resolve a ticket
```
Choice: 7  → Student ID: 101 → Category: Grade Inquiry → Description: Midterm grade seems wrong
Choice: 8  → Filter: OPEN only  →  shows Ticket #1
Choice: 9  → Ticket ID: 1 → Resolution note: Rechecked — grade confirmed correct
Choice: 8  → Filter: RESOLVED  →  shows Ticket #1 as RESOLVED
```

---

## Validation rules
| Field      | Rule                                      |
|------------|-------------------------------------------|
| Student ID | Positive integer; unique on add           |
| Name       | Non-empty; stored in Title Case           |
| Phone      | Digits only (spaces & dashes auto-removed)|
| Midterm    | Numeric, 0 – 100                          |
| Final      | Numeric, 0 – 100                          |

---

## Running the tests
```bash
python -m pytest tests/ -v
```
Expected: **28 tests**, all passing.

---

## External references
- Python official docs: https://docs.python.org/3/
- `enum` module: https://docs.python.org/3/library/enum.html
