"""
main.py — Entry point for the Student Service Desk & Registry application.

Run:
    python main.py

The program preloads a few sample students so you can test features
immediately without entering data manually.
"""

from src.app import ServiceDeskApp, run_menu
from src.registry import add_student


def _load_sample_data(app: ServiceDeskApp) -> None:
    """Load a small set of sample students for quick testing."""
    samples = [
        (101, "Amina Ali",      "77889900", 70,  85),
        (102, "Youssouf Omar",  "77112233", 85, 100),
        (103, "Fatima Hassan",  "77334455", 55,  60),
        (104, "Ibrahim Warsame","77556677", 90,  95),
        (105, "Hodan Abdi",     "77001122", 45,  50),
    ]
    for sid, name, phone, mid, fin in samples:
        add_student(app._students, sid, name, phone, mid, fin)
    print("  (Sample data loaded: 5 students — IDs 101–105)")


if __name__ == "__main__":
    app = ServiceDeskApp()
    _load_sample_data(app)
    run_menu(app)
