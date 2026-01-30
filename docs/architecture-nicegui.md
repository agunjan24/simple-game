# NiceGUI App Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                      Browser (Client)                   │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  HTML/CSS    │  │  WebSocket   │  │  Web Audio    │  │
│  │  (Rendered   │  │  (Real-time  │  │  API (Ticks,  │  │
│  │   by NiceGUI)│  │   UI updates)│  │   Victory)    │  │
│  └─────────────┘  └──────┬───────┘  └───────────────┘  │
└──────────────────────────┼──────────────────────────────┘
                           │ WebSocket
┌──────────────────────────┼──────────────────────────────┐
│                   Python Server (NiceGUI)                │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │              app_nicegui.py (~1500 lines)        │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐   │    │
│  │  │           THEMES Dictionary               │   │    │
│  │  │  ┌──────────────┐ ┌───────────────────┐  │   │    │
│  │  │  │  Bollywood   │ │    Hollywood      │  │   │    │
│  │  │  │  - colors    │ │    - colors       │  │   │    │
│  │  │  │  - team names│ │    - team names   │  │   │    │
│  │  │  │  - phrases   │ │    - phrases      │  │   │    │
│  │  │  │  - csv_file  │ │    - csv_file     │  │   │    │
│  │  │  │  - image_dir │ │    - image_dir    │  │   │    │
│  │  │  └──────────────┘ └───────────────────┘  │   │    │
│  │  └──────────────────────────────────────────┘   │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐   │    │
│  │  │          CSS Generation                   │   │    │
│  │  │  generate_theme_css(colors) ──> <style>  │   │    │
│  │  │  generate_body_bg(colors)   ──> bg style │   │    │
│  │  └──────────────────────────────────────────┘   │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐   │    │
│  │  │          GameState Class                  │   │    │
│  │  │  - theme / current_movie / time_left     │   │    │
│  │  │  - team_mode / team_scores / team_names  │   │    │
│  │  │  - shown_movies / progressive_reveal     │   │    │
│  │  │  ─────────────────────────────────────── │   │    │
│  │  │  Methods:                                 │   │    │
│  │  │  - set_theme() / next_movie() / reset()  │   │    │
│  │  │  - calculate_blur() / calculate_points() │   │    │
│  │  │  - award_points() / get_winner()         │   │    │
│  │  │  - randomize_team_names()                │   │    │
│  │  └──────────────────────────────────────────┘   │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐   │    │
│  │  │         create_game_ui()                  │   │    │
│  │  │                                           │   │    │
│  │  │  ┌─────────────────────────────────────┐ │   │    │
│  │  │  │       Welcome Screen                 │ │   │    │
│  │  │  │  - Theme toggle (Bollywood/Hollywood)│ │   │    │
│  │  │  │  - Solo / Team mode switch           │ │   │    │
│  │  │  │  - Progressive reveal toggle         │ │   │    │
│  │  │  │  - Team config (names, timer)        │ │   │    │
│  │  │  │  - START THE SHOW button             │ │   │    │
│  │  │  └─────────────────────────────────────┘ │   │    │
│  │  │              │ start_game_from_welcome()  │   │    │
│  │  │              ▼                            │   │    │
│  │  │  ┌─────────────────────────────────────┐ │   │    │
│  │  │  │        Game Screen                   │ │   │    │
│  │  │  │  ┌───────────────────────────────┐  │ │   │    │
│  │  │  │  │ Header: Title + Progress Dots │  │ │   │    │
│  │  │  │  │          + Timer Circle       │  │ │   │    │
│  │  │  │  └───────────────────────────────┘  │ │   │    │
│  │  │  │  ┌───────────────────────────────┐  │ │   │    │
│  │  │  │  │ Image Area                    │  │ │   │    │
│  │  │  │  │  - Movie image (CSS blur)     │  │ │   │    │
│  │  │  │  │  - Countdown overlay          │  │ │   │    │
│  │  │  │  └───────────────────────────────┘  │ │   │    │
│  │  │  │  ┌───────────────────────────────┐  │ │   │    │
│  │  │  │  │ Controls: HINT | REVEAL | NEXT│  │ │   │    │
│  │  │  │  └───────────────────────────────┘  │ │   │    │
│  │  │  │  ┌───────────────────────────────┐  │ │   │    │
│  │  │  │  │ Hint / Answer / Scoreboard    │  │ │   │    │
│  │  │  │  └───────────────────────────────┘  │ │   │    │
│  │  │  └─────────────────────────────────────┘ │   │    │
│  │  │              │ all movies shown           │   │    │
│  │  │              ▼                            │   │    │
│  │  │  ┌─────────────────────────────────────┐ │   │    │
│  │  │  │       Game Over Screen               │ │   │    │
│  │  │  │  - Winner announcement               │ │   │    │
│  │  │  │  - Confetti animation                 │ │   │    │
│  │  │  │  - PLAY AGAIN button                  │ │   │    │
│  │  │  └─────────────────────────────────────┘ │   │    │
│  │  └──────────────────────────────────────────┘   │    │
│  └──────────────────────────────────────────────┘  │    │
│                                                     │    │
│  ┌──────────────┐  ┌──────────────┐                │    │
│  │  data.csv    │  │ data_holly-  │  ◄── Pandas    │    │
│  │  (Bollywood) │  │ wood.csv     │      load_data │    │
│  └──────────────┘  └──────────────┘                │    │
│                                                     │    │
│  ┌──────────────┐  ┌──────────────┐                │    │
│  │  images/     │  │ images_      │  ◄── Served    │    │
│  │  (Bollywood) │  │ hollywood/   │      by NiceGUI│    │
│  └──────────────┘  └──────────────┘                │    │
└─────────────────────────────────────────────────────┘

## Deployment

  Local                              Render (Production)
  ─────                              ───────────────────
  127.0.0.1:8080                     0.0.0.0:PORT
  --network flag for                 Free tier
  phone testing                      (spins down after 15min)
```

## Data Flow

```
Game Round Lifecycle:

  next_movie()
      │
      ▼
  Pick random unshown movie from valid_movies
      │
      ▼
  refresh_game_content()
      ├── Update image (with blur if progressive reveal)
      ├── Update progress dots
      └── Reset hint/answer containers
      │
      ▼
  start_timer_after_load()  ◄── triggered by image onload
      │
      ▼
  update_timer() (every 1s)
      ├── Decrement time_left
      ├── Update timer display
      ├── Recalculate blur (progressive reveal)
      ├── Show countdown overlay (last 10s)
      ├── Play tick sound (last 10s)
      └── Time runs out ──► reveal_answer_click()
      │
      ▼
  User interaction:
      ├── HINT ──► show_hint_click() ──► display hint, set hint_used
      ├── REVEAL ──► reveal_answer_click() ──► show answer, clear blur
      │              └── Team mode: show scoring buttons (✓/✗)
      │                  └── score_answer() ──► award_points()
      └── NEXT ──► next_movie_click()
                   └── All shown? ──► show_game_over()
                   └── More left? ──► next_movie() (loop back)
```

## Timer-Based Scoring (Team Mode)

```
  Total time ──────────────────────────────────► 0
  │          │           │           │          │
  │◄─ 100pts ─►│◄─ 75pts ─►│◄─ 50pts ─►│  time up
  │  1st third  │ 2nd third │ 3rd third │
  │             │           │           │
  └── If hint used: -25 penalty ────────┘
```

## Theme System

```
  set_theme("bollywood")          set_theme("hollywood")
         │                                │
         ▼                                ▼
  ┌──────────────┐                ┌──────────────┐
  │ data.csv     │                │ data_holly-  │
  │ images/      │                │ wood.csv     │
  │ Gold/Magenta │                │ images_holly │
  │ Shahenshah   │                │ Silver/Red   │
  │ vs Mogambo   │                │ Avengers vs  │
  │ ...          │                │ Justice Lgue │
  └──────┬───────┘                └──────┬───────┘
         │                                │
         └──────────┬─────────────────────┘
                    ▼
         generate_theme_css(colors)
                    │
                    ▼
         Dynamic CSS injected via
         ui.add_head_html()
```
