"""Cards showcase example.

Run this script to open a window that displays multiple Card variants.
This acts like a small storybook for manual visual testing.
"""
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap
import sys
import pathlib

# Make examples runnable from repo root by adding project to sys.path when needed
try:
    from bfs_component.ui.components import Card, ContactCard, CompanyCard
except ModuleNotFoundError:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    from bfs_component.ui.components import Card, ContactCard, CompanyCard


def make_sample_cards():
    cards = []

    # Simple Card with header/body/footer
    c1 = Card()
    c1.set_header(QLabel("Simple Card"))
    c1.set_body(QLabel("This is a simple card with plain text body."))
    c1.set_footer(QLabel("Footer text"))
    cards.append(c1)

    # ContactCard example (initials, name, role, email)
    contact = ContactCard("JD", "Jane Doe", "Engineer", "jane@example.com")
    cards.append(contact)

    # CompanyCard example (uses name and optional tags)
    company = CompanyCard("Acme Corp", tags=["Technology", "Active"])
    cards.append(company)

    # A separate long-text Card to show wrapping and sizing
    long_card = Card()
    long_card.set_header(QLabel("Long text card"))
    long_body = QLabel(
        "Acme Corporation provides everything you need. "
        "This card is intentionally longer to demonstrate wrapping and sizing. "
        "It should wrap and increase the card height as needed.")
    long_body.setWordWrap(True)
    long_card.set_body(long_body)
    cards.append(long_card)

    # Card with custom widget in header (logo)
    c4 = Card()
    logo = QLabel()
    logo.setPixmap(QPixmap())
    logo.setText("[Logo]")
    c4.set_header(logo)
    body = QLabel("Card with logo header and a longer piece of text to show layout.")
    body.setWordWrap(True)
    c4.set_body(body)
    cards.append(c4)

    return cards


def main(argv):
    app = QApplication(argv)
    win = QWidget()
    win.setWindowTitle("Cards Showcase")
    outer = QVBoxLayout(win)

    row = QHBoxLayout()
    for card in make_sample_cards():
        card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        row.addWidget(card)

    outer.addLayout(row)
    win.setLayout(outer)
    win.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
