# Rules: design and build (section 5)

## 5. Design and build (art direction, MUI + Tailwind)

Owned by page-designer. Design every page as if the `frontend-design` skill is active (load it with the Skill tool when it is listed; the rules below summarize it). The goal is a page that looks made for this one practice, never a template. Material Design stays the logic underneath (MUI components, color roles, contrast, states), but the look is editorial and specific to the brand.

### 5.1 Ground it in the practice

Before designing, name in one line each: the practice's world (specialty, place, patients), the audience, and the page's one job. Distinct choices come from the subject: an orthopedic surgeon in Layton (movement, bone, mountains, athletes) should look nothing like a med spa in Scottsdale (skin, light, ritual) or a behavioral health clinic (calm, safety, plain talk). Use the brand guide, logo, photos and real practice facts throughout. Design decisions (color, type, imagery, shape) come from the brand guidelines first, then the current website; a benchmark site never drives the look.

### 5.2 Write a design plan, then review it

Before any code, write a short plan:

- **Color:** 4 to 6 named hex values (for example "Summit navy #0B2545", "Trail blue #1463FF", "Snowfield #F2F6FB"), built from the brand color and its tonal palette (`scripts/m3_scheme.py`). Say where each one is used.
- **Type:** the typefaces (brand fonts first) and their roles, plus the one type scale for this project, picked from the ranges in 5.5.
- **Layout:** one sentence and a small ASCII wireframe for the hero and for the overall page rhythm. Say how content aligns, and which benchmark structure ideas you used, if any.
- **Principles:** 2 or 3 lines on what makes this page unique, and the **one** memorable element where the boldness is spent (for example: a full-bleed brand gradient field behind the hero, a hero photo that breaks the grid, a distinctive display face set with a strong headline shape).

Then review the plan against the brief. If any part reads like the default you would make for any similar practice, change it and say what you changed and why. Check it against the cliché list in 5.3. Show the plan to the user only when they asked to approve the plan first; otherwise keep it in your working notes and build.

### 5.3 Clichés to avoid (unless the brand guide asks for them)

- Purple or violet gradients, purple-to-pink, and any gradient that is not built from the brand's own colors.
- Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Space Grotesk, Playfair Display, or system defaults as the main type.
- The SaaS card kit: content chopped into identical rounded cards, one radius on everything, the same soft grey shadow under each.
- A warm cream background (near #F4F1EA) with a serif display and a terracotta or clay accent (near #D97757).
- A near-black background with one acid-green or vermilion accent.
- Broadsheet layouts with hairline rules and zero radius everywhere.
- Template chrome: tracked all-caps eyebrows above every heading, "A · B · C" meta strings, "→" on every link, tinted near-black (#0B0B0B, #111) standing in for black, monospace for small labels.
- Big number + small label + gradient accent as the default hero.
- Numbered markers (01, 02, 03) on content that is not a sequence. Steps and timelines may be numbered; reasons and benefits may not.
- Fade-and-slide-up on every section, hover effects on every card.

### 5.4 Color and gradients

- The brand color is the seed. Run `scripts/m3_scheme.py "#HEX"` to get Material color roles (for accessible text and surface pairs) and the full tonal palettes (tones 0 to 100) of the brand, secondary, tertiary and neutral hues.
- Use color with intent, not timidly: at least one full-bleed section in a strong brand tone, and one gradient moment built only from brand tones (for example primary tone 20 to primary tone 50, or primary to tertiary), with optional fine grain (an inline SVG noise at low opacity) so it feels printed, not digital. Keep gradients to one or two big moments (hero field, final CTA band), never as decoration on every element.
- Neutrals come from the brand's neutral palette (slightly tinted toward the brand hue), not pure greys. True black is #000 only if the brand uses it.
- Every text and background pair meets WCAG 2.2 AA. Use the role pairs from `scripts/m3_scheme.py` (`on-primary` on `primary`, and so on) or check contrast.

### 5.5 Typography

**Fonts.** Use the approved brand fonts and verify that they load (`scripts/qa.py` lists the loaded families). If a brand font is unavailable, say so and propose a substitute; never swap an approved font silently. Keep the family count to one or two. When the brand names no fonts, pick one distinct pairing (Google Fonts) that fits the practice, and do not reuse the same pairing on every project:

| Feel | Display | Body | Good for |
|---|---|---|---|
| Warm, human | Fraunces (use its optical size and soft axis) | Hanken Grotesk | Family practice, women's health, pediatrics |
| Refined, quiet luxury | Instrument Serif | Instrument Sans | Aesthetics, plastics, med spa, dermatology |
| Energetic, athletic | Bricolage Grotesque (play with width) | Source Serif 4 | Orthopedics, sports medicine, PT, chiropractic |
| Trusted, institutional | Newsreader (large optical size) | Public Sans | Multi-specialty groups, surgery centers |
| Friendly, bright | Young Serif | Figtree | Dental, pediatrics, primary care |
| Calm, very readable | Literata | Atkinson Hyperlegible | Behavioral health, older audiences, eye care |

**Scale.** These are flexible starting ranges. Choose **one coherent scale per project** based on the font's proportions, the brand, content length and viewport, then reuse that small set of styles everywhere. Do not pick a different size for every module.

| Role | Desktop | Mobile | Line height |
|---|---|---|---|
| H1 / hero heading | 48 to 64px | 34 to 42px | 1.05 to 1.18 |
| H2 / section heading | 36 to 44px | 28 to 34px | 1.15 to 1.25 |
| H3 / module heading | 22 to 28px | 21 to 24px | 1.2 to 1.35 |
| H4 / supporting heading | 18 to 20px | 18 to 20px | 1.3 to 1.4 |
| Intro / lead | 19 to 21px | 18 to 19px | 1.5 to 1.65 |
| Body | 17 to 18px | 16 to 18px | 1.5 to 1.7 |
| Eyebrow | 12 to 14px | 12 to 13px | 1.3 to 1.5 |
| Caption / supporting note | 13 to 14px | 13 to 14px | 1.4 to 1.6 |
| Button label | 15 to 17px | 15 to 17px | 1.2 to 1.4 |

Put the chosen scale in Tailwind `@theme` (for example `--text-h1`, `--text-h2`) and in the MUI theme `typography`, with `clamp()` between the mobile and desktop values.

**Rules**
- Keep a visible difference between heading levels. Use semantic heading levels by content structure, independent of visual size.
- Use regular or medium weights when the font gives enough hierarchy. Reserve bold for emphasis; do not make every heading heavy by default.
- Body copy around 45 to 75 characters per line on desktop. Let lines get narrower on mobile; never shrink text to keep desktop wrapping.
- Aim for intentional headline shapes. Adjust text width and scale before adding manual line breaks. Avoid a lone last word and awkward short lines (`text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs).
- Tighten heading tracking slightly only when the font benefits. No cramped letters, clipped accents, or extra tracking in body copy.
- Uppercase and wider tracking only for short labels, used selectively, following the brand's capitalization conventions.
- Eyebrows are optional. Omit them when they repeat the heading.
- Do not rely on pale text, very thin weights or tiny type to look sophisticated.
- Sentence case for headings and buttons unless the brand says otherwise. Form input text at least 16px on mobile.

### 5.6 Layout, spacing and motion

- **Strong asymmetry:** a 12-column grid with uneven spans (7/5, 8/4, 5/7), offset starts, media that breaks the container edge, and overlaps (a photo under the headline, a form card overlapping two sections). Avoid centered, symmetric stacks except for one deliberate moment.
- **Zero fluff padding:** spacing comes from a scale tied to the body line-height (for example 0.5x to 6x). Each section gets the space its content needs, not a blanket `py-24`. No empty wrapper divs, no decorative spacers. Tight is fine; cramped is not.
- **Hierarchy over boxes:** separate content with scale, color fields and alignment before reaching for borders, cards or shadows. When cards are right (directories, provider grids), keep them flat and vary emphasis (one featured item larger) where the content allows.
- **Shadows:** follow the brand guide when it specifies shadows. Otherwise never use short, dark, tight shadows (like `0 1px 3px rgba(0,0,0,.3)` or MUI's default elevations). Use shadows that are **wider and more transparent**: a large blur, a soft downward offset, a negative spread so the edge fades, and low opacity (about 0.06 to 0.14), tinted with the darkest brand neutral instead of pure black. Starting points:
  - Soft (resting cards, panels): `0 12px 32px -8px rgb(<ink> / 0.08)`
  - Raised (forms, overlapping panels): `0 18px 48px -12px rgb(<ink> / 0.10)`
  - Floating (sticky bars, menus, dialogs): `0 24px 64px -16px rgb(<ink> / 0.12)`
  Use them only where a surface truly floats or overlaps; flat content stays flat. Set them once in the MUI theme `shadows` and Tailwind `@theme` (`templates/scaffold/`) so every component shares them.
- **Mobile:** design the 390px view first. Keep asymmetry through bleed, offsets and type scale, not tiny columns.
- **Motion:** two moments at most that the user did not trigger: one orchestrated hero entrance (headline, media and CTA in one short sequence) and the CTA attention motion in conversion mode. Motion that answers an action (accordion opening, form step changing, video opening) is welcome. Respect `prefers-reduced-motion`.

### 5.7 Block treatments in MUI + Tailwind

Tailwind does layout, spacing, type and color. MUI supplies interactive components, restyled through the theme so they never look like stock MUI.

| Block | Treatment |
|---|---|
| Heroes (M01, M02) | Headline from the H1 range with a deliberate shape on the grid, media bleeding off one edge, brand color field or gradient behind. CTA is a MUI `Button` with the unique CTA shape |
| Feature cards (M08) | Not three equal cards. An editorial list: large titles with short text on an asymmetric grid, or one featured item with two smaller ones |
| Stats (M10) | One stat larger in the display face (within the H1 to H2 range), the others smaller beside it, each with plain context |
| Steps (M11) | Real sequence, so numbers are allowed: display numerals (H2 size) on a staggered path |
| Pull quote and reviews (M12, M26) | One large quote set in the display face; other reviews smaller in a scroll-snap row. Stars in a brand tone |
| Tabs (M13) | MUI `Tabs` (vertical on desktop, scrollable on mobile), restyled indicator |
| Comparison (M14) | Plain table with the recommended column on a brand color field |
| FAQ (M31) | MUI `Accordion` with `disableGutters`, no shadow, large question type, rules between items |
| Forms (M29, M30) | MUI `TextField` and `Select` with theme overrides (custom radius, focus color, label style). Multi-step form: MUI `MobileStepper` or a custom progress bar. Quiz: large tappable option cards built on MUI `ToggleButton` or `Radio` |
| Video (M22) | Poster image with a play control; MUI `Dialog` opens the player, which loads only on click |
| Carousel and gallery (M23, M24) | CSS scroll-snap with MUI `IconButton` controls; no carousel library |
| Header and mobile bar (G1, G2, LP) | Thin custom header; MUI `Drawer` for the mobile menu; sticky call/book bar on mobile |
| Insurance strip (M25) | Logos in one tonal color, set on a quiet band, not boxed |
| Icons | Individual imports from `@mui/icons-material` or inline SVG, used sparingly |

### 5.8 Stack and build

Every page is a small **React + Vite + TypeScript** project using **MUI** (current major version, with Emotion) and **Tailwind CSS v4**, built to one self-contained HTML file for preview.

Structure:

```
<page-slug>/
  index.html            # fonts, meta, <!-- Built with create-page vX.Y.Z -->
  vite.config.ts        # react(), tailwindcss(), viteSingleFile()
  src/main.tsx          # StyledEngineProvider enableCssLayer + GlobalStyles layer order + ThemeProvider
  src/theme.ts          # MUI theme from the design plan (palette, typography, shape, component overrides)
  src/index.css         # @layer order, @import "tailwindcss", @theme tokens from the design plan
  src/content.json      # copied from page-content's content.json; components render it, never edit it
  src/blocks/*.tsx      # one component per block, named by ID (M01BHero.tsx), root has data-block="M01-B"
  src/Page.tsx          # the block order from the plan
```

Rules:
- **MUI + Tailwind layering (required):** wrap the app in `<StyledEngineProvider enableCssLayer>`, render `<GlobalStyles styles="@layer theme, base, mui, components, utilities;" />` first, and start `index.css` with `@layer theme, base, mui, components, utilities;` then `@import "tailwindcss";`. Tailwind classes then override MUI without `!important`.
- **One token source:** put the design plan's colors, fonts and spacing in Tailwind `@theme` (for example `--color-summit`, `--font-display`) and use the same values in the MUI theme. No raw hex in components; no pile of arbitrary values like `text-[#123456]`.
- **Style MUI through the theme** (`components.MuiButton.styleOverrides`, and so on) plus `className`. Keep `sx` for rare one-offs.
- **Production-grade Tailwind:** semantic HTML, small readable class lists, responsive prefixes mobile first, no dead classes, no inline styles.
- Forms do not submit anywhere real. Mark the action with `<!-- HIPAA-compliant form endpoint required -->`.
- **Speed, without giving up design:** no extra UI libraries beyond React + MUI + Tailwind, MUI imported per component path, at most 2 font families (`display=swap`), images as compressed WebP with `loading="lazy"` below the fold, video loads only on click. Aim for about 250 KB gzipped for the built file, before images and video. Gradients, grain, SVG shapes and color fields are nearly free in CSS, so speed is never a reason to drop them.
- Build: `npm install`, then `npx vite build`. The preview is `dist/index.html`. Run the checks in section 6 on it.
- Start from `templates/scaffold/`: copy it into the page folder and run `setup.sh`.

### 5.9 Quality floor (always, without announcing it)

Responsive from 360px up, visible keyboard focus, `prefers-reduced-motion` respected, WCAG 2.2 AA contrast, 48px touch targets, one `<h1>`, ordered headings, labels on every field, alt text on every image, skip link. Images: the user's photos when given; otherwise placeholder boxes with the right aspect ratio and a label saying what photo goes there. Never use stock photos of real-looking patients presented as actual patients. No third-party tracking scripts.
