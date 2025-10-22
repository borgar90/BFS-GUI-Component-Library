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


class TextInput(QWidget):
    """A labelled text input with validation and inline error display.

    Features:
    - label text above the input
    - placeholder text
    - required flag (shows error when empty)
    - regex validator (QRegularExpression) with an error message
    - `text_changed` signal emitted when the text changes

    Simple usage:
        t = TextInput(label="Name", placeholder="Full name")
        t.set_required(True)
        t.set_validation_regex(r"^[A-Za-z ]+$", "Only letters and spaces allowed")
    """
    from PySide6.QtCore import Signal

    text_changed = Signal(str)

    def __init__(self, label: str = "", placeholder: str = "", parent=None):
        super().__init__(parent)
        from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit
        from PySide6.QtGui import QRegularExpressionValidator
        from PySide6.QtCore import QRegularExpression

        self._label_text = label
        self._required = False
        self._regex = None
        self._regex_error = "Invalid input"

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._label = QLabel(label)
        self._label.setStyleSheet("font-weight: 600;")
        layout.addWidget(self._label)

        self._input = QLineEdit()
        self._input.setPlaceholderText(placeholder)
        self._input.textChanged.connect(self._on_text_changed)
        layout.addWidget(self._input)

        self._error = QLabel("")
        self._error.setStyleSheet("color: #DC2626; font-size: 11px;")
        self._error.setVisible(False)
        layout.addWidget(self._error)

        self.setLayout(layout)

    def _on_text_changed(self, txt: str):
        self.clear_error()
        self.text_changed.emit(txt)

    def set_placeholder(self, text: str):
        self._input.setPlaceholderText(text)

    def set_required(self, required: bool = True, error_message: str = "This field is required"):
        self._required = required
        self._required_error = error_message

    def set_validation_regex(self, pattern: str, error_message: str = "Invalid input"):
        """Set a regular expression validator. Pattern is a Python/Qt regex.

        The widget will validate via `is_valid()` and you can display the
        error message by calling `validate(show_error=True)` or checking
        `is_valid()` programmatically.
        """
        from PySide6.QtCore import QRegularExpression
        from PySide6.QtGui import QRegularExpressionValidator

        self._regex = QRegularExpression(pattern)
        self._regex_validator = QRegularExpressionValidator(self._regex)
        self._regex_error = error_message

    def text(self) -> str:
        return self._input.text()

    def set_text(self, value: str):
        self._input.setText(value)

    def clear(self):
        self._input.clear()
        self.clear_error()

    def is_valid(self) -> bool:
        """Return True if current text satisfies required/regex rules."""
        txt = self.text()
        if self._required and not txt:
            return False
        if getattr(self, "_regex", None) is not None:
            # use validator
            state, _, _ = getattr(self, "_regex_validator").validate(txt, 0)
            from PySide6.QtGui import QValidator

            return state == QValidator.Acceptable
        return True

    def validate(self, show_error: bool = True) -> bool:
        ok = self.is_valid()
        if not ok and show_error:
            if self._required and not self.text():
                self._show_error(getattr(self, "_required_error", "This field is required"))
            elif getattr(self, "_regex", None) is not None:
                self._show_error(getattr(self, "_regex_error", "Invalid input"))
            else:
                self._show_error("Invalid input")
        return ok

    def _show_error(self, msg: str):
        self._error.setText(msg)
        self._error.setVisible(True)

    def clear_error(self):
        self._error.setText("")
        self._error.setVisible(False)


class SearchableSelect(QWidget):
    """A combo-like widget with a text input and a filtered drop-down list.

    - Provide a list of options (sequence of strings or (value, label) tuples)
    - Typing filters visible options (case-insensitive, substring match)
    - Arrow keys navigate, Enter selects, clicking selects
    - Emits `selection_changed` with the selected value (label if string list)
    """
    from PySide6.QtCore import Signal

    selection_changed = Signal(object)

    def __init__(self, options: list, placeholder: str = "", parent=None, show_all_on_focus: bool = True):
        super().__init__(parent)
        from PySide6.QtWidgets import QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
        from PySide6.QtCore import Qt

        self._raw_options = []
        # Normalize options to list of (value, label)
        for o in options:
            if isinstance(o, tuple) and len(o) >= 2:
                self._raw_options.append((o[0], str(o[1])))
            else:
                self._raw_options.append((o, str(o)))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self._input = QLineEdit()
        self._input.setPlaceholderText(placeholder)
        layout.addWidget(self._input)

        self._list = QListWidget()
        self._list.setVisible(False)
        self._list.setMaximumHeight(200)
        layout.addWidget(self._list)

        self.setLayout(layout)

        self._populate_list(self._raw_options)
        # signals and behavior
        self._show_all_on_focus = show_all_on_focus
        self._input.textChanged.connect(self._on_text_changed)
        # wrap keypress
        self._input.keyPressEvent = self._input_keypress_wrapper(self._input.keyPressEvent)
        self._list.itemClicked.connect(self._on_item_clicked)

        if self._show_all_on_focus:
            orig_focus_in = getattr(self._input, 'focusInEvent', None)

            def _focus_in(event):
                # show all options when focused
                self._populate_list(self._raw_options)
                self._list.setVisible(self._list.count() > 0)
                if orig_focus_in:
                    return orig_focus_in(event)

            self._input.focusInEvent = _focus_in

    def _populate_list(self, options):
        from PySide6.QtWidgets import QListWidgetItem
        self._list.clear()
        for val, label in options:
            item = QListWidgetItem(label)
            item.setData(256, val)
            self._list.addItem(item)

    def _on_text_changed(self, txt: str):
        txt_low = txt.strip().lower()
        if not txt_low:
            # show all options
            filtered = self._raw_options
        else:
            filtered = [o for o in self._raw_options if txt_low in o[1].lower()]

        self._populate_list(filtered)
        self._list.setVisible(len(filtered) > 0)

    def _input_keypress_wrapper(self, orig):
        from PySide6.QtCore import Qt

        def _wrapper(event):
            key = event.key()
            if key in (Qt.Key_Down, Qt.Key_Up):
                # navigate the list
                if not self._list.isVisible():
                    self._list.setVisible(True)
                cur = self._list.currentRow()
                if key == Qt.Key_Down:
                    cur = min(self._list.count() - 1, cur + 1) if cur >= 0 else 0
                else:
                    cur = max(0, cur - 1) if cur >= 0 else max(0, self._list.count() - 1)
                self._list.setCurrentRow(cur)
                return
            if key == Qt.Key_Return or key == Qt.Key_Enter:
                item = self._list.currentItem()
                if item:
                    self._select_item(item)
                return
            # default
            return orig(event)

        return _wrapper

    def _on_item_clicked(self, item):
        self._select_item(item)

    def _select_item(self, item):
        val = item.data(256)
        label = item.text()
        self._input.setText(label)
        self._list.setVisible(False)
        self.selection_changed.emit(val)

    def current_value(self):
        # return value of current selection if any
        cur = self._list.currentItem()
        return cur.data(256) if cur is not None else None

    def set_options(self, options: list):
        self._raw_options = []
        for o in options:
            if isinstance(o, tuple) and len(o) >= 2:
                self._raw_options.append((o[0], str(o[1])))
            else:
                self._raw_options.append((o, str(o)))
        self._populate_list(self._raw_options)


