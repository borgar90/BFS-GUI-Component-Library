# BFS Component Library (Python)


Minimal scaffold for BFS component library in Python.

Structure:

- bfs_component/ - package source
- tests/ - unit tests

Usage:

pip install -e .

Running the GUI (requires PySide6):

python run_app.py

API documentation (MainWindow / TitleBar)
-------------------------------------

MainWindow is a frameless window with a customizable title bar and a content slot.

Key methods

- MainWindow.set_content(widget: QWidget)
	- Replace the content area with the provided widget. The content is wrapped in a styled off-white holder.

- MainWindow.clear_content()
	- Remove any existing content holder and children.

- MainWindow.set_title(title: str)
	- Update the title shown in the custom title bar and the native window title.

- MainWindow.set_status_message(message: str, timeout: int = 0)
	- Show a status message in the status bar. timeout is in milliseconds.

- MainWindow.add_toolbar(widget: QWidget)
	- Add a widget to the titlebar area (right-aligned).

- MainWindow.add_menu(menu: QMenu)
	- Add a QMenu to the titlebar menu area. (Basic menu bar support.)

TitleBar supports logo injection via TitleBar.set_logo(pixmap|path|widget)

Examples
--------

Simple example (injecting a label as content and a logo):

```python
from bfs_component.ui.main_window import MainWindow
from PySide6.QtWidgets import QLabel

win = MainWindow(logo='assets/logo.png')
win.set_title('Acme Corporation')
win.set_content(QLabel('This is the content area'))
win.set_status_message('Ready', timeout=3000)
win.show()
```

Packaging notes
---------------

The package is configured with a minimal `pyproject.toml`. When ready to publish, update metadata (authors, license) and use `python -m build` to create wheels.

Testing
-------

Run unit tests with pytest in the virtual environment:

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q
```


