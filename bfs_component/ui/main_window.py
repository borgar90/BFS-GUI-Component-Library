"""Main window for BFS Component Library using PySide6.

Provides a frameless `MainWindow` with a customizable `TitleBar`, menu area,
search field, and a content injection API. Designed to be used as a component
that can be embedded or run as a standalone app.

Public API highlights:
- MainWindow.set_content(widget)
- MainWindow.clear_content()
- MainWindow.set_title(title)
- MainWindow.set_status_message(message, timeout_ms)
"""
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont, QColor

from bfs_component.ui.components import MainFrame


class TitleBar(QWidget):
    """Custom title bar widget used by `MainWindow`.

    Supports logo injection via `set_logo`, displays a title label, a menu
    bar area, a search field and standard window control buttons.
    """
    def __init__(self, parent=None, title: str = "BFS", logo=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(56)
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        # logo placeholder (can be replaced by injection)
        self._logo_widget = QLabel("")
        # increase base size by 50% (from 72x36 -> approx 108x54)
        self._logo_widget.setFixedHeight(54)
        self._logo_widget.setFixedWidth(108)
        self._logo_widget.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        layout.addWidget(self._logo_widget)
        # small gap between logo and search field
        from PySide6.QtWidgets import QSpacerItem, QSizePolicy
        layout.addItem(QSpacerItem(12, 1, QSizePolicy.Fixed, QSizePolicy.Minimum))
        if logo is not None:
            self.set_logo(logo)

        # simple menu bar area (inserted before the title)
        from PySide6.QtWidgets import QMenuBar
        self._menu_bar = QMenuBar()
        self._menu_bar.setStyleSheet("QMenuBar{background: transparent; color: white;} QMenuBar::item{spacing: 6px; padding: 4px 8px;}")
        self._menu_bar.setFixedHeight(28)
        layout.addWidget(self._menu_bar)

        # title label
        self._title_label = QLabel(title)
        self._title_label.setFont(QFont("Segoe UI", 12, QFont.DemiBold))
        self._title_label.setStyleSheet("color: white;")
        layout.addWidget(self._title_label)

        # search field (left of the search icon)
        from PySide6.QtWidgets import QLineEdit

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        # reduce height by 1/6 (36 -> 30)
        self.search_field.setFixedHeight(30)
        # add a bit more blue tint to the background
        self.search_field.setStyleSheet(
            "QLineEdit{background: rgba(59,130,246,0.12); color: white; border: 1px solid rgba(59,130,246,0.18); border-radius: 8px; padding: 4px 10px;} QLineEdit:focus{border:1px solid rgba(99,102,241,0.26);}"
        )
        self.search_field.setMaximumWidth(420)
        # place search field and icon together in a small sublayout
        search_wrap = QHBoxLayout()
        search_wrap.setSpacing(6)
        search_wrap.addWidget(self.search_field)
        search = QPushButton("🔍")
        search.setFixedSize(34, 28)
        search.setStyleSheet("background: transparent; color: white; border: none;")
        search_wrap.addWidget(search)
        layout.addLayout(search_wrap)
        layout.addStretch()

        # avatar placeholder
        avatar = QLabel("")
        avatar.setFixedSize(36, 36)
        avatar.setStyleSheet("background: white; border-radius: 18px;")
        layout.addWidget(avatar)

        # window control buttons
        btn_min = QPushButton("—")
        btn_min.setFixedSize(36, 28)
        btn_min.setStyleSheet("background: transparent; color: white; border: none;")
        btn_min.clicked.connect(self.on_minimize)
        layout.addWidget(btn_min)

        btn_max = QPushButton("▢")
        btn_max.setFixedSize(36, 28)
        btn_max.setStyleSheet("background: transparent; color: white; border: none;")
        btn_max.clicked.connect(self.on_max_restore)
        layout.addWidget(btn_max)

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(36, 28)
        btn_close.setStyleSheet("background: transparent; color: white; border: none; font-weight: bold;")
        btn_close.clicked.connect(self.on_close)
        layout.addWidget(btn_close)

        self.setLayout(layout)
        self._is_maximized = False

    def on_minimize(self):
        if self.parent:
            self.parent.showMinimized()

    def on_max_restore(self):
        if not self.parent:
            return
        if self._is_maximized:
            self.parent.showNormal()
            self._is_maximized = False
        else:
            self.parent.showMaximized()
            self._is_maximized = True

    def on_close(self):
        if self.parent:
            self.parent.close()

    # make titlebar draggable
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and hasattr(self, "_drag_pos"):
            delta = event.globalPosition().toPoint() - self._drag_pos
            if self.parent and not self._is_maximized:
                self.parent.move(self.parent.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def set_logo(self, logo):
        """Accept a path, QPixmap, or QWidget to replace the logo placeholder."""
        from PySide6.QtGui import QPixmap
        from PySide6.QtWidgets import QWidget

        # remove existing if widget
        if isinstance(logo, QWidget):
            # replace widget
            layout = self.layout()
            layout.replaceWidget(self._logo_widget, logo)
            self._logo_widget.deleteLater()
            self._logo_widget = logo
            return

        if isinstance(logo, QPixmap):
            self._logo_widget.setPixmap(logo.scaled(self._logo_widget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self._logo_widget.setText("")
            return

        # assume path
        try:
            pix = QPixmap(str(logo))
            if not pix.isNull():
                self._logo_widget.setPixmap(pix.scaled(self._logo_widget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self._logo_widget.setText("")
        except Exception:
            # fallback: set text
            self._logo_widget.setText(str(logo))


class MainWindow(QWidget):
    """Frameless main window with custom title bar and rounded corners.

    This replaces the native window decorations with a custom-drawn frame so the
    application can match the provided design.
    """

    def __init__(self, logo=None):
        """Create a frameless `MainWindow`.

        Args:
            logo: optional path/pixmap/widget to show at the far left of the titlebar.
        """
        super().__init__()
        # set frameless window hint via setWindowFlag
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        # translucent background for rounded corners
        self.setAttribute(Qt.WA_TranslucentBackground)

        # outer container to apply shadow and rounded background
        self._outer = QWidget(self)
        self._outer.setObjectName("outer")
        self._outer.setStyleSheet(
            "QWidget#outer{background: qlineargradient(x1:0 y1:0, x2:1 y2:0, stop:0 #0f172a, stop:1 #111827); border-radius:14px;}"
        )

        shadow = QGraphicsDropShadowEffect(self._outer)
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 160))
        self._outer.setGraphicsEffect(shadow)

        # layout inside outer
        outer_layout = QVBoxLayout(self._outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # title bar
        self.titlebar = TitleBar(self, title="BFS", logo=logo)
        outer_layout.addWidget(self.titlebar)

        # content area placeholder (removed per request — keep only the title bar)
        # leave a stretch so the titlebar sits at the top and the rest is empty
        outer_layout.addStretch()

        # root layout for this widget
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.addWidget(self._outer)

        self._old_geometry = self.geometry()

        # status bar area (hidden until used)
        from PySide6.QtWidgets import QStatusBar
        from PySide6.QtCore import QTimer

        self._status_bar = QStatusBar()
        self._status_bar.setStyleSheet("QStatusBar{background: transparent; color: #374151;}")
        self._status_bar.setVisible(False)
        root.addWidget(self._status_bar)
        self._status_timer = None

    def set_logo(self, logo):
        if hasattr(self, "titlebar"):
            self.titlebar.set_logo(logo)

    def clear_content(self):
        """Remove any existing content holder and its children."""
        if hasattr(self, "_content_holder") and self._content_holder is not None:
            try:
                # remove from layout
                self._outer.layout().removeWidget(self._content_holder)
            except Exception:
                pass
            self._content_holder.setParent(None)
            self._content_holder.deleteLater()
            self._content_holder = None

    def set_content(self, widget):
        """Create an off-white content holder and insert the provided widget into it.

        widget: QWidget to place inside the content area
        """
        # clear existing
        self.clear_content()

        # create holder
        self._content_holder = QWidget()
        self._content_holder.setObjectName("content_holder")
        self._content_holder.setStyleSheet(
            "QWidget#content_holder{background: #F8FAFC; border-top-left-radius:0px; border-top-right-radius:0px; border-bottom-left-radius:10px; border-bottom-right-radius:10px;}"
        )
        ch_layout = QVBoxLayout(self._content_holder)
        ch_layout.setContentsMargins(12, 12, 12, 12)
        ch_layout.setSpacing(8)
        ch_layout.addWidget(widget)

        # insert holder under the titlebar (after titlebar which is first in outer_layout)
        outer_layout = self._outer.layout()
        outer_layout.addWidget(self._content_holder)

    # QMainWindow-like convenience methods
    def set_title(self, title: str):
        """Set the window title shown in the titlebar and the native window title."""
        if hasattr(self, "titlebar"):
            # update label if TitleBar had a title label
            try:
                for child in self.titlebar.children():
                    if isinstance(child, QLabel) and child.text():
                        child.setText(title)
                        break
            except Exception:
                pass
        try:
            super().setWindowTitle(title)
        except Exception:
            # QWidget has no setWindowTitle in some contexts, ignore
            pass

    def set_status_message(self, message: str, timeout: int = 0):
        """Show a status message in the status bar. timeout in milliseconds.

        If timeout > 0 the message will clear after timeout milliseconds.
        """
        # show status bar
        self._status_bar.showMessage(message)
        self._status_bar.setVisible(True)
        from PySide6.QtCore import QTimer
        # clear any existing timer
        try:
            if self._status_timer is not None:
                self._status_timer.stop()
        except Exception:
            pass
        if timeout and timeout > 0:
            self._status_timer = QTimer(self)
            self._status_timer.setSingleShot(True)
            self._status_timer.timeout.connect(lambda: self._status_bar.clearMessage())
            self._status_timer.start(timeout)

    def add_toolbar(self, widget):
        """Add a widget to the titlebar area, aligned to the right of the titlebar."""
        if hasattr(self, "titlebar"):
            self.titlebar.layout().insertWidget(self.titlebar.layout().count() - 3, widget)

    def add_menu(self, menu):
        """Placeholder for menu integration (no-op)."""
        # menus are better handled by embedding a menu bar widget
        pass

    def set_central_widget(self, widget):
        """Alias for set_content for QMainWindow compatibility."""
        self.set_content(widget)

    # ensure minimum size so controls are usable
    def show(self):
        self.resize(980, 640)
        super().show()

