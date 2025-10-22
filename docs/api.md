# API Reference

This page lists the main classes and methods in the package.

## MainWindow (bfs_component.ui.main_window.MainWindow)

Key methods:

- `set_content(widget: QWidget)` — insert a widget into the off-white content holder.
- `clear_content()` — remove existing content.
- `set_title(title: str)` — update the title label.
- `set_status_message(message: str, timeout: int = 0)` — show a status message; timeout in ms.

## TitleBar (bfs_component.ui.main_window.TitleBar)

Supports `set_logo(path|pixmap|widget)` and contains a `QMenuBar` accessible at `titlebar._menu_bar`.

## MainFrame (bfs_component.ui.components.MainFrame)

Composed helper widgets: `HeaderWidget`, `CompanyCard`, `ContactCard`.

See inline docstrings for detailed signatures and behaviors.
