# Reference Details

This file contains detailed reference data moved out of CLAUDE.md to save token budget.
Claude can read this file on demand when specific details are needed.

## Color Palettes

| Element | Bollywood | Hollywood | History |
|---------|-----------|-----------|---------|
| **Primary** | Gold (#D4AF37) | Silver (#C0C0C0) | Parchment Gold (#C9A84C) |
| **Primary Light** | #F4D03F | #E8E8E8 | #E8D5A3 |
| **Primary Dark** | #B8860B | #A0A0A0 | Bronze (#8B6914) |
| **Accent** | Magenta (#E91E63) | Red (#FF4444) | Deep Red (#8B0000) |
| **Accent Dark** | #880E4F | #CC0000 | #5C0000 |
| **Secondary** | Turquoise (#00BFA5) | Royal Blue (#4169E1) | Steel Blue (#4682B4) |
| **Background Dark** | #0D0208 | #0A0A0A | #0A0A0F |
| **Background Mid** | #1A0A14 (Maroon) | #1A1A2E (Navy) | #0F1A2E (Deep Navy) |
| **Background Light** | #150520 | #16213E | #162040 |
| **Text Light** | Cream (#FFF8E7) | White (#FFFFFF) | Parchment (#F5ECD7) |
| **Text Dark** | #1A0A14 | #1A1A2E | #0F1A2E |

## Team Name Pairs

**Bollywood:** Shahenshah vs Mogambo, Dilwale vs Dulhania, Munna vs Circuit, Jai vs Veeru, Rahul vs Anjali, Chulbul vs Pandey, Gabbar vs Thakur, Don vs Jaani

**Hollywood:** Avengers vs Justice League, Marvel vs DC, Jedi vs Sith, Bond vs Bourne, Hogwarts vs Mordor, Gotham vs Metropolis, Rebels vs Empire, Autobots vs Decepticons

**History:** Patriots vs Loyalists, Union vs Confederacy, Federalists vs Republicans, Hamilton vs Burr, North vs South, Eagles vs Redcoats, Founders vs Pioneers, Liberty vs Crown

## Hollywood Movies (Current)

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

## Scoring System (Team Mode)
- **100 points:** Correct in first third of time
- **75 points:** Correct in middle third
- **50 points:** Correct in last third
- **-25 penalty:** If hint was used

## Progressive Reveal
- Max blur: 10px at start, clears linearly, fully clear at 10s remaining
- Uses CSS `filter: blur()` with 0.3s transition
- Toggle on/off from welcome screen

## Mobile CSS Specifics
- Buttons: `padding: 6px 10px`, `font-size: 0.7rem`, `border-radius: 20px`
- Timer: 50px circle (vs 80px desktop)
- Image max-height: `35vh`
- iOS fix: `touch-action: manipulation`, `-webkit-tap-highlight-color: transparent`
- Disabled `spotlightPulse` animation on mobile (blocks touch on iOS)

## GameState Class Methods
- `_load_theme_data()`, `get_theme_config()`, `get_theme_colors()`, `set_theme(name)`
- `next_movie()`, `reset_game()`, `calculate_blur()`
- `calculate_points()`, `award_points()`, `get_winner()`, `randomize_team_names()`

## UI Function Structure
`create_game_ui()` contains: `update_timer()`, `refresh_game_content()`, `show_game_over()`, `start_timer_after_load()`, `show_hint_click()`, `reveal_answer_click()`, `score_answer()`, `proceed_to_next()`, `next_movie_click()`, `start_new_game()`, `start_game_from_welcome()`, `build_welcome_screen()`, `build_game_screen()`

## Audio Features
Web Audio API: `playTick(timeLeft)` (last 10s beeps), `playVictory()` (completion chord), `createConfetti()` (visual burst)

## Deployment (Render)
- Repo: `agunjan24/simple-game`
- Build: `pip install -r requirements.txt`
- Start: `python app_nicegui.py`
- Env: `HOST=0.0.0.0`, `PYTHON_VERSION=3.11.7`
- Free tier (spins down after 15 min)

## Future Enhancement Ideas
- Difficulty-based scoring, leaderboard, more themes (Tollywood, K-Drama, Anime)
- Custom theme builder, sound toggle, multiplayer, category filter
- Native mobile app (PWA/React Native/Flutter)
- Monetization: freemium, IAP, ads, subscription
