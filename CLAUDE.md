# Bollywood/Hollywood/History Frames - Project Guide

## Overview
A guessing game where users identify movies or historical moments from screenshots within a timer. Three themes: **Bollywood**, **Hollywood**, **History**. Two implementations: Streamlit (Bollywood only) and NiceGUI (full-featured, deployed to Render).

**Target platforms:** Desktop browsers, mobile (Android/iOS via Capacitor), large displays up to 65" TV.

## Tech Stack
Python 3.11+, NiceGUI (primary), Streamlit (legacy), Pandas. Mobile app: Vue 3 + Capacitor.

## Running the App
```bash
run_nicegui.bat              # localhost:8080
run_nicegui.bat --network    # LAN-accessible for phone testing
run_nicegui.bat --network 30 # with 30s timer
streamlit run app.py         # Streamlit version
```

## Project Structure
- `app_nicegui.py` — Main app (NiceGUI, themes, deployed)
- `app.py` — Streamlit version (Bollywood only)
- `data.csv` / `images/` — Bollywood data
- `data_hollywood.csv` / `images_hollywood/` — Hollywood data
- `data_history.csv` / `images_history/` — History data
- `mobile-app/` — Vue 3 + Capacitor mobile app

## Data Format
CSV columns: `filename`, `movie_name`, `hint`, `category`, `difficulty`. Mobile app JSON uses `title` instead of `movie_name`. Add movies by adding image + CSV row; app auto-filters to existing images.

## Architecture (app_nicegui.py)
- **THEMES dict** (~line 1-100): Theme configs with colors, CSV paths, team names
- **CSS Generation** (~100-400): `generate_theme_css()`, `generate_body_bg()`
- **GameState class** (~450-600): Game logic, state, scoring
- **create_game_ui()** (~600-1400): All UI — welcome screen, game screen, handlers
- Themes generate CSS dynamically from color config — no manual CSS needed

## Key Technical Notes
- **Tailwind limitation in NiceGUI:** Visibility classes (`hidden sm:flex`) don't work. Use CSS media queries for show/hide.
- **iOS compatibility:** Use `touch-action: manipulation` and disable animated transforms on mobile to fix touch issues.
- **Images:** Prefer 4:3 aspect ratio, 1200x900px, PNG/WebP.
- **Deployment:** Render free tier, reads `HOST`/`PORT` env vars. Repo: `agunjan24/simple-game`.

## See Also
`REFERENCE.md` — Full color palettes, team name lists, movie lists, scoring details, CSS specifics, future ideas.
