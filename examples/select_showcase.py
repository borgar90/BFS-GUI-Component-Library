"""SearchableSelect showcase.

Run to interactively test filtering and selection.
"""
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
import sys
import pathlib

try:
    from bfs_component.ui.components import SearchableSelect
except ModuleNotFoundError:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    import sys
    sys.path.insert(0, str(repo_root))
    from bfs_component.ui.components import SearchableSelect

COUNTRIES = [
    "Norway",
    "Sweden",
    "Denmark",
    "Finland",
    "Iceland",
    "United Kingdom",
    "United States",
    "Germany",
]


def main(argv):
    app = QApplication(argv)
    win = QWidget()
    win.setWindowTitle("Select Showcase")
    layout = QVBoxLayout(win)

    sel = SearchableSelect(COUNTRIES, placeholder="Type to filter countries")
    layout.addWidget(sel)

    chosen = QLabel("Selected: none")
    layout.addWidget(chosen)

    def on_select(val):
        chosen.setText(f"Selected: {val}")

    sel.selection_changed.connect(on_select)

    win.setLayout(layout)
    win.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
