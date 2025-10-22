"""BFS Light Theme tokens for desktop UI and component library exports.

This file exposes a compact set of design tokens intended to be portable
into a component library. Tokens are intentionally primitive (colors,
numbers, strings) so they can be mapped to platform-specific formats (CSS,
Qt stylesheets, design-system JSON, etc.).
"""

THEME = {
    # Core colors
    "colors": {
        "gradient": "linear-gradient(135deg, #071830, #163053, #3b2b6b, #6b44d9, #9a4de0)",
    "gradient_stops": ["#071830", "#163053", "#3b2b6b", "#6b44d9", "#9a4de0"],
    # focus / input-specific gradient (used for focus rings)
    "input_focus_gradient": "qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #00C6FF, stop:0.5 #9047FF, stop:1 #FF6F61)",
    "input_focus_stops": ["#00C6FF", "#9047FF", "#FF6F61"],
        "primary": "#3b2b6b",
        "primary_variant": "#6b44d9",
        "accent": "#9a4de0",
        "accent_deep": "#6b44d9",
        "bg": "#FAFAFA",
        "surface": "#FFFFFF",
        "border": "#E0E0E0",
        "text": "#111827",
        "muted": "#6B7280",
        "white": "#FFFFFF",
        "black": "#000000",
    },

    # Corner radius tokens (in px)
    "radius": {
        "small": 6,
        "default": 12,
        "large": 18,
        "round": 9999,
    },

    # Elevation / shadow tokens (strings suitable for CSS/Qt mapping)
    "shadow": {
        "soft": "0 2px 6px rgba(0,0,0,0.06)",
        "medium": "0 8px 24px rgba(0,0,0,0.12)",
        "heavy": "0 20px 60px rgba(0,0,0,0.18)",
    },

    # Spacing scale (px)
    "spacing": {
        "xs": 4,
        "sm": 8,
        "md": 16,
        "lg": 24,
        "xl": 32,
    },

    # Typography sizes (px)
    "type": {
        "h1": 28,
        "h2": 22,
        "h3": 18,
        "body": 14,
        "small": 12,
    },

    # Component sizing
    "components": {
        "logo_size": 96,          # default logo pixel size used in TitleBar
        "titlebar": {
            "height": 106,        # nominal height; UI code may compute from logo + padding
            "padding_top": 5,
            "padding_bottom": 5,
            "padding_lr": 12,
        },
        "control_button": {
            "size": 32,
            "radius": 16,
        },
        "avatar": {
            "sm": 32,
            "md": 48,
            "lg": 64,
        },
        "card": {
            "padding": 20,
            "radius": 10,
        },
    },

    # Small utilities
    "utils": {
        "focus_ring": "0 0 0 3px rgba(58,77,233,0.12)",
        # default painted focus ring width (px)
        "focus_ring_width": 6,
        "divider": "rgba(15,23,42,0.06)",
    },

    # Raw tokens kept for backwards compatibility with the older code
    "_legacy": {
        "bg": "#FAFAFA",
        "surface": "#FFFFFF",
        "text": "#111827",
        "muted": "#6B7280",
    }
}

# Export short-hands to help simple imports (desktop code expects flat keys)
THEME.update({
    "gradient_stops": THEME["colors"]["gradient_stops"],
    "gradient": THEME["colors"]["gradient"],
    "bg": THEME["colors"]["bg"],
    "surface": THEME["colors"]["surface"],
    "text": THEME["colors"]["text"],
    "radius_default": THEME["radius"]["default"],
})
