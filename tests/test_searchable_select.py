import sys
from PySide6.QtWidgets import QApplication


def test_searchable_select_filters_and_selects():
    from bfs_component.ui.components import SearchableSelect

    app = QApplication.instance() or QApplication(sys.argv)
    opts = ["Norway", "Sweden", "Denmark"]
    s = SearchableSelect(opts)

    # simulate typing 'nor'
    s._input.setText("nor")
    s._on_text_changed("nor")

    # After filtering, at least Norway should appear as first item
    items = [s._list.item(i).text() for i in range(s._list.count())]
    assert any("norway" == it.lower() or "nor" in it.lower() for it in items)

    # select the first item and ensure signal is emitted (connect to local collector)
    collected = []

    def on_sel(val):
        collected.append(val)

    s.selection_changed.connect(on_sel)
    # select via internal helper
    if s._list.count() > 0:
        s._select_item(s._list.item(0))

    assert len(collected) == 1
    assert collected[0] in opts
