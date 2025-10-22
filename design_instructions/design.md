# 🎨 BFS Light Theme Design System

This document defines the **official BFS Light Theme**, derived from our CRM and design system exploration.  
It establishes a unified visual identity across all BFS applications (SaaS, CRM, internal tools, dashboards, and desktop apps).

---

## 🌈 1. Color Palette

| Role | Color Name | Hex | Description |
|------|-------------|-----|-------------|
| **Primary Gradient Start** | Electric Cyan | `#00E5FF` | Core neon accent for gradients and buttons |
| **Primary Gradient Mid** | Ultraviolet | `#7C4DFF` | Used in transitions and gradient blending |
| **Primary Gradient End** | Magenta Blaze | `#E040FB` | Warm tone for gradient finish |
| **Accent** | Solar Amber | `#FF8A00` | Used sparingly for highlights or alerts |
| **Background Base** | Cloud White | `#FAFAFA` | Default app background |
| **Surface Panel** | Snow Mist | `#FFFFFF` | Cards, forms, modals |
| **Borders** | Graphite Line | `#E0E0E0` | Soft dividers and component outlines |
| **Text Primary** | Deep Charcoal | `#111827` | Main text and headings |
| **Text Secondary** | Gray Nebula | `#6B7280` | Subdued text and labels |
| **Text Placeholder** | Cloud Gray | `#9CA3AF` | Input placeholders |
| **Success** | Emerald Pulse | `#10B981` | Positive actions |
| **Error** | Plasma Red | `#EF4444` | Alerts and destructive actions |

### 🔮 Gradient Preset
```css
background: linear-gradient(135deg, #00E5FF, #7C4DFF, #E040FB, #FF8A00);


🧩 2. Surfaces & Elevation
Layer	Color	Shadow / Border	Description
App Background	#FAFAFA	none	Clean neutral base
Card / Panel	#FFFFFF	subtle 0 2px 6px rgba(0,0,0,0.05)	Floating component base
Modal / Drawer	#FFFFFF	0 6px 20px rgba(0,0,0,0.1)	Top-layer interactions
Input Field	#FFFFFF	1px solid #E0E0E0	Clear and soft with subtle shadow
🔘 3. Buttons
Primary Button

Background: BFS gradient

Text: #FFFFFF

Hover: Reverse gradient direction

Shadow: 0 4px 10px rgba(0,0,0,0.1)

Border Radius: 12px

Secondary Button

Background: #FFFFFF

Border: 1px solid #E0E0E0

Text: #111827

Hover: Gradient border glow

Destructive Button

Background: #EF4444

Text: #FFFFFF

Hover: Slightly darker red tone

🔤 4. Typography
Type	Font	Size	Weight	Usage
Logo / Brand	Orbitron / Exo 2	28–36px	700	BFS branding
Headings (H1–H3)	Poppins / Inter	18–24px	600	Section titles
Body Text	Inter / Nunito Sans	14–16px	400	Regular text
Labels	Inter	12px	500	UI labels
Code / Technical	JetBrains Mono	13px	500	Dev panels
🧠 5. Components
Cards

Background: #FFFFFF

Border: 1px solid #E0E0E0

Shadow: 0 2px 6px rgba(0,0,0,0.05)

Border-radius: 12px

Hover: Slight lift (translateY(-2px)) with glow edge in gradient

Inputs

Background: #FFFFFF

Border: 1px solid #E0E0E0

Focus: Gradient underline / border glow

Padding: 12px 16px

Placeholder: #9CA3AF

Avatars

Circular shape

Gradient initials background (randomized from palette)

Drop shadow for depth

Tags / Badges

Soft rounded corners

Color-coded (Active, Pending, Inactive)

Light pastel background with gradient text possible

🧭 6. Layout & Navigation
Top Bar

Background: #FFFFFF

Shadow: subtle bottom line (0 1px 0 rgba(0,0,0,0.05))

Elements:

BFS Logo on left (color)

Section Title (“Dashboard”, “CRM”)

Right: Search bar + Avatar

Sidebar (Optional)

Background: #F8FAFC

Active Icon: gradient accent line on left

Hover: subtle gradient glow

💫 7. Animation & Interactivity
Element	Effect	Duration
Button hover	Gradient pulse or reverse	200ms
Card hover	Elevate and glow	150ms
Input focus	Gradient border fade in	150ms
Modal open	Slide & fade	250ms
Add contact	Smooth fade + item insertion	200ms
🪞 8. Component Examples (Use Cases)
Example 1: Dashboard

Top bar with BFS logo

White panels for metrics

“Add Customer” gradient button

Example 2: Add New Customer Form

Clean white card

Form inputs with shadows

Gradient “Add” button

“Cancel” as neutral secondary

Example 3: Company View (Multi-Contact)

Header: Company logo + name + status badges

Contact cards: rounded, white, gradient avatars

“+ Add Contact” gradient button on top right

🧱 9. Theming Tokens (CSS Variables)
:root {
  --color-bg: #FAFAFA;
  --color-surface: #FFFFFF;
  --color-border: #E0E0E0;
  --color-text: #111827;
  --color-text-secondary: #6B7280;

  --gradient-bfs: linear-gradient(135deg, #00E5FF, #7C4DFF, #E040FB, #FF8A00);
  --radius-base: 12px;
  --shadow-soft: 0 2px 6px rgba(0,0,0,0.05);
  --shadow-strong: 0 6px 20px rgba(0,0,0,0.1);
  --transition-base: all 0.2s ease;
}

🌤️ 10. Design Philosophy

Bright, professional, and human.

The BFS Light Theme represents clarity and approachability.
It merges neon gradients (BFS signature) with clean white UI to evoke trust, innovation, and precision — perfect for business SaaS and CRM tools.

Maintainer: Borgar Flaen Stensrud
Theme Version: 1.0.0
Applies To:

BFS CRM Desktop App

BFS Web Console

BFS SaaS Platform

BFS Admin Panels

BFS API Dashboard

BFS Dashboards