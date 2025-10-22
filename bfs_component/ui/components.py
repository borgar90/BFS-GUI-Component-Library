from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QRadioButton,
    QFrame,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap, QFont, QColor
from PySide6.QtCore import Qt
from PySide6.QtCore import QRegularExpression
from PySide6.QtWidgets import QComboBox, QCompleter, QLineEdit
from PySide6.QtCore import Qt as _Qt


class StyledLineEdit(QLineEdit):
    """A small QLineEdit subclass for consistent styling and validation.

    Provides a helper to set a regular-expression validator and a simple
    is_valid() method. This avoids duplicating input behavior and keeps
    styling centralized.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._regex = None
        self._regex_validator = None
        self._regex_error = None
        # Default dark/neon input styling inspired by the design board.
        # - dark background
        # - rounded corners
        # - subtle translucent border normally
        # - stronger neon-tinted border on focus
        # - lighter placeholder color
        self.setStyleSheet(r"""
        QLineEdit {
            background: #0b1220;
            color: #E6EEF8;
            border-radius: 10px;
            padding: 8px 12px;
            border: 1px solid rgba(255,255,255,0.06);
            selection-background-color: #7C3AED;
            selection-color: white;
            font-size: 12pt;
        }
        QLineEdit:focus {
            /* subtle neon focus using a strong purple tint */
            border: 1px solid rgba(124,58,237,0.95);
            background: qlineargradient(x1:0 y1:0 x2:1 y2:0, stop:0 #08122a, stop:1 #0c1526);
        }
        QLineEdit[error="true"] {
            border: 1px solid #DC2626;
        }
        QLineEdit::placeholder {
            color: rgba(230,238,248,0.45);
        }
        """)
        # prepare an indicator property; stylesheet can use :focus, but we'll
        # also toggle a 'focused' dynamic property so effects can be forced
        # and refreshed if needed.
        self.setProperty('focused', False)

    def focusInEvent(self, event):
        # apply a neon drop shadow to simulate the glow in the design
        try:
            from PySide6.QtWidgets import QGraphicsDropShadowEffect
            from PySide6.QtGui import QColor
            effect = QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(18)
            # use a more neutral cooler shadow so it doesn't overpower the warm gradient
            effect.setColor(QColor(8, 18, 42, 160))
            effect.setOffset(0, 0)
            self.setGraphicsEffect(effect)
        except Exception:
            # if effects unavailable, still set the property so stylesheet reacts
            pass
        self.setProperty('focused', True)
        # ensure style is refreshed
        self.style().unpolish(self)
        self.style().polish(self)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        # remove effect and clear property
        try:
            self.setGraphicsEffect(None)
        except Exception:
            pass
        self.setProperty('focused', False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().focusOutEvent(event)

    def paintEvent(self, event):
        # let the base class draw the line edit (text, background, caret)
        super().paintEvent(event)
        # only draw the gradient stroke when focused
        if not self.hasFocus():
            return

        try:
            from PySide6.QtGui import QPainter, QPen, QLinearGradient, QColor
            from PySide6.QtCore import QRectF

            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # inset the stroke slightly so it doesn't overlap text area
            r = QRectF(self.rect())
            inset = 2.0
            r.adjust(inset, inset, -inset, -inset)

            # Map colors so the top-left shows the warm stop (red -> orange -> pink),
            # the top area transitions to purple, and bottom-right becomes dark blue.
            # We'll create a diagonal gradient from top-left -> bottom-right and
            # place warm stops early with strong alpha.
            grad = QLinearGradient(r.topLeft(), r.bottomRight())
            # warm region at the start (top-left)
            grad.setColorAt(0.0, QColor(249, 59, 22, 255))   # vivid red/orange
            grad.setColorAt(0.12, QColor(249, 115, 22, 240))  # orange
            grad.setColorAt(0.28, QColor(236, 72, 153, 230))  # pink
            # transition to purple across the top/mid
            grad.setColorAt(0.55, QColor(124, 58, 237, 200))
            # darker blue toward bottom-right
            grad.setColorAt(1.0, QColor(8, 18, 42, 200))

            pen = QPen()
            pen.setBrush(grad)
            # stronger inner stroke width so colors are visible
            pen.setWidthF(4.0)
            pen.setJoinStyle(pen.RoundJoin)

            painter.setPen(pen)
            painter.drawRoundedRect(r, 10.0, 10.0)
            # faint outer translucent stroke to add contrast for warm colors
            outer_pen = QPen(QColor(255, 255, 255, 30))
            outer_pen.setWidthF(1.0)
            painter.setPen(outer_pen)
            painter.drawRoundedRect(r.adjusted(-0.5, -0.5, 0.5, 0.5), 10.0, 10.0)
            painter.end()
        except Exception:
            # be forgiving - if painting fails, don't crash
            return

    def set_validation_regex(self, pattern: str, error_message: str = "Invalid"):
        from PySide6.QtCore import QRegularExpression
        from PySide6.QtGui import QRegularExpressionValidator

        self._regex = QRegularExpression(pattern)
        self._regex_validator = QRegularExpressionValidator(self._regex)
        self._regex_error = error_message

    def is_valid(self):
        if getattr(self, '_regex_validator', None) is None:
            return True
        state, _, _ = self._regex_validator.validate(self.text(), 0)
        from PySide6.QtGui import QValidator

        return state == QValidator.Acceptable


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
        """TextInput is a thin composed widget that uses a styled QLineEdit.

        Internally we reuse a QLineEdit subclass (`StyledLineEdit`) so the
        underlying behaviour comes from Qt's native input widget and is easier
        to style and integrate with toolkits.
        """
        super().__init__(parent)
        from PySide6.QtWidgets import QVBoxLayout, QLabel

        self._label_text = label
        self._required = False
        self._regex_error = "Invalid input"

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._label = QLabel(label)
        self._label.setStyleSheet("font-weight: 600;")
        layout.addWidget(self._label)

        # use StyledLineEdit (subclass of QLineEdit) so we don't reinvent
        # validation and styling behavior
        self._input = StyledLineEdit()
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
        # delegate to the styled line edit which keeps the validator
        self._input.set_validation_regex(pattern, error_message)
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
        return self._input.is_valid()

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

        # input with a trailing dropdown button to mimic a combobox
        from PySide6.QtWidgets import QHBoxLayout, QToolButton

        h = QHBoxLayout()
        h.setContentsMargins(0, 0, 0, 0)
        self._input = QLineEdit()
        self._input.setPlaceholderText(placeholder)
        h.addWidget(self._input)

        self._button = QToolButton()
        self._button.setText("\u25BE")  # down arrow
        self._button.setCursor(self._input.cursor())
        self._button.setFocusPolicy(Qt.NoFocus)
        h.addWidget(self._button)

        layout.addLayout(h)

        # use a popup list so options only appear while focus is on the select
        self._popup = QListWidget(None)
        self._popup.setWindowFlags(Qt.Popup)
        self._popup.setFocusPolicy(Qt.StrongFocus)
        self._popup.setUniformItemSizes(True)
        self._popup.setMaximumHeight(200)

        self.setLayout(layout)

        self._populate_list(self._raw_options)
        # signals and behavior
        self._show_all_on_focus = show_all_on_focus
        self._input.textChanged.connect(self._on_text_changed)
        # wrap keypress
        self._input.keyPressEvent = self._input_keypress_wrapper(self._input.keyPressEvent)
        self._popup.itemClicked.connect(self._on_item_clicked)
        self._button.clicked.connect(self.toggle_popup)

        # Hide popup when focus leaves both input and popup
        self._popup.installEventFilter(self)

        if self._show_all_on_focus:
            orig_focus_in = getattr(self._input, 'focusInEvent', None)

            def _focus_in(event):
                # show all options when focused
                self._populate_list(self._raw_options)
                self._show_popup()
                if orig_focus_in:
                    return orig_focus_in(event)

            self._input.focusInEvent = _focus_in

        # ensure input losing focus hides popup unless popup itself gets focus
        orig_focus_out = getattr(self._input, 'focusOutEvent', None)

        def _focus_out(event):
            # schedule check after focus changes
            from PySide6.QtCore import QTimer

            QTimer.singleShot(0, self._hide_if_focus_lost)
            if orig_focus_out:
                return orig_focus_out(event)

        self._input.focusOutEvent = _focus_out

    def _populate_list(self, options):
        from PySide6.QtWidgets import QListWidgetItem
        self._popup.clear()
        for val, label in options:
            item = QListWidgetItem(label)
            item.setData(256, val)
            self._popup.addItem(item)

    def _on_text_changed(self, txt: str):
        txt_low = txt.strip().lower()
        if not txt_low:
            # show all options
            filtered = self._raw_options
        else:
            filtered = [o for o in self._raw_options if txt_low in o[1].lower()]
        self._populate_list(filtered)
        if len(filtered) > 0:
            self._show_popup()
        else:
            self._popup.hide()

    def _input_keypress_wrapper(self, orig):
        from PySide6.QtCore import Qt

        def _wrapper(event):
            key = event.key()
            if key in (Qt.Key_Down, Qt.Key_Up):
                # navigate the popup list
                if not self._popup.isVisible():
                    self._show_popup()
                cur = self._popup.currentRow()
                if key == Qt.Key_Down:
                    cur = min(self._popup.count() - 1, cur + 1) if cur >= 0 else 0
                else:
                    cur = max(0, cur - 1) if cur >= 0 else max(0, self._popup.count() - 1)
                self._popup.setCurrentRow(cur)
                return
            if key == Qt.Key_Return or key == Qt.Key_Enter:
                item = self._popup.currentItem()
                if item:
                    self._select_item(item)
                return
            # default
            return orig(event)

        return _wrapper

    def _on_item_clicked(self, item):
        self._select_item(item)

    def toggle_popup(self):
        if self._popup.isVisible():
            self._popup.hide()
        else:
            # repopulate and show
            self._populate_list(self._raw_options)
            self._show_popup()

    # Combobox-like convenience API
    def set_current_value(self, value):
        # find item with matching value and select it
        for i in range(self._popup.count()):
            it = self._popup.item(i)
            if it.data(256) == value:
                self._select_item(it)
                return True
        return False

    def get_current_value(self):
        return self.current_value()

    def _select_item(self, item):
        val = item.data(256)
        label = item.text()
        self._input.setText(label)
        self._popup.hide()
        self.selection_changed.emit(val)

    def current_value(self):
        # return value of current selection if any
        cur = self._popup.currentItem()
        return cur.data(256) if cur is not None else None


class StyledComboBox(QWidget):
    """A combobox-like component built from QComboBox (editable) + StyledLineEdit.

    - Uses Qt's QCompleter for inline filtering and navigation
    - Provides `set_items(items)` where items is list[str] or list[(val,label)]
    - Emits `selection_changed(value)` when an item is selected
    """
    from PySide6.QtCore import Signal

    selection_changed = Signal(object)

    def __init__(self, items: list[str] | list[tuple] = None, parent=None):
        super().__init__(parent)
        from PySide6.QtWidgets import QHBoxLayout

        self._combobox = QComboBox()
        self._combobox.setEditable(True)
        # replace line edit with StyledLineEdit for consistent styling
        self._input = StyledLineEdit()
        self._combobox.setLineEdit(self._input)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._combobox)
        self.setLayout(layout)

        self._completer = QCompleter()
        self._completer.setCaseSensitivity(_Qt.CaseInsensitive)
        self._combobox.setCompleter(self._completer)

        self._items = []
        if items:
            self.set_items(items)

        self._combobox.activated.connect(self._on_activated)

    def set_items(self, items: list):
        # store as list of (value,label)
        normalized = []
        self._combobox.clear()
        for it in items:
            if isinstance(it, tuple) and len(it) >= 2:
                normalized.append((it[0], str(it[1])))
                self._combobox.addItem(str(it[1]), it[0])
            else:
                normalized.append((it, str(it)))
                self._combobox.addItem(str(it), it)
        self._items = normalized
        # update completer model
        labels = [lbl for _, lbl in self._items]
        from PySide6.QtCore import QStringListModel
        model = QStringListModel(labels)
        self._completer.setModel(model)

    def _on_activated(self, index_or_text):
        # QComboBox.activated can send either index or text depending on usage
        if isinstance(index_or_text, int):
            val = self._combobox.itemData(index_or_text)
            self.selection_changed.emit(val)
        else:
            # find matching label
            txt = str(index_or_text)
            for val, lbl in self._items:
                if lbl == txt:
                    self.selection_changed.emit(val)
                    return

    def current_value(self):
        idx = self._combobox.currentIndex()
        if idx >= 0:
            return self._combobox.itemData(idx)
        # fall back to text
        return self._combobox.currentText()

    def set_current_value(self, value):
        # try to find exact match in item data
        for i in range(self._combobox.count()):
            if self._combobox.itemData(i) == value:
                self._combobox.setCurrentIndex(i)
                return True
        # fallback: set text
        self._combobox.setCurrentText(str(value))
        return False


class StyledRadioButton(QRadioButton):
    """A thin subclass of QRadioButton to centralize styling for the library.

    We keep it minimal: primarily a hook to apply a shared stylesheet later.
    """
    def __init__(self, label: str = "", parent=None):
        super().__init__(label, parent)


class RadioGroup(QWidget):
    """A simple radio-button group component.

    - Use `set_options(items)` where items is list[str] or list[(value,label)]
    - Emits `selection_changed(value)` when selection changes
    - Methods: set_value(value), get_value()
    """
    from PySide6.QtCore import Signal

    selection_changed = Signal(object)

    def __init__(self, items: list = None, orientation: Qt = Qt.Vertical, parent=None):
        super().__init__(parent)
        from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QButtonGroup

        self._layout = QVBoxLayout() if orientation == Qt.Vertical else QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)
        self._id_to_value = {}
        self._value_to_id = {}

        if items:
            self.set_options(items)

        self._button_group.idToggled.connect(self._on_id_toggled)

    def set_options(self, items: list):
        # clear existing buttons
        for i in reversed(range(self._layout.count())):
            w = self._layout.itemAt(i).widget()
            if w:
                self._layout.removeWidget(w)
                w.setParent(None)

        self._id_to_value.clear()
        self._value_to_id.clear()
        self._button_group = type(self._button_group)(self)
        self._button_group.setExclusive(True)

        for idx, it in enumerate(items):
            if isinstance(it, tuple) and len(it) >= 2:
                val, lbl = it[0], str(it[1])
            else:
                val, lbl = it, str(it)
            btn = StyledRadioButton(lbl)
            self._layout.addWidget(btn)
            self._button_group.addButton(btn, idx)
            self._id_to_value[idx] = val
            self._value_to_id[val] = idx

    def _on_id_toggled(self, id_, checked):
        if checked:
            val = self._id_to_value.get(id_)
            self.selection_changed.emit(val)

    def set_value(self, value):
        idx = self._value_to_id.get(value)
        if idx is not None:
            btn = self._button_group.button(idx)
            if btn:
                btn.setChecked(True)
                return True
        return False

    def get_value(self):
        btn = self._button_group.checkedButton()
        if btn is None:
            return None
        id_ = self._button_group.id(btn)
        return self._id_to_value.get(id_)



