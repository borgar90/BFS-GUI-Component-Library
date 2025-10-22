## Input components

Text and form inputs live here. The first component is `TextInput`, a small
labelled text entry with validation helpers.

Usage

```python
from bfs_component.ui.components import TextInput

t = TextInput("Name", placeholder="Full name")
t.set_required(True)
t.set_validation_regex(r"^[A-Za-z ]+$", "Only letters and spaces allowed")
```

See `examples/inputs_showcase.py` for a small interactive demo.
