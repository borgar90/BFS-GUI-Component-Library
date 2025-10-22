"""Inputs showcase example.

Shows the `TextInput` component with a few validation rules.
"""
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import sys
import pathlib

# When examples are run directly from the repo, ensure the project root is on sys.path
try:
    from bfs_component.ui.components import TextInput
except ModuleNotFoundError:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    from bfs_component.ui.components import TextInput


def main(argv):
    app = QApplication(argv)
    win = QWidget()
    win.setWindowTitle("Inputs Showcase")
    layout = QVBoxLayout(win)

    name = TextInput("Name", placeholder="Full name")
    name.set_required(True)
    name.set_validation_regex(r"^[A-Za-z ]+$", "Only letters and spaces allowed")
    layout.addWidget(name)

    email = TextInput("Email", placeholder="you@example.com")
    email.set_validation_regex(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", "Enter a valid email")
    layout.addWidget(email)

    status = QLabel("")
    layout.addWidget(status)

    def on_submit():
        ok = name.validate(True) and email.validate(True)
        status.setText("All good!" if ok else "Please fix errors.")

    btn = QPushButton("Submit")
    btn.clicked.connect(on_submit)
    layout.addWidget(btn)

    win.setLayout(layout)
    win.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
