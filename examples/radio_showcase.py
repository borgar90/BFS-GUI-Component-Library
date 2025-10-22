"""Small interactive example for RadioGroup usage.

Run this file directly with: python examples/radio_showcase.py
"""
import sys
import pathlib
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

try:
    from bfs_component.ui.components import RadioGroup
except ModuleNotFoundError:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    from bfs_component.ui.components import RadioGroup


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    win = QWidget()
    win.setWindowTitle("RadioGroup Showcase")
    layout = QVBoxLayout()

    label = QLabel("Choose an environment:")
    layout.addWidget(label)

    rg = RadioGroup(items=[('dev', 'Development'), ('stg', 'Staging'), ('prod', 'Production')])
    layout.addWidget(rg)

    selected = QLabel("Selected: None")
    layout.addWidget(selected)

    def on_change(val):
        selected.setText(f"Selected: {val}")

    rg.selection_changed.connect(on_change)

    # programmatic interaction
    btn_set_prod = QPushButton("Select Production")
    def set_prod():
        rg.set_value('prod')
    btn_set_prod.clicked.connect(set_prod)
    layout.addWidget(btn_set_prod)

    btn_get = QPushButton("Get current value")
    def get_val():
        v = rg.get_value()
        selected.setText(f"Selected: {v}")
    btn_get.clicked.connect(get_val)
    layout.addWidget(btn_get)

    win.setLayout(layout)
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
