# Bollywood Frames - Project Guide

## Overview
A Bollywood movie guessing game where users identify movies from screenshot images within a 60-second timer. Two implementations exist: Streamlit (primary) and NiceGUI (alternative).

## Tech Stack
- **Language:** Python 3.11+
- **Primary Framework:** Streamlit
- **Alternative Framework:** NiceGUI (deployed to Render)
- **Data Handling:** Pandas

## Project Structure
```
bollywood-game/
├── app.py              # Streamlit version (main)
├── app_nicegui.py      # NiceGUI version (deployed)
├── run_streamlit.bat   # Windows launcher for Streamlit
├── run_nicegui.bat     # Windows launcher for NiceGUI (supports --network flag)
├── requirements.txt    # Python dependencies
├── data.csv            # Movie metadata (filename, movie_name, hint)
└── images/             # Movie screenshot images (~6MB each)
```

## Running the App

### Streamlit version:
```bash
run_streamlit.bat
# or: streamlit run app.py
```

### NiceGUI version:
```bash
run_nicegui.bat              # localhost only (default)
run_nicegui.bat 30           # with 30 second timer
run_nicegui.bat --network    # accessible from phone on same WiFi
run_nicegui.bat --network 30 # network mode with custom timer
```
Runs on http://localhost:8080

### Mobile Testing
Use `--network` flag to test on phone:
1. Run `run_nicegui.bat --network`
2. Note the IP address printed (e.g., `192.168.1.x`)
3. On phone, visit `http://192.168.1.x:8080`

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Data Format
`data.csv` contains:
- `filename`: Image file name in images/ folder
- `movie_name`: Full movie title (the answer)
- `hint`: Custom hint text or "No hint"

## Game Mechanics
- 60-second countdown timer per movie
- Buttons: Show Hint, Reveal Answer, Next Movie
- Auto-hint generation: shows first letter + character count if no custom hint
- Tracks shown movies to prevent duplicates
- Game ends when all movies have been shown

### Progressive Reveal (NiceGUI only)
The movie image starts blurred and gradually clears as time counts down:
- **Toggle on/off** from the welcome screen (enabled by default)
- **Max blur:** 10px at start (recognizable but challenging)
- **Clears linearly** as time decreases
- **Fully clear at 10 seconds remaining** (builds final tension)
- **Scales with timer duration** - shorter timers reveal faster
- **Instant clear** when "REVEAL" button is clicked
- Uses CSS `filter: blur()` with smooth 0.3s transition

## Architecture Notes
- Streamlit version uses session state + JavaScript injection for timer
- NiceGUI version uses GameState class + native ui.timer()
- Both versions validate that image files exist before including movies
- No tests or CI/CD configured

## Deployment (Render)

NiceGUI version is deployed to Render. GitHub repo: `agunjan24/simple-game`

### Environment Variables (Render)
| Key | Value |
|-----|-------|
| `HOST` | `0.0.0.0` |
| `PYTHON_VERSION` | `3.11.7` |

### Render Settings
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app_nicegui.py`
- **Plan:** Free tier (spins down after 15 min inactivity)

### Local vs Deployed
The app reads `HOST` and `PORT` from environment variables:
- **Local:** Defaults to `127.0.0.1:8080`
- **Render:** Uses `HOST=0.0.0.0` and Render-provided `PORT`

## Mobile Responsive Design

The NiceGUI app uses responsive CSS patterns:

### CSS Techniques Used
- **`clamp(min, preferred, max)`** for fluid typography: `font-size: clamp(1rem, 4vw, 1.8rem)`
- **Tailwind responsive prefixes:** `gap-2 md:gap-4`, `p-4 md:p-6` (for layout only)
- **Media queries** at `max-width: 640px` for mobile-specific overrides

### Important: Tailwind Responsive Classes Limitation
**Tailwind visibility classes like `hidden sm:flex` do NOT work reliably in NiceGUI.**
Use CSS media queries instead for show/hide logic. Tailwind works for spacing/layout but not for conditional rendering.

### Key Mobile Adjustments (in `@media (max-width: 640px)`)
- Buttons: `padding: 6px 10px`, `font-size: 0.7rem`, `border-radius: 20px`
- Timer: 50px circle (vs 80px desktop)
- Countdown overlay: 5rem (vs 12rem desktop)
- Image max-height: `min(50vh, 400px)`
- Game card animation disabled (fixes iOS touch issues)

### iOS Safari/Chrome Compatibility
iOS Chrome uses WebKit (Safari engine). Key fixes applied:
```css
.bollywood-btn {
    touch-action: manipulation;        /* Prevents 300ms tap delay */
    -webkit-tap-highlight-color: transparent;
    -webkit-touch-callout: none;
    user-select: none;
}
```
Also: Disabled `spotlightPulse` animation on mobile as animated transforms on parent elements can block touch events on iOS.

### Testing Mobile Layouts
1. **Browser DevTools:** F12 → Device toggle (Ctrl+Shift+M)
2. **Real device:** Use `run_nicegui.bat --network`
3. **Test on iOS:** iOS Chrome is actually Safari - test touch interactions specifically
