"""Inputs showcase example.

Shows the `TextInput` component with a few validation rules.
"""
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
import sys
import pathlib

# When examples are run directly from the repo, ensure the project root is on sys.path
try:
    from bfs_component.ui.components import TextInput, StyledLineEdit
except ModuleNotFoundError:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    from bfs_component.ui.components import TextInput, StyledLineEdit


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

    # --- direct StyledLineEdit showcase (screenshot-friendly) ---
    layout.addSpacing(12)
    lbl_demo = QLabel("Focused gradient demo:")
    layout.addWidget(lbl_demo)

    demo_input = StyledLineEdit()
    demo_input.setPlaceholderText("Click or press 'Focus' to see the glow")
    layout.addWidget(demo_input)

    # small gradient swatch for quick visual testing (10x10)

    class GradientSwatch(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            # small: 20x50 as requested; expanded preview will be 100x120
            self._small_w = 20
            self._small_h = 50
            self._large_w = 100
            self._large_h = 120
            self.setFixedSize(self._small_w, self._small_h)
            self._expanded = False

        def mousePressEvent(self, event):
            # toggle size between small and large for easier inspection
            self._expanded = not self._expanded
            if self._expanded:
                self.setFixedSize(self._large_w, self._large_h)
            else:
                self.setFixedSize(self._small_w, self._small_h)
            self.update()

        def paintEvent(self, event):
            from PySide6.QtGui import QPainter, QLinearGradient, QColor
            from PySide6.QtCore import QRectF

            p = QPainter(self)
            p.setRenderHint(QPainter.Antialiasing)
            r = QRectF(self.rect())
            grad = QLinearGradient(r.topLeft(), r.bottomRight())
            grad.setColorAt(0.0, QColor('#00C6FF'))
            grad.setColorAt(0.5, QColor('#9047FF'))
            grad.setColorAt(1.0, QColor('#FF6F61'))
            p.fillRect(r, grad)
            p.end()

    lbl_swatch = QLabel("Gradient swatch (click to toggle size):")
    layout.addWidget(lbl_swatch)
    sw = GradientSwatch()
    layout.addWidget(sw)

    btn_row = QHBoxLayout()
    btn_focus = QPushButton("Focus")
    btn_unfocus = QPushButton("Unfocus")

    def do_focus():
        demo_input.setFocus()

    def do_unfocus():
        # move focus to the submit button to remove focus from input
        btn.setFocus()

    btn_focus.clicked.connect(do_focus)
    btn_unfocus.clicked.connect(do_unfocus)
    btn_row.addWidget(btn_focus)
    btn_row.addWidget(btn_unfocus)
    layout.addLayout(btn_row)

    # autofocus demo input so a screenshot will capture the focused state
    demo_input.setFocus()

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
