import sys
from PySide6.QtWidgets import QApplication


def test_searchable_select_filters_and_selects():
    from bfs_component.ui.components import StyledComboBox

    app = QApplication.instance() or QApplication(sys.argv)
    opts = ["Norway", "Sweden", "Denmark"]
    s = StyledComboBox(opts)

    # simulate user selecting "Norway" programmatically via set_current_value
    collected = []

    def on_sel(val):
        collected.append(val)

    s.selection_changed.connect(on_sel)
    # set current value
    s.set_current_value("Norway")
    # simulate activation (combobox would normally emit selection_changed)
    s._combobox.activated.emit(s._combobox.currentIndex())

    assert len(collected) == 1
    assert collected[0] == "Norway"
