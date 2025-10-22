from bfs_component.ui.components import TextInput
from PySide6.QtWidgets import QApplication
import sys

# Ensure a QApplication exists for widget construction during tests
_app = QApplication.instance() or QApplication(sys.argv)


def test_textinput_basic():
    t = TextInput("Test", placeholder="Enter")
    assert t.text() == ""
    t.set_text("abc")
    assert t.text() == "abc"


def test_textinput_required_validation():
    t = TextInput("Required")
    t.set_required(True, "Must provide value")
    t.set_text("")
    assert not t.is_valid()
    assert not t.validate(show_error=False)


def test_textinput_regex_validation():
    t = TextInput("Email")
    t.set_validation_regex(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", "Bad email")
    t.set_text("notanemail")
    assert not t.is_valid()
    t.set_text("name@example.com")
    assert t.is_valid()
