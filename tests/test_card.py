import sys
import pytest
from PySide6.QtWidgets import QApplication, QLabel, QWidget


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication(sys.argv)
    yield app


def test_card_slots(qapp):
    from bfs_component.ui.components import Card

    card = Card()
    header = QLabel("H")
    body = QLabel("B")
    footer = QLabel("F")
    card.set_header(header)
    card.set_body(body)
    card.set_footer(footer)
    # ensure attributes exist
    assert hasattr(card, "_header")
    assert hasattr(card, "_body")
    assert hasattr(card, "_footer")
