## Card component

The `Card` component is a small reusable container widget with three slots:

- header: typically a QLabel, icon, or title
- body: main content (text, layout, list)
- footer: small actions or meta information

API

- Card.set_header(widget)
- Card.set_body(widget)
- Card.set_footer(widget)

The repository includes `ContactCard` and `CompanyCard` which subclass `Card` and demonstrate how to build specialized cards.

Examples

See `examples/cards_showcase.py` for a small storybook-like window that demonstrates multiple card variants.
