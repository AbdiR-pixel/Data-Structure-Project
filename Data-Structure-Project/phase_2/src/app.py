"""
app.py — ServiceDeskApp: the controller that owns the registry,
         the ticket store, and all menu-driven UI methods.

Each menu option calls a dedicated *_ui() method.  Business logic
lives in registry.py / reports.py; input helpers in validation.py.
"""

from src.models import Student, Ticket, TicketStatus
from src.registry import (
    add_student,
    update_student,
    delete_student,
    find_by_id,
    search_by_name,
)
from src.reports import print_class_report
from src.validation import (
    StudentNotFoundError,
    DuplicateStudentError,
    TicketNotFoundError,
    ValidationError,
    read_int,
    read_float,
    read_non_empty,
)


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def _separator(char: str = "─", width: int = 50) -> None:
    print(char * width)


def _ok(msg: str) -> None:
    print(f"  ✔  {msg}")


def _warn(msg: str) -> None:
    print(f"  ✘  {msg}")


# ─────────────────────────────────────────────
#  Application Class
# ─────────────────────────────────────────────

class ServiceDeskApp:
    """
    Main application controller for the Student Service Desk.

    Owns:
        _students (dict): {student_id (int): Student}
        _tickets  (dict): {ticket_id  (int): Ticket}
        _next_ticket_id (int): auto-increment counter.
    """

    def __init__(self):
        self._students: dict[int, Student] = {}
        self._tickets: dict[int, Ticket]   = {}
        self._next_ticket_id: int = 1

    # ════════════════════════════════════════
    #  Student Operations
    # ════════════════════════════════════════

    def add_student_ui(self) -> None:
        """
        Prompt the user for student details and add a new record.

        Warns if the ID already exists and asks for explicit confirmation
        before overwriting.  Validates all fields before storing.
        """
        _separator()
        print("  ADD STUDENT")
        _separator()
        try:
            sid = read_int("  Student ID   : ")
            name  = read_non_empty("  Name         : ")
            phone = read_non_empty("  Phone        : ")
            mid   = read_float("  Midterm score: ")
            fin   = read_float("  Final score  : ")
        except ValidationError as e:
            _warn(str(e))
            return

        # Check for existing ID with confirmation
        overwrite = False
        if sid in self._students:
            confirm = input(
                f"  Student ID {sid} already exists. Overwrite? (yes/no): "
            ).strip().lower()
            if confirm != "yes":
                _warn("Operation cancelled. Existing record kept unchanged.")
                return
            overwrite = True

        try:
            student = add_student(
                self._students, sid, name, phone, mid, fin, overwrite=overwrite
            )
            _ok(f"Student added: {student}")
        except (DuplicateStudentError, ValidationError) as e:
            _warn(str(e))

    def update_student_ui(self) -> None:
        """
        Prompt for a student ID, a field name, and a new value, then update
        the record.  Re-validates the new value before applying the change.
        """
        _separator()
        print("  UPDATE STUDENT")
        _separator()
        try:
            sid = read_int("  Student ID   : ")
        except ValidationError as e:
            _warn(str(e))
            return

        try:
            student = find_by_id(self._students, sid)
        except StudentNotFoundError as e:
            _warn(str(e))
            return

        print(f"  Current record: {student}")
        print("  Fields: name | phone | midterm | final")
        field = input("  Field to update: ").strip().lower()
        new_val_raw = input(f"  New value for '{field}': ").strip()

        try:
            updated = update_student(self._students, sid, field, new_val_raw)
            _ok(f"Record updated: {updated}")
        except (StudentNotFoundError, ValidationError) as e:
            _warn(str(e))

    def delete_student_ui(self) -> None:
        """
        Prompt for a student ID and remove the record after confirmation.
        Informs the user if the ID does not exist.
        """
        _separator()
        print("  DELETE STUDENT")
        _separator()
        try:
            sid = read_int("  Student ID to delete: ")
        except ValidationError as e:
            _warn(str(e))
            return

        if sid not in self._students:
            _warn(f"No student with ID {sid}. Nothing deleted.")
            return

        confirm = input(
            f"  Delete student '{self._students[sid].name}' (ID {sid})? (yes/no): "
        ).strip().lower()
        if confirm != "yes":
            _warn("Deletion cancelled.")
            return

        try:
            removed = delete_student(self._students, sid)
            _ok(f"Deleted: {removed.name} (ID {removed.student_id})")
        except StudentNotFoundError as e:
            _warn(str(e))

    def find_student_ui(self) -> None:
        """
        Prompt for a student ID and display the full record if found,
        or an informative message if not.
        """
        _separator()
        print("  FIND STUDENT BY ID")
        _separator()
        try:
            sid = read_int("  Student ID: ")
        except ValidationError as e:
            _warn(str(e))
            return

        try:
            student = find_by_id(self._students, sid)
            print(f"\n  {student}\n")
        except StudentNotFoundError as e:
            _warn(str(e))

    def search_by_name_ui(self) -> None:
        """
        Prompt for a partial name string and list all matching students.
        Uses case-insensitive substring matching (lower(), strip(), 'in').
        """
        _separator()
        print("  SEARCH BY NAME")
        _separator()
        query = input("  Enter name (or part of it): ").strip()
        if not query:
            _warn("Search query cannot be empty.")
            return

        results = search_by_name(self._students, query)
        if not results:
            _warn(f"No students matched '{query}'.")
        else:
            print(f"\n  Found {len(results)} result(s) for '{query}':")
            for s in results:
                print(f"    {s}")
            print()

    def print_class_report_ui(self) -> None:
        """
        Print the full class report including size, averages, top/bottom
        students, pass rate, and grade distribution.
        """
        print_class_report(self._students)

    # ════════════════════════════════════════
    #  Ticket Operations
    # ════════════════════════════════════════

    def create_ticket_ui(self) -> None:
        """
        Create a new service ticket linked to an existing student.

        Verifies that the student ID exists before creating the ticket.
        Assigns a unique auto-incremented ticket ID.
        """
        _separator()
        print("  CREATE SERVICE TICKET")
        _separator()
        try:
            sid = read_int("  Student ID      : ")
        except ValidationError as e:
            _warn(str(e))
            return

        if sid not in self._students:
            _warn(
                f"No student with ID {sid}. "
                "Ticket cannot be created for an unknown student."
            )
            return

        print(f"  Student found: {self._students[sid].name}")
        print(
            "  Categories: Grade Inquiry | Certificate Request | "
            "Update Info | Other"
        )
        try:
            category    = read_non_empty("  Category        : ")
            description = read_non_empty("  Description     : ")
        except ValidationError as e:
            _warn(str(e))
            return

        tid = self._next_ticket_id
        ticket = Ticket(tid, sid, category, description)
        self._tickets[tid] = ticket
        self._next_ticket_id += 1
        _ok(f"Ticket #{tid} created for student {sid} ({self._students[sid].name}).")

    def list_tickets_ui(self) -> None:
        """
        List all tickets, with an optional filter by status (OPEN / RESOLVED).

        Prints a formatted view of each matching ticket.
        """
        _separator()
        print("  LIST TICKETS")
        _separator()
        if not self._tickets:
            print("  No tickets in the system yet.")
            return

        print("  Filter: (1) All   (2) OPEN only   (3) RESOLVED only")
        choice = input("  Choice: ").strip()

        if choice == "2":
            target = TicketStatus.OPEN
            label  = "OPEN"
        elif choice == "3":
            target = TicketStatus.RESOLVED
            label  = "RESOLVED"
        else:
            target = None
            label  = "ALL"

        filtered = [
            t for t in self._tickets.values()
            if target is None or t.status == target
        ]

        if not filtered:
            _warn(f"No {label} tickets found.")
            return

        print(f"\n  Showing {len(filtered)} {label} ticket(s):\n")
        for t in filtered:
            print(f"  {t}")
            print()

    def resolve_ticket_ui(self) -> None:
        """
        Mark an existing ticket as RESOLVED and store a resolution note.

        Requires the ticket to be in OPEN status; shows an error otherwise.
        """
        _separator()
        print("  RESOLVE TICKET")
        _separator()
        try:
            tid = read_int("  Ticket ID to resolve: ")
        except ValidationError as e:
            _warn(str(e))
            return

        if tid not in self._tickets:
            _warn(f"No ticket with ID {tid}.")
            return

        ticket = self._tickets[tid]
        if ticket.status == TicketStatus.RESOLVED:
            _warn(f"Ticket #{tid} is already resolved.")
            return

        print(f"  {ticket}")
        try:
            note = read_non_empty("  Resolution note: ")
        except ValidationError as e:
            _warn(str(e))
            return

        try:
            ticket.resolve(note)
            _ok(f"Ticket #{tid} resolved.")
        except ValueError as e:
            _warn(str(e))


# ─────────────────────────────────────────────
#  Menu Loop
# ─────────────────────────────────────────────

def run_menu(app: ServiceDeskApp) -> None:
    """
    Run the main interactive menu loop until the user selects Exit.

    Uses a while-loop and try/except so the program never crashes on
    bad input or unexpected errors.  Invalid choices raise ValueError
    caught by the outer handler.

    Args:
        app (ServiceDeskApp): The application instance to drive.
    """
    while True:
        print("\n" + "═" * 50)
        print("   STUDENT SERVICE DESK & REGISTRY — Phase 2")
        print("═" * 50)
        print("   1) Add student")
        print("   2) Update student")
        print("   3) Delete student")
        print("   4) Find student by ID")
        print("   5) Search by name")
        print("   6) Class report")
        print("   7) Create service ticket")
        print("   8) List tickets (filter by status)")
        print("   9) Resolve ticket")
        print("   0) Exit")
        print("─" * 50)

        choice = input("   Choice: ").strip()

        try:
            if choice == "1":
                app.add_student_ui()
            elif choice == "2":
                app.update_student_ui()
            elif choice == "3":
                app.delete_student_ui()
            elif choice == "4":
                app.find_student_ui()
            elif choice == "5":
                app.search_by_name_ui()
            elif choice == "6":
                app.print_class_report_ui()
            elif choice == "7":
                app.create_ticket_ui()
            elif choice == "8":
                app.list_tickets_ui()
            elif choice == "9":
                app.resolve_ticket_ui()
            elif choice == "0":
                print("\n  Goodbye!\n")
                break
            else:
                raise ValueError(f"'{choice}' is not a valid menu choice.")
        except Exception as e:
            print(f"\n  ERROR: {e}\n")
