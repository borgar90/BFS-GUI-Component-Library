## SearchableSelect

`SearchableSelect` is a small combo-like widget that filters options as the user types.

API

- `SearchableSelect(options, placeholder="")` — construct with a list of strings or (value,label) tuples
- `selection_changed` signal — emits the selected value
- `set_options(list)` — replace options at runtime

Examples

See `examples/select_showcase.py` for an interactive demo (type "nor" to see Norway).

Behavior

- By default the widget shows all options when the input receives focus (so you can click to browse options without typing). This can be disabled by passing `show_all_on_focus=False` to the constructor.
