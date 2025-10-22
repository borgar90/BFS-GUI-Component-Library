import pytest

from PySide6.QtWidgets import QApplication

from bfs_component.ui.components import RadioGroup


@pytest.fixture(autouse=True)
def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_radio_group_happy_path(qtbot=None):
    rg = RadioGroup(items=[('a', 'Option A'), ('b', 'Option B'), ('c', 'Option C')])

    captured = []

    def on_change(v):
        captured.append(v)

    rg.selection_changed.connect(on_change)

    # programmatic set
    assert rg.set_value('b') is True
    assert rg.get_value() == 'b'
    # selecting another
    assert rg.set_value('c') is True
    assert rg.get_value() == 'c'

    # ensure selection_changed emitted correct values
    # Note: set_value triggers button.setChecked which will emit selection_changed
    assert 'b' in captured and 'c' in captured


def test_set_invalid_value_returns_false():
    rg = RadioGroup(items=['one', 'two'])
    # setting a value that doesn't exist should return False and not change selection
    prev = rg.get_value()
    assert rg.set_value('does-not-exist') is False
    assert rg.get_value() == prev
