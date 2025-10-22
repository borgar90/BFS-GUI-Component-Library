"""Lightweight visual test: render the cards showcase to an image file.

This test creates the showcase window offscreen, grabs a screenshot and writes
it to a temporary file. The assertion ensures the output image exists and is
non-empty. This is a simple smoke test to catch rendering regressions.
"""
import tempfile
import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap


def test_cards_showcase_screenshot(tmp_path):
    from examples import cards_showcase

    app = QApplication.instance() or QApplication(sys.argv)

    # Build the UI and show it briefly
    win = cards_showcase.main if hasattr(cards_showcase, 'main') else None
    # Use the same builder: create a QWidget like the example
    widget = cards_showcase.__dict__.get('make_sample_cards')
    # make_sample_cards returns Card widgets; we need a container like the example
    # Instead of reconstructing the full example window, import and instantiate the
    # example window by running its main() but without exec loop. We'll create the
    # QWidget layout manually similar to the example.
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

    container = QWidget()
    container.setWindowTitle("Cards Showcase - Test")
    outer = QVBoxLayout(container)
    row = QHBoxLayout()
    cards = cards_showcase.make_sample_cards()
    for c in cards:
        row.addWidget(c)
    outer.addLayout(row)
    container.setLayout(outer)

    # Render offscreen: show, process events and grab
    container.show()
    app.processEvents()

    pix = QPixmap(container.size())
    container.render(pix)

    tmp_file = tmp_path / "cards_showcase.png"
    saved = pix.save(str(tmp_file))
    assert saved, "Failed to save screenshot"
    assert tmp_file.exists()
    assert tmp_file.stat().st_size > 0
