from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap, QFont, QColor
from PySide6.QtCore import Qt


class HeaderWidget(QWidget):
    """A small header widget used inside MainFrame.

    Shows a circular logo placeholder and a title label. This is a lightweight
    helper intended for composing the `MainFrame` content.
    """
    def __init__(self, title: str = "BFS"):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        logo = QLabel()
        logo.setFixedSize(36, 36)
        logo.setStyleSheet("background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #6EE7F2, stop:1 #7C3AED); border-radius: 8px;")
        layout.addWidget(logo)
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title_label)
        layout.addStretch()
        self.setLayout(layout)


class Card(QFrame):
    """A generic card widget with header/body/footer slots.

    Usage:
        card = Card()
        card.set_header(QLabel('Header'))
        card.set_body(QWidget())
        card.set_footer(QLabel('Footer'))
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("QFrame{background: white; border-radius: 8px;}")
        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(8, 8, 8, 8)
        self._main_layout.setSpacing(6)
        self.setLayout(self._main_layout)

    def set_header(self, widget: QWidget):
        if hasattr(self, "_header") and self._header is not None:
            self._main_layout.removeWidget(self._header)
            self._header.setParent(None)
        self._header = widget
        self._main_layout.insertWidget(0, widget)

    def set_body(self, widget: QWidget):
        # body inserted after header if present
        idx = 1 if hasattr(self, "_header") and self._header is not None else 0
        self._body = widget
        self._main_layout.insertWidget(idx, widget)

    def set_footer(self, widget: QWidget):
        # footer at the end
        if hasattr(self, "_footer") and self._footer is not None:
            self._main_layout.removeWidget(self._footer)
            self._footer.setParent(None)
        self._footer = widget
        self._main_layout.addWidget(widget)


class ContactCard(Card):
    """Contact card implemented on top of Card. Keeps same visual layout but
    uses Card slots for consistency.
    """
    def __init__(self, initials: str, name: str, role: str, email: str = "", phone: str = ""):
        super().__init__()
        layout = QHBoxLayout()
        avatar = QLabel(initials)
        avatar.setFixedSize(48, 48)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet("background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #60A5FA, stop:1 #A78BFA); color: white; border-radius: 12px; font-weight: bold;")
        layout.addWidget(avatar)

        v = QVBoxLayout()
        name_label = QLabel(name)
        name_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        v.addWidget(name_label)
        role_label = QLabel(role)
        role_label.setStyleSheet("color: #6b7280;")
        v.addWidget(role_label)

        if email:
            v.addWidget(QLabel(email))
        if phone:
            v.addWidget(QLabel(phone))

        layout.addLayout(v)
        self.set_body(QWidget())
        # put our layout inside a body container to preserve Card slots
        body_container = QWidget()
        body_container.setLayout(layout)
        self.set_body(body_container)


class CompanyCard(QFrame):
    """A company overview card with logo, name and tag badges.

    Parameters
    - name: company name
    - tags: optional list of tag strings to show as badges
    """
    def __init__(self, name: str, tags: list[str] = None):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("QFrame{background: white; border-radius: 12px;}")
        layout = QHBoxLayout()
        left = QVBoxLayout()
        logo = QLabel(name[:2].upper())
        logo.setFixedSize(64, 64)
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #34D399, stop:1 #60A5FA); color: white; border-radius: 16px; font-weight: bold; font-size: 18pt;")
        left.addWidget(logo)
        left.addStretch()
        layout.addLayout(left)

        mid = QVBoxLayout()
        title = QLabel(name)
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        mid.addWidget(title)
        if tags:
            tags_h = QHBoxLayout()
            for t in tags:
                tag = QLabel(t)
                tag.setStyleSheet("background: #F3F4F6; border-radius: 6px; padding: 4px; color: #111827;")
                tags_h.addWidget(tag)
            tags_h.addStretch()
            mid.addLayout(tags_h)
        layout.addLayout(mid)

        right = QVBoxLayout()
        add_btn = QPushButton("+ Add Contact")
        add_btn.setStyleSheet("background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #60A5FA, stop:1 #EC4899); color: white; padding: 8px; border-radius: 8px;")
        right.addWidget(add_btn)
        right.addStretch()
        layout.addLayout(right)

        self.setLayout(layout)


class MainFrame(QWidget):
    """The main content frame that composes header, company card and contacts.

    This widget is intended as a reusable content panel that can be injected
    into `MainWindow` via `set_content`.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        header = HeaderWidget("BFS")
        layout.addWidget(header)
        layout.addSpacing(12)

        comp = CompanyCard("Acme Corporation", tags=["Technology", "Active"])
        comp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(comp)
        layout.addSpacing(12)

        # contacts area
        contacts_h = QHBoxLayout()
        left_col = QVBoxLayout()
        left_col.addWidget(ContactCard("JD", "Jane Doe", "Project Manager", "jane@acme.com", "+47 934 88 112"))
        left_col.addSpacing(8)
        left_col.addWidget(ContactCard("JS", "John Smith", "Sales Representative", phone="+1 202 555 0168"))
        contacts_h.addLayout(left_col)

        right_col = QVBoxLayout()
        right_col.addWidget(ContactCard("JS", "John Smith", "Sales Representative", phone="+1 202 555 0168"))
        right_col.addSpacing(8)
        right_col.addWidget(ContactCard("C", "Carol Remecom", "Marketing Director"))
        right_col.addSpacing(8)
        right_col.addWidget(ContactCard("MB", "Michael Brown", "Sales Representative", phone="+1 202 555 0168"))
        contacts_h.addLayout(right_col)

        layout.addLayout(contacts_h)
        layout.addStretch()

        self.setLayout(layout)
