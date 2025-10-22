from bfs_component.ui.main_window import MainWindow
from PySide6.QtWidgets import QLabel


def run():
    win = MainWindow(logo='assets/logo.png')
    win.set_title('Acme Corporation')
    win.set_content(QLabel('This is the content area'))
    win.set_status_message('Ready', timeout=3000)
    win.show()


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    run()
    sys.exit(app.exec())
