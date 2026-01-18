# Bollywood Frames - Project Guide

## Overview
A Bollywood movie guessing game where users identify movies from screenshot images within a 60-second timer. Two implementations exist: Streamlit (primary) and NiceGUI (alternative).

## Tech Stack
- **Language:** Python 3.7+
- **Primary Framework:** Streamlit
- **Alternative Framework:** NiceGUI
- **Data Handling:** Pandas

## Project Structure
```
bollywood-game/
├── app.py              # Streamlit version (main)
├── app_nicegui.py      # NiceGUI version (alternative)
├── requirements.txt    # Python dependencies
├── data.csv            # Movie metadata (filename, movie_name, hint)
└── images/             # Movie screenshot images (~6MB each)
```

## Running the App

### Streamlit version (primary):
```bash
streamlit run app.py
```

### NiceGUI version:
```bash
python app_nicegui.py
```
Runs on http://localhost:8080

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

## Architecture Notes
- Streamlit version uses session state + JavaScript injection for timer
- NiceGUI version uses GameState class + native ui.timer()
- Both versions validate that image files exist before including movies
- No tests or CI/CD configured
