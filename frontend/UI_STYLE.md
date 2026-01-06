# FoodID UI Style & Palette

## Colors & Gradients
- **Primary Gradient**: #FF6B6B → #FF8E53 (hero text, primary buttons, logo text gradient)
- **Secondary Gradient**: #4FACFE → #00F2FE (supporting highlight option)
- **Background**: #0F0F12 with soft radial glows (primary glow rgba(255,107,107,0.15) at 15%/15%, secondary glow rgba(79,172,254,0.1) at 85%/85%)
- **Surface**: rgba(255,255,255,0.05) (cards), hover: rgba(255,255,255,0.08)
- **Borders**: rgba(255,255,255,0.10)
- **Text Primary**: #FFFFFF
- **Text Secondary**: rgba(255,255,255,0.60)
- **Accent**: #FF6B6B (icons, hover state, spinner top border)
- **Chip/Badge BG**: rgba(255,255,255,0.10) with border rgba(255,255,255,0.05)
- **Result Highlight**: rgba(255,107,107,0.08) with border rgba(255,107,107,0.30)
- **Confidence Bar**: gradient 90deg rgba(255,107,107,0.10) → rgba(255,107,107,0.05)

## Typography
- **Font**: "Outfit", sans-serif
- **Hero Heading**: 4rem, 700 weight, vertical gradient #FFFFFF → rgba(255,255,255,0.7)
- **Body**: 1rem, line-height ~1.6
- **Subtitle**: 1.25rem, color rgba(255,255,255,0.6)

## Layout & Components
- **Nav**: Logo gradient text; badges with pill shape and glass blur (backdrop-filter blur(12px))
- **Cards**: Rounded 1.5rem, glass effect, shadow 0 20px 40px rgba(0,0,0,0.2)
- **Upload Area**: Dashed border rgba(255,255,255,0.10), hover/drag border #FF6B6B and light red tint
- **Preview**: Rounded 1rem, shadow 0 8px 32px rgba(0,0,0,0.2); overlay gradient to transparent
- **Buttons**:
  - Primary: Primary gradient fill, white text, shadow 0 4px 15px rgba(255,107,107,0.3); hover lift
  - Secondary: Semi-transparent white bg, blur backdrop
- **States**:
  - Empty: Centered, secondary text, emoji accent
  - Loading: Spinner (#FF6B6B on top border)
  - Results: Top match tinted with accent background; confidence bar animates width

## Spacing & Grid
- **Container**: Max width 1280px, 2rem padding
- **Content Grid**: 1.2fr / 0.8fr columns, 2rem gap; stacks to 1 column below 900px
- **Stats Footer**: 3-column grid; borders between items; stacks vertically on mobile

## Effects
- **Glass Blur**: blur(12px) on cards/badges for subtle translucency
- **Animations**: fadeIn and slideUp for hero/content; spinner rotate; confidence bar width transition 1s ease-out

## Usage Notes
- Keep text on dark surfaces; reserve gradients for key CTAs and brand elements.
- Maintain accent #FF6B6B for interactive focus (hover, active states) to stay consistent with results and spinner.
- Preserve card transparency and shadows to keep the neon-on-dark feel without pure black fills.
