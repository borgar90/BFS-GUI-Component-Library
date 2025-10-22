"""Launcher for the BFS Component Library GUI using PySide6"""
import sys

from PySide6.QtWidgets import QApplication
from bfs_component.ui.main_window import MainWindow
from pathlib import Path


def main(argv=None):
    argv = argv or sys.argv
    app = QApplication(argv)
    # try to inject a project logo from assets/logo.png if present
    logo_path = Path(__file__).parent / "assets" / "logo.png"
    if logo_path.exists():
        win = MainWindow(logo=str(logo_path))
    else:
        win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
