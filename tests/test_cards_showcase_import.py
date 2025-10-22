"""Smoke test: import and construct showcase widgets without starting the event loop."""
from PySide6.QtWidgets import QApplication
import sys


def test_import_cards_showcase():
    # Import inside the test so any UI issues surface here
    from examples import cards_showcase
    # Construct widgets (this creates a QApplication internally when run as script,
    # but here we ensure a QApplication exists for widget creation)
    app = QApplication.instance() or QApplication(sys.argv)
    # Build the sample cards list
    cards = cards_showcase.make_sample_cards()
    assert isinstance(cards, list)
    assert len(cards) >= 3
