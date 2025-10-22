import sys
import pytest

from PySide6.QtWidgets import QApplication, QLabel


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication(sys.argv)
    yield app


def test_set_content_and_clear(qapp):
    from bfs_component.ui.main_window import MainWindow

    win = MainWindow()
    widget = QLabel("hello")
    win.set_content(widget)
    assert hasattr(win, "_content_holder") and win._content_holder is not None
    # clear and ensure removed
    win.clear_content()
    assert not hasattr(win, "_content_holder") or win._content_holder is None


def test_set_title_and_status(qapp, capsys):
    from bfs_component.ui.main_window import MainWindow

    win = MainWindow()
    win.set_title("Test Title")
    # set a status message with a short timeout
    win.set_status_message("Loading...", timeout=10)
    # status_message prints were removed; ensure no exception and status visible
    assert hasattr(win, "_status_bar")
