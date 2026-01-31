# Bollywood/Hollywood Frames - Project Guide

## Overview
A movie guessing game where users identify movies from screenshot images within a configurable timer. Supports two themes: **Bollywood** and **Hollywood** with distinct styling, color palettes, and movie datasets. Two implementations exist: Streamlit (Bollywood only) and NiceGUI (full-featured with theme support).

### Target Platforms
The app must look and work well on all of the following:
- **Laptop/desktop browser** (Chrome, Firefox, Edge, Safari)
- **Mobile phones** — Android and iOS (browser + native app via Capacitor)
- **Large displays** — projected or cast to screens up to **65" TV**

## Tech Stack
- **Language:** Python 3.11+
- **Primary Framework:** Streamlit (simpler, Bollywood only)
- **Alternative Framework:** NiceGUI (full-featured, deployed to Render)
- **Data Handling:** Pandas

## Project Structure
```
bollywood-game/
├── app.py                  # Streamlit version (Bollywood only)
├── app_nicegui.py          # NiceGUI version (deployed, theme support)
├── run_streamlit.bat       # Windows launcher for Streamlit
├── run_nicegui.bat         # Windows launcher for NiceGUI
├── requirements.txt        # Python dependencies
├── CLAUDE.md               # This file - project documentation
│
├── data.csv                # Bollywood movie metadata (10 movies)
├── images/                 # Bollywood movie screenshots
│
├── data_hollywood.csv      # Hollywood movie metadata (12 movies)
└── images_hollywood/       # Hollywood movie screenshots
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

---

## Data Format

### CSV Structure
Both `data.csv` and `data_hollywood.csv` use the same format:

| Column | Description | Example |
|--------|-------------|---------|
| `filename` | Image file name (with extension) | `Titanic.png` |
| `movie_name` | Full movie title (the answer) | `Titanic` |
| `hint` | Custom hint text or "No hint" | `"Jack and Rose"` |
| `category` | Genre/category | `Romance` |
| `difficulty` | Easy, Medium, or Hard | `Easy` |

### Current Movie Counts
- **Bollywood:** 10 movies in `data.csv` / `images/`
- **Hollywood:** 12 movies in `data_hollywood.csv` / `images_hollywood/`

> **Note:** Movie libraries for both themes are actively growing. More screenshots will be added over time.

### Hollywood Movies (Current)
| Movie | Category | Difficulty |
|-------|----------|------------|
| A Star Is Born | Romance | Medium |
| Anaconda | Horror | Easy |
| Driving Miss Daisy | Drama | Medium |
| Forrest Gump | Drama | Easy |
| Independence Day | Sci-Fi | Easy |
| Jurassic Park | Sci-Fi | Easy |
| Meet the Parents | Comedy | Easy |
| Scent of a Woman | Drama | Medium |
| Sleepless in Seattle | Romance | Medium |
| Striptease | Drama | Hard |
| The Godfather | Crime | Easy |
| Titanic | Romance | Easy |

### Adding New Movies
1. Add screenshot image to appropriate folder (`images/` or `images_hollywood/`)
2. Add entry to corresponding CSV with matching filename
3. App auto-filters to only show movies with existing image files
4. Restart app to reload data

### Recommended Image Dimensions
- **Aspect ratio: 4:3** (e.g., 1200x900px) — best compromise for both portrait phones and landscape TV/laptop screens
- **Resolution: 1200x900px** — sharp on a 65" TV, reasonable file size
- **Format: PNG or WebP**
- Avoid 16:9 landscape — appears small on mobile phones (width-constrained, leaving empty vertical space)
- Current images are mostly landscape (16:9), which is why they appear small on mobile

---

## Game Mechanics

### Core Gameplay
- Configurable countdown timer per movie (default: 60s solo, 45s team)
- Buttons: **HINT** (💡), **REVEAL** (🎬), **NEXT** (▶)
- Auto-hint generation: shows first letter + character count if no custom hint
- Tracks shown movies to prevent duplicates within session
- Game ends when all movies have been shown

### Game Modes

#### Solo Mode (Default)
- Single player guesses movies
- 60-second timer per round
- Score tracked but not prominently displayed

#### Team Mode
- Two teams compete (toggle on welcome screen)
- Configurable timer (15-120 seconds, default 45s)
- Theme-specific team name pairs (randomizable with 🎲 button)
- Scoring system:
  - **100 points:** Correct in first third of time
  - **75 points:** Correct in middle third
  - **50 points:** Correct in last third
  - **-25 penalty:** If hint was used
- Coordinator marks answers as Correct (✓) or Wrong (✗)
- Teams alternate turns automatically

### Progressive Reveal (NiceGUI only)
The movie image starts blurred and gradually clears as time counts down:
- **Toggle on/off** from welcome screen (enabled by default)
- **Max blur:** 10px at start (recognizable but challenging)
- **Clears linearly** as time decreases
- **Fully clear at 10 seconds remaining** (builds final tension)
- **Scales with timer duration** - shorter timers reveal faster
- **Instant clear** when "REVEAL" button is clicked
- Uses CSS `filter: blur()` with smooth 0.3s transition

---

## Theme System (NiceGUI only)

### Theme Configuration
Themes are defined in the `THEMES` dictionary in `app_nicegui.py`:

```python
THEMES = {
    'bollywood': {
        'name': 'Bollywood Frames',
        'title_text': 'BOLLYWOOD',
        'colors': { ... },
        'csv_file': 'data.csv',
        'image_folder': 'images',
        'team_names': [...],
        'winner_phrases': [...],
        'loser_phrases': [...],
    },
    'hollywood': { ... }
}
```

### Color Palettes

| Element | Bollywood | Hollywood |
|---------|-----------|-----------|
| **Primary** | Gold (#D4AF37) | Silver (#C0C0C0) |
| **Primary Light** | #F4D03F | #E8E8E8 |
| **Primary Dark** | #B8860B | #A0A0A0 |
| **Accent** | Magenta (#E91E63) | Red (#FF4444) |
| **Accent Dark** | #880E4F | #CC0000 |
| **Secondary** | Turquoise (#00BFA5) | Royal Blue (#4169E1) |
| **Background Dark** | #0D0208 | #0A0A0A |
| **Background Mid** | #1A0A14 (Maroon) | #1A1A2E (Navy) |
| **Background Light** | #150520 | #16213E |
| **Text Light** | Cream (#FFF8E7) | White (#FFFFFF) |
| **Text Dark** | #1A0A14 | #1A1A2E |

### Team Name Pairs

**Bollywood:**
- Shahenshah vs Mogambo
- Dilwale vs Dulhania
- Munna vs Circuit
- Jai vs Veeru
- Rahul vs Anjali
- Chulbul vs Pandey
- Gabbar vs Thakur
- Don vs Jaani

**Hollywood:**
- Avengers vs Justice League
- Marvel vs DC
- Jedi vs Sith
- Bond vs Bourne
- Hogwarts vs Mordor
- Gotham vs Metropolis
- Rebels vs Empire
- Autobots vs Decepticons

### Adding a New Theme
1. Add new theme entry to `THEMES` dictionary with all required keys
2. Create corresponding CSV file (e.g., `data_newtheme.csv`)
3. Create image folder (e.g., `images_newtheme/`)
4. Add theme toggle button in `build_welcome_screen()` function
5. CSS is generated dynamically from theme colors - no CSS changes needed

---

## Code Architecture (app_nicegui.py)

### Key Components

| Section | Lines (approx) | Description |
|---------|----------------|-------------|
| Configuration | 1-100 | THEMES dict, constants |
| CSS Generation | 100-400 | `generate_theme_css()`, `generate_body_bg()` |
| Data Loading | 400-450 | `load_data()`, `get_valid_game_data()` |
| GameState Class | 450-600 | All game logic and state |
| UI Functions | 600-1400 | `create_game_ui()` with nested functions |
| App Entry | 1450-1480 | Route definition, `ui.run()` |

### GameState Class Methods
- `_load_theme_data()` - Load CSV/images for current theme
- `get_theme_config()` / `get_theme_colors()` - Access theme settings
- `set_theme(name)` - Switch themes (reloads data)
- `next_movie()` - Pick random unshown movie
- `reset_game()` - Start over
- `calculate_blur()` - Progressive reveal blur amount
- `calculate_points()` / `award_points()` - Team scoring
- `get_winner()` - Determine winning team
- `randomize_team_names()` - Pick new team name pair

### UI Function Structure
```
create_game_ui()
├── update_timer()           # Called every second
├── refresh_game_content()   # Update image, hints, buttons
├── show_game_over()         # Victory screen with confetti
├── start_timer_after_load() # Begin timer when image loads
├── show_hint_click()        # HINT button handler
├── reveal_answer_click()    # REVEAL button handler
├── score_answer()           # Team mode: mark correct/wrong
├── proceed_to_next()        # Advance to next movie
├── next_movie_click()       # NEXT button handler
├── start_new_game()         # PLAY AGAIN handler
├── start_game_from_welcome()# START THE SHOW handler
├── build_welcome_screen()   # Welcome/config screen
└── build_game_screen()      # Main gameplay screen
```

---

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

---

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
- Countdown overlay: 4rem (vs 8rem desktop)
- Image max-height: `35vh`
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

---

## Audio Features

The app includes Web Audio API sound effects (in JavaScript):
- **`playTick(timeLeft)`** - Countdown beeps for last 10 seconds (pitch increases as time runs out)
- **`playVictory()`** - Triumphant chord on game completion
- **`createConfetti()`** - Visual confetti burst on victory

---

## Future Enhancement Ideas

### Gameplay Features
- [ ] Difficulty-based scoring multiplier
- [ ] Leaderboard / high scores persistence
- [ ] More themes (Tollywood, K-Drama, Anime, etc.)
- [ ] Custom theme builder
- [ ] Sound toggle setting
- [ ] Multiplayer over network
- [ ] Movie categories filter on welcome screen
- [ ] Expand movie libraries (ongoing for both Bollywood & Hollywood)

### Mobile App & Monetization
- [ ] **Native mobile app** - Package as installable app for Android (Google Play) and iOS (App Store)
  - Options: PWA, React Native, Flutter, or NiceGUI's native packaging
  - Offline support with bundled images
- [ ] **Monetization strategies to explore:**
  - Freemium model (free base game, paid theme packs)
  - In-app purchases (hint packs, extra time, new movie packs)
  - Ad-supported free tier (interstitial ads between rounds)
  - Premium ad-free version
  - Subscription for unlimited access to all themes
  - One-time purchase for full game
