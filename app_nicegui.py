"""
🎬 BOLLYWOOD/HOLLYWOOD FRAMES - Movie Guessing Game
====================================================
A themed movie guessing game with premium, cinematic UI design.
Supports both Bollywood and Hollywood themes with distinct color palettes.

DESIGN PHILOSOPHY:
- Inspired by film awards, movie premieres, and cinematic aesthetics
- Dynamic color palettes based on selected theme
- Typography: Rozha One (dramatic headlines) + Poppins (modern body)
- Elements: Film reels, spotlights, star motifs, metallic accents
- Feel: Premium, celebratory, culturally authentic

THEMES:
- Bollywood: Gold, Magenta, Turquoise, Deep Maroon (Filmfare Awards inspired)
- Hollywood: Silver, Red, Royal Blue, Deep Navy (Academy Awards inspired)
"""

import os
import sys
from pathlib import Path
import pandas as pd
import random
from nicegui import ui, app

# =============================================================================
# CONFIGURATION
# =============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DURATION_SEC = 60

# =============================================================================
# THEME CONFIGURATION - Bollywood & Hollywood
# =============================================================================
THEMES = {
    'bollywood': {
        'name': 'Bollywood Frames',
        'title_text': 'BOLLYWOOD',
        'colors': {
            'primary': '#D4AF37',        # Gold
            'primary_light': '#F4D03F',
            'primary_dark': '#B8860B',
            'accent': '#E91E63',          # Magenta
            'accent_dark': '#880E4F',
            'secondary': '#00BFA5',       # Turquoise
            'bg_dark': '#0D0208',
            'bg_mid': '#1A0A14',          # Maroon
            'bg_light': '#150520',
            'text_light': '#FFF8E7',      # Cream
            'text_dark': '#1A0A14',
        },
        'csv_file': 'data.csv',
        'image_folder': 'images',
        'team_names': [
            ("Shahenshah", "Mogambo"),
            ("Dilwale", "Dulhania"),
            ("Munna", "Circuit"),
            ("Jai", "Veeru"),
            ("Rahul", "Anjali"),
            ("Chulbul", "Pandey"),
            ("Gabbar", "Thakur"),
            ("Don", "Jaani"),
        ],
        'winner_phrases': [
            "Picture abhi baaki hai mere dost... oh wait, you won!",
            "Rishte mein toh hum tumhare baap lagte hain... CHAMPIONS!",
            "Vijay Dinanath Chauhan... WINNER!",
        ],
        'loser_phrases': [
            "Mogambo khush nahi hua!",
            "Kabhi kabhi jeetne ke liye kuch haarna padta hai",
            "Haar kar jeetne wale ko baazigar kehte hain... but not today!",
        ],
    },
    'hollywood': {
        'name': 'Hollywood Frames',
        'title_text': 'HOLLYWOOD',
        'colors': {
            'primary': '#C0C0C0',        # Silver/Platinum
            'primary_light': '#E8E8E8',
            'primary_dark': '#A0A0A0',
            'accent': '#FF4444',          # Red carpet red
            'accent_dark': '#CC0000',
            'secondary': '#4169E1',       # Royal blue
            'bg_dark': '#0A0A0A',
            'bg_mid': '#1A1A2E',          # Deep navy
            'bg_light': '#16213E',
            'text_light': '#FFFFFF',      # White
            'text_dark': '#1A1A2E',
        },
        'csv_file': 'data_hollywood.csv',
        'image_folder': 'images_hollywood',
        'team_names': [
            ("Avengers", "Justice League"),
            ("Marvel", "DC"),
            ("Jedi", "Sith"),
            ("Bond", "Bourne"),
            ("Hogwarts", "Mordor"),
            ("Gotham", "Metropolis"),
            ("Rebels", "Empire"),
            ("Autobots", "Decepticons"),
        ],
        'winner_phrases': [
            "I'll be back... as champion!",
            "You had me at hello... WINNER!",
            "May the Force be with you, champion!",
            "Here's looking at you, WINNER!",
            "To infinity and beyond... CHAMPIONS!",
        ],
        'loser_phrases': [
            "Hasta la vista, baby!",
            "You can't handle the truth!",
            "Here's looking at you, kid... better luck next time!",
            "I am inevitable... your loss!",
            "Frankly, my dear, I don't give a damn about your score!",
        ],
    }
}

def get_timer_duration():
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
            if duration > 0:
                return duration
        except ValueError:
            pass
    return DEFAULT_DURATION_SEC

GAME_DURATION_SEC = get_timer_duration()

# Default theme for initial load
DEFAULT_THEME = 'bollywood'

# =============================================================================
# STYLES - Dynamic Theme-Aware CSS Generation
# =============================================================================

def generate_theme_css(theme_colors):
    """Generate CSS with theme-specific colors."""
    c = theme_colors
    return f'''
    <!-- Google Fonts: Rozha One for dramatic headlines, Poppins for modern body -->
    <link href="https://fonts.googleapis.com/css2?family=Rozha+One&family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet">

    <style>
        /* ===== BASE STYLES ===== */
        * {{
            font-family: 'Poppins', sans-serif;
        }}

        /* ===== HEADLINE FONT ===== */
        .bollywood-title {{
            font-family: 'Rozha One', serif !important;
            letter-spacing: 2px;
        }}

        /* ===== ANIMATIONS ===== */

        /* Primary shimmer effect */
        @keyframes primaryShimmer {{
            0% {{ background-position: -200% center; }}
            100% {{ background-position: 200% center; }}
        }}

        /* Spotlight pulse */
        @keyframes spotlightPulse {{
            0%, 100% {{ opacity: 0.8; transform: scale(1); }}
            50% {{ opacity: 1; transform: scale(1.02); }}
        }}

        /* Star twinkle */
        @keyframes twinkle {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(0.8); }}
        }}

        /* Float up */
        @keyframes floatUp {{
            0% {{ transform: translateY(100px); opacity: 0; }}
            100% {{ transform: translateY(0); opacity: 1; }}
        }}

        /* Glow pulse */
        @keyframes glowPulse {{
            0%, 100% {{ box-shadow: 0 0 20px {c['primary']}80; }}
            50% {{ box-shadow: 0 0 40px {c['primary']}cc, 0 0 60px {c['accent']}66; }}
        }}

        /* Film reel rotation */
        @keyframes reelSpin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        /* Countdown pulse */
        @keyframes countdownPulse {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(1); }}
            50% {{ transform: translate(-50%, -50%) scale(1.1); }}
        }}

        /* Confetti fall */
        @keyframes confettiFall {{
            0% {{ transform: translateY(-100vh) rotate(0deg); opacity: 1; }}
            100% {{ transform: translateY(100vh) rotate(720deg); opacity: 0; }}
        }}

        /* ===== COMPONENT STYLES ===== */

        /* Main title with primary gradient */
        .main-title {{
            font-family: 'Rozha One', serif !important;
            font-size: 3.5rem;
            background: linear-gradient(
                90deg,
                {c['primary']} 0%,
                {c['primary_light']} 25%,
                {c['primary']} 50%,
                {c['primary_light']} 75%,
                {c['primary']} 100%
            );
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: primaryShimmer 3s linear infinite;
            text-shadow: none;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }}

        /* Subtitle styling */
        .subtitle {{
            font-family: 'Poppins', sans-serif;
            color: {c['text_light']};
            font-size: 1.1rem;
            letter-spacing: 4px;
            text-transform: uppercase;
            opacity: 0.9;
        }}

        /* Game card with spotlight effect */
        .game-card {{
            background: linear-gradient(145deg, rgba(255,248,231,0.98), rgba(255,248,231,0.92));
            border-radius: 24px;
            box-shadow:
                0 25px 50px rgba(0,0,0,0.4),
                0 0 100px {c['primary']}33,
                inset 0 1px 0 rgba(255,255,255,0.8);
            animation: spotlightPulse 4s ease-in-out infinite;
            border: 2px solid {c['primary']}4d;
        }}

        /* Film strip decoration */
        .film-strip-border {{
            background: repeating-linear-gradient(
                90deg,
                {c['bg_mid']} 0px,
                {c['bg_mid']} 10px,
                {c['primary']} 10px,
                {c['primary']} 12px,
                {c['bg_mid']} 12px,
                {c['bg_mid']} 22px
            );
            height: 12px;
            border-radius: 12px 12px 0 0;
        }}

        /* Theme button base */
        .bollywood-btn {{
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 0.75rem;
            padding: 8px 18px;
            border-radius: 25px;
            border: 1.5px solid {c['primary']};
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow:
                0 2px 8px rgba(0,0,0,0.2),
                inset 0 1px 0 rgba(255,255,255,0.3);
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
            user-select: none;
        }}

        .bollywood-btn:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow:
                0 8px 25px rgba(0,0,0,0.4),
                0 0 20px {c['primary']}66;
        }}

        .bollywood-btn:active {{
            transform: translateY(0) scale(0.98);
        }}

        @media (pointer: coarse) {{
            .bollywood-btn:active {{
                transform: scale(0.95);
            }}
        }}

        /* Button variants */
        .btn-gold {{
            background: linear-gradient(145deg, {c['primary_light']}, {c['primary']}, {c['primary_dark']});
            color: {c['text_dark']};
        }}

        .btn-magenta {{
            background: linear-gradient(145deg, {c['accent']}, {c['accent']}dd, {c['accent_dark']});
            color: white;
        }}

        .btn-turquoise {{
            background: linear-gradient(145deg, {c['secondary']}, {c['secondary']}dd, {c['secondary']}aa);
            color: white;
        }}

        /* Movie frame */
        .movie-frame {{
            position: relative;
            border-radius: 16px;
            overflow: hidden;
            box-shadow:
                0 10px 40px rgba(0,0,0,0.4),
                0 0 0 4px {c['primary']},
                0 0 0 8px {c['bg_mid']},
                0 0 60px {c['primary']}33;
        }}

        /* Timer styling */
        .timer-container {{
            background: linear-gradient(145deg, {c['primary']}, {c['primary_dark']});
            border-radius: 50%;
            padding: 4px;
            box-shadow:
                0 4px 20px {c['primary']}80,
                inset 0 2px 4px rgba(255,255,255,0.3);
        }}

        .timer-inner {{
            background: linear-gradient(145deg, {c['bg_mid']}, {c['bg_light']});
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .timer-text {{
            font-family: 'Poppins', sans-serif;
            font-weight: 800;
            color: {c['primary']};
            font-size: 1.5rem;
        }}

        /* Hint box */
        .hint-box {{
            background: linear-gradient(145deg, {c['text_light']}, {c['primary_light']}20);
            border: 2px solid {c['primary']};
            border-radius: 12px;
            padding: 16px 24px;
            animation: floatUp 0.5s ease-out;
        }}

        /* Answer reveal */
        .answer-box {{
            background: linear-gradient(145deg, {c['secondary']}20, {c['secondary']}10);
            border: 2px solid {c['secondary']};
            border-radius: 12px;
            padding: 16px 24px;
            animation: floatUp 0.5s ease-out;
        }}

        /* Countdown overlay */
        .countdown-overlay {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Rozha One', serif;
            font-size: 8rem;
            font-weight: 400;
            color: {c['accent']};
            text-shadow:
                0 0 40px {c['accent']}cc,
                0 0 80px {c['accent']}66,
                0 4px 0 {c['accent_dark']};
            z-index: 100;
            pointer-events: none;
            animation: countdownPulse 1s ease-in-out infinite;
        }}

        .image-area-container {{
            position: relative;
        }}

        .star {{
            color: {c['primary']};
            animation: twinkle 1.5s ease-in-out infinite;
        }}

        /* Progress indicator */
        .progress-dots {{
            display: flex;
            gap: 8px;
            justify-content: center;
        }}

        .progress-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: {c['primary']}4d;
            transition: all 0.3s ease;
        }}

        .progress-dot.completed {{
            background: {c['primary']};
            box-shadow: 0 0 10px {c['primary']}80;
        }}

        .progress-dot.current {{
            background: {c['accent']};
            box-shadow: 0 0 15px {c['accent']}99;
            animation: glowPulse 2s infinite;
        }}

        /* Feature 1: Clickable dots for history navigation */
        .progress-dot.clickable {{
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .progress-dot.clickable:hover {{
            transform: scale(1.3);
            box-shadow: 0 0 15px {c['primary']};
        }}

        .progress-dot.reviewing {{
            background: {c['secondary']} !important;
            box-shadow: 0 0 15px {c['secondary']}99;
            animation: glowPulse 2s infinite;
        }}

        /* Feature 2: Clickable timer */
        .timer-clickable {{
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .timer-clickable:hover {{
            transform: scale(1.1);
        }}

        .timer-clickable:active {{
            transform: scale(0.95);
        }}

        /* Feature 3: Clickable image */
        .image-clickable {{
            cursor: pointer;
            transition: box-shadow 0.2s;
        }}

        .image-clickable:hover {{
            box-shadow: 0 10px 50px rgba(0,0,0,0.5);
        }}

        /* Feature 1: Review mode indicator */
        .review-indicator {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .review-badge {{
            background: linear-gradient(135deg, {c['secondary']}, {c['secondary']}cc);
            color: white;
            font-size: clamp(0.8rem, 3vw, 1rem);
            font-weight: 700;
            padding: 6px 16px;
            border-radius: 25px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
        }}

        .back-btn {{
            background: linear-gradient(135deg, #FF7043, #E64A19);
            color: white;
            font-family: 'Poppins', sans-serif;
            font-size: clamp(0.7rem, 2.5vw, 0.85rem);
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 20px;
            border: none;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .back-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}

        .back-btn:active {{
            transform: scale(0.95);
        }}

        /* Confetti */
        .confetti {{
            position: fixed;
            width: 10px;
            height: 10px;
            z-index: 1001;
            animation: confettiFall 3s linear forwards;
        }}

        /* Game over celebration */
        .celebration-container {{
            animation: floatUp 0.8s ease-out;
        }}

        .trophy-icon {{
            font-size: 6rem;
            animation: glowPulse 2s infinite;
        }}

        /* Theme toggle buttons */
        .theme-toggle-btn {{
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 0.85rem;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            touch-action: manipulation;
        }}

        .theme-toggle-btn.inactive {{
            background: transparent;
            border: 2px solid {c['primary']}66;
            color: {c['text_dark']};
            opacity: 0.7;
        }}

        .theme-toggle-btn.active {{
            background: linear-gradient(145deg, {c['primary_light']}, {c['primary']});
            border: 2px solid {c['primary']};
            color: {c['text_dark']};
            box-shadow: 0 2px 10px {c['primary']}66;
        }}

        .theme-toggle-btn:hover {{
            transform: scale(1.05);
        }}

        /* ===== MOBILE RESPONSIVE STYLES ===== */
        @media (max-width: 640px) {{
            .countdown-overlay {{
                font-size: 4rem !important;
            }}

            .main-title {{
                font-size: 2rem;
            }}

            .game-card {{
                animation: none;
            }}

            .bollywood-btn {{
                padding: 6px 10px;
                font-size: 0.7rem;
                border-radius: 20px;
                border-width: 1px;
                letter-spacing: 0;
            }}

            .timer-container {{
                width: 50px !important;
                height: 50px !important;
            }}

            .timer-text {{
                font-size: 0.95rem;
            }}

            .trophy-icon {{
                font-size: 4rem;
            }}

            .game-card {{
                border-radius: 12px;
                margin: 0 !important;
            }}

            .movie-frame {{
                box-shadow:
                    0 5px 20px rgba(0,0,0,0.4),
                    0 0 0 2px {c['primary']},
                    0 0 0 4px {c['bg_mid']};
            }}

            .progress-dot {{
                width: 8px;
                height: 8px;
            }}

            .hint-box, .answer-box {{
                padding: 4px 8px;
                border-radius: 6px;
            }}

            .game-image {{
                max-height: 50vh !important;
                width: 100% !important;
            }}

            .film-strip-border {{
                height: 6px;
            }}

            .progress-dots {{
                gap: 4px;
            }}

            .image-area-container {{
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                min-height: 100px !important;
            }}

            .theme-toggle-btn {{
                font-size: 0.75rem;
                padding: 6px 12px;
            }}
        }}

        .mobile-icon-btn {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .mobile-icon-btn:hover {{
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }}

        .mobile-icon-btn:active {{
            transform: scale(0.95);
        }}
    </style>

    <script>
        let audioCtx = null;

        function playTick(timeLeft) {{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();

            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();

            const freq = 880 + (10 - timeLeft) * 44;
            osc.type = 'sine';
            osc.frequency.value = freq;

            const duration = 0.08 + (timeLeft / 10) * 0.12;

            gain.gain.setValueAtTime(0, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.01);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime + duration - 0.02);
            gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + duration);

            osc.connect(gain);
            gain.connect(audioCtx.destination);

            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }}

        function playVictory() {{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();

            const notes = [523, 659, 784, 1047];
            const now = audioCtx.currentTime;

            notes.forEach((freq, i) => {{
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();

                osc.type = 'sine';
                osc.frequency.value = freq;

                const startTime = now + i * 0.1;
                gain.gain.setValueAtTime(0, startTime);
                gain.gain.linearRampToValueAtTime(0.15, startTime + 0.05);
                gain.gain.setValueAtTime(0.15, startTime + 0.3);
                gain.gain.linearRampToValueAtTime(0, startTime + 0.6);

                osc.connect(gain);
                gain.connect(audioCtx.destination);

                osc.start(startTime);
                osc.stop(startTime + 0.7);
            }});
        }}

        function createConfetti(themeColors) {{
            const colors = themeColors || ['{c['primary']}', '{c['accent']}', '{c['secondary']}', '{c['primary_light']}'];

            for (let i = 0; i < 50; i++) {{
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 2 + 's';
                confetti.style.animationDuration = (2 + Math.random() * 2) + 's';
                document.body.appendChild(confetti);

                setTimeout(() => confetti.remove(), 5000);
            }}
        }}
    </script>
    '''


def generate_body_bg(theme_colors):
    """Generate body background CSS for theme."""
    c = theme_colors
    return f'''
        background:
            radial-gradient(ellipse at top, {c['primary']}1a 0%, transparent 50%),
            radial-gradient(ellipse at bottom, {c['accent']}1a 0%, transparent 50%),
            linear-gradient(180deg, {c['bg_dark']} 0%, {c['bg_mid']} 50%, {c['bg_light']} 100%);
        min-height: 100vh;
    '''

# =============================================================================
# DATA LOADING
# =============================================================================
def load_data(csv_file=None):
    """Loads the CSV and ensures we only use rows where images exist."""
    if csv_file is None:
        csv_file = os.path.join(SCRIPT_DIR, THEMES[DEFAULT_THEME]['csv_file'])
    if not os.path.exists(csv_file):
        return pd.DataFrame()
    df = pd.read_csv(csv_file)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def get_valid_game_data(df, image_folder=None):
    """Filters the dataframe to include only images that actually exist."""
    if image_folder is None:
        image_folder = os.path.join(SCRIPT_DIR, THEMES[DEFAULT_THEME]['image_folder'])
    if df.empty:
        return []
    valid_rounds = []
    for _, row in df.iterrows():
        image_path = os.path.join(image_folder, row['filename'])
        if os.path.exists(image_path):
            valid_rounds.append(row.to_dict())
    return valid_rounds


# =============================================================================
# GAME STATE
# =============================================================================
class GameState:
    """Manages the game logic and state."""

    def __init__(self):
        # Theme support
        self.theme = DEFAULT_THEME
        self._load_theme_data()

        self.shown_movies = []
        self.current_movie = None
        self.time_left = GAME_DURATION_SEC
        self.show_hint = False
        self.show_answer = False
        self.game_over = False
        self.timer_active = False
        self.score = 0  # Track successful guesses (solo mode)
        self.current_screen = 'welcome'  # welcome, game, gameover

        # Team mode properties
        self.team_mode = False
        self.timer_duration = 45  # Default 45s for team mode
        self.team_names = list(random.choice(self.get_theme_config()['team_names']))
        self.team_scores = [0, 0]  # [Team A score, Team B score]
        self.current_team = 0  # 0 = Team A, 1 = Team B
        self.hint_used = False  # Track if hint was used this round
        self.awaiting_score = False  # Waiting for coordinator to mark correct/wrong

        # Progressive reveal setting
        self.progressive_reveal = True  # Image starts blurred and clears over time

        # Feature 1: History navigation (review mode)
        self.reviewing_movie = None  # Movie being reviewed (or None)
        self.saved_time_left = None  # Saved timer when entering review
        self.saved_timer_active = False  # Saved timer state

        # Feature 2: Timer pause
        self.timer_paused = False  # Timer manually paused by clicking

        # Feature 3: Image click to clear blur
        self.image_revealed = False  # Image blur cleared by clicking

    def _load_theme_data(self):
        """Load data for current theme."""
        config = self.get_theme_config()
        csv_path = os.path.join(SCRIPT_DIR, config['csv_file'])
        image_folder = os.path.join(SCRIPT_DIR, config['image_folder'])
        self.df = load_data(csv_path)
        self.valid_movies = get_valid_game_data(self.df, image_folder)

    def get_theme_config(self):
        """Get configuration for current theme."""
        return THEMES[self.theme]

    def get_theme_colors(self):
        """Get color palette for current theme."""
        return self.get_theme_config()['colors']

    def set_theme(self, theme_name):
        """Switch to a different theme."""
        if theme_name in THEMES:
            self.theme = theme_name
            self._load_theme_data()
            self.randomize_team_names()
            # Reset shown movies when switching themes
            self.shown_movies = []

    def get_image_folder(self):
        """Get the image folder path for current theme."""
        return os.path.join(SCRIPT_DIR, self.get_theme_config()['image_folder'])

    def next_movie(self):
        """Pick a random movie that hasn't been shown yet."""
        available = [m for m in self.valid_movies if m['filename'] not in self.shown_movies]

        if available:
            self.current_movie = random.choice(available)
            self.shown_movies.append(self.current_movie['filename'])
            # Use configured timer duration for team mode, default for solo
            self.time_left = self.timer_duration if self.team_mode else GAME_DURATION_SEC
            self.show_hint = False
            self.show_answer = False
            self.hint_used = False
            self.awaiting_score = False
            self.game_over = False
            self.timer_active = False  # Don't start timer until image loads
            # Reset Feature 2 & 3 state for new movie
            self.timer_paused = False
            self.image_revealed = False
            return True
        else:
            self.game_over = True
            self.current_movie = None
            self.timer_active = False
            self.current_screen = 'gameover'
            return False

    def reset_game(self):
        """Reset the game to start over."""
        self.shown_movies = []
        self.game_over = False
        self.score = 0
        self.current_screen = 'game'
        # Reset team mode properties
        if self.team_mode:
            self.team_scores = [0, 0]
            self.current_team = 0
        self.next_movie()

    def randomize_team_names(self):
        """Pick a new random pair of team names from current theme."""
        self.team_names = list(random.choice(self.get_theme_config()['team_names']))

    def switch_team(self):
        """Switch to the other team."""
        self.current_team = 1 - self.current_team

    def get_current_team_name(self):
        """Get the name of the current team."""
        return self.team_names[self.current_team]

    def calculate_points(self, correct: bool) -> int:
        """Calculate points based on time remaining and hint usage."""
        if not correct:
            return 0

        # Calculate time-based points (proportional to timer duration)
        duration = self.timer_duration if self.team_mode else GAME_DURATION_SEC
        time_ratio = self.time_left / duration

        # Feature 2 & 3: Timer paused or image revealed locks to last-third rate (50 points)
        if self.timer_paused or self.image_revealed:
            points = 50
        elif time_ratio > 0.66:  # First third of time
            points = 100
        elif time_ratio > 0.33:  # Middle third
            points = 75
        else:  # Last third
            points = 50

        # Hint penalty: -25 points
        if self.hint_used:
            points = max(0, points - 25)

        return points

    def award_points(self, correct: bool):
        """Award points to the current team (or solo score)."""
        points = self.calculate_points(correct)
        if self.team_mode:
            self.team_scores[self.current_team] += points
        else:
            self.score += points
        return points

    def get_winner(self):
        """Get the winning team index and phrase. Returns (winner_index, is_tie)."""
        if self.team_scores[0] > self.team_scores[1]:
            return 0, False
        elif self.team_scores[1] > self.team_scores[0]:
            return 1, False
        else:
            return -1, True  # Tie

    def remaining_count(self):
        """Count of movies not yet shown."""
        return len(self.valid_movies) - len(self.shown_movies)

    def get_timer_duration(self):
        """Get the current timer duration based on game mode."""
        return self.timer_duration if self.team_mode else GAME_DURATION_SEC

    def calculate_blur(self):
        """
        Calculate blur amount based on time remaining.
        Returns blur in pixels (max 10px, clears to 0 at 10s remaining).
        Scales automatically with timer duration.
        Returns 0 if progressive reveal is disabled.
        """
        if not self.progressive_reveal:
            return 0
        # Feature 2 & 3: Instant clear when timer paused or image revealed
        if self.timer_paused or self.image_revealed:
            return 0
        total_time = self.get_timer_duration()
        # Clear blur completely in last 10 seconds
        if self.time_left <= 10:
            return 0
        # Calculate ratio: starts at 1.0 (full blur), decreases to 0
        ratio = (self.time_left - 10) / (total_time - 10)
        max_blur = 10  # Maximum blur in pixels (recognizable but challenging)
        return round(ratio * max_blur, 1)

    def total_count(self):
        """Total number of movies."""
        return len(self.valid_movies)

    def shown_count(self):
        """Number of movies shown."""
        return len(self.shown_movies)

    def get_hint_text(self):
        """Generate hint text."""
        if not self.current_movie:
            return ""
        custom_hint = self.current_movie.get('hint', '')
        if pd.isna(custom_hint) or custom_hint == '' or custom_hint == '"No hint"':
            movie_name = self.current_movie['movie_name']
            return f"Starts with '{movie_name[0]}' • {len(movie_name)} characters"
        return custom_hint.strip('"')

    def get_hint_text_for_movie(self, movie):
        """Generate hint text for a specific movie (used in review mode)."""
        if not movie:
            return ""
        custom_hint = movie.get('hint', '')
        if pd.isna(custom_hint) or custom_hint == '' or custom_hint == '"No hint"':
            movie_name = movie['movie_name']
            return f"Starts with '{movie_name[0]}' • {len(movie_name)} characters"
        return custom_hint.strip('"')

    # Feature 1: History navigation (review mode)
    def is_reviewing(self):
        """Check if currently in review mode."""
        return self.reviewing_movie is not None

    def enter_review(self, index):
        """Enter review mode to view a previously shown movie."""
        if index < 0 or index >= len(self.shown_movies) - 1:
            return  # Can't review current or future movies
        filename = self.shown_movies[index]
        movie = next((m for m in self.valid_movies if m['filename'] == filename), None)
        if not movie:
            return

        # Save current game state
        self.saved_time_left = self.time_left
        self.saved_timer_active = self.timer_active
        self.reviewing_movie = movie
        # Pause timer while reviewing
        self.timer_active = False

    def exit_review(self):
        """Exit review mode and return to current game."""
        if not self.reviewing_movie:
            return
        self.reviewing_movie = None
        # Restore saved time but keep timer paused (user must click timer to resume)
        if self.saved_time_left is not None:
            self.time_left = self.saved_time_left
            self.saved_time_left = None
        # Timer stays paused - user clicks timer to resume (consistent with Feature 2)
        self.saved_timer_active = False


# =============================================================================
# MAIN UI
# =============================================================================
def create_game_ui():
    """Creates the main game interface with Bollywood theming."""

    game = GameState()

    # UI element references
    main_container = None
    timer_display = None
    timer_container_el = None  # Reference to timer for class updates
    countdown_overlay = None
    image_container = None
    image_element = None  # Reference to image for blur updates
    hint_container = None
    answer_container = None
    progress_container = None
    next_btn = None
    # Team mode UI elements
    scoreboard_container = None
    scoring_buttons_container = None

    # ---------- TIMER UPDATE ----------
    def update_timer():
        """Called every second to update the countdown."""
        if not game.timer_active:
            return

        game.time_left -= 1

        # Update timer display
        minutes = game.time_left // 60
        seconds = game.time_left % 60
        timer_display.set_text(f"{minutes}:{seconds:02d}")

        # Update progressive blur on image
        if image_element and not game.show_answer:
            blur = game.calculate_blur()
            image_element.style(
                f'max-height: min(55vh, 450px); object-fit: contain; '
                f'filter: blur({blur}px); transition: filter 0.3s ease-out;'
            )

        # Countdown overlay for last 10 seconds
        if not countdown_overlay:
            return

        if game.time_left <= 10 and game.time_left > 0:
            countdown_overlay.set_text(str(game.time_left))
            countdown_overlay.style('display: block;')
            ui.run_javascript(f'playTick({game.time_left})')
        elif game.time_left <= 0:
            game.timer_active = False
            # Auto-reveal answer when time's up
            game.show_answer = True
            refresh_game_content()
            # Show timeout clock AFTER refresh (which recreates countdown_overlay)
            if countdown_overlay:
                countdown_overlay.set_text("⏰")
                countdown_overlay.style('display: block; font-size: 4rem;')
                # Hide the clock after a brief moment
                ui.timer(2.0, lambda: countdown_overlay.style('display: none;') if countdown_overlay else None, once=True)
        else:
            countdown_overlay.style('display: none;')

    # ---------- UI REFRESH ----------
    def refresh_game_content():
        """Refresh the game content area."""

        # Update progress dots
        progress_container.clear()
        with progress_container:
            with ui.row().classes('progress-dots'):
                for i in range(game.total_count()):
                    dot_class = 'progress-dot'
                    if i < game.shown_count() - 1:
                        dot_class += ' completed clickable'
                        # Check if this dot is the one being reviewed
                        if game.is_reviewing() and game.shown_movies[i] == game.reviewing_movie['filename']:
                            dot_class += ' reviewing'
                    elif i == game.shown_count() - 1 and not game.is_reviewing():
                        dot_class += ' current'
                    dot = ui.element('div').classes(dot_class)
                    # Make completed dots clickable
                    if i < game.shown_count() - 1:
                        dot.on('click', lambda e, idx=i: on_dot_click(idx))

        if game.game_over:
            show_game_over()
            return

        # Determine which movie to display (review mode or current)
        display_movie = game.reviewing_movie if game.is_reviewing() else game.current_movie

        if display_movie:
            # Update image and countdown overlay
            nonlocal countdown_overlay, image_element
            image_container.clear()
            with image_container:
                # Image with onload handler to start timer
                img_path = os.path.join(game.get_image_folder(), display_movie['filename'])
                # In review mode: no blur. Normal mode: blur based on answer state and time
                if game.is_reviewing():
                    blur = 0
                else:
                    blur = 0 if game.show_answer else game.calculate_blur()

                # Determine if image should be clickable (Feature 3, one-way action)
                image_clickable = not game.is_reviewing() and not game.show_answer and not game.image_revealed and blur > 0
                image_classes = 'max-w-full rounded-lg game-image' + (' image-clickable' if image_clickable else '')

                image_element = ui.image(img_path).classes(image_classes).style(
                    f'max-height: min(55vh, 450px); object-fit: contain; '
                    f'filter: blur({blur}px); transition: filter 0.3s ease-out;'
                )
                # Add click handler for image (Feature 3)
                if image_clickable:
                    image_element.on('click', on_image_click)
                # Start timer when image loads (only in normal mode)
                image_element.on('load', lambda: start_timer_after_load())
                # Re-create countdown overlay inside image container (only in normal mode)
                if not game.is_reviewing():
                    countdown_overlay = ui.label("").classes('countdown-overlay').style('display: none;')

            # Update hint - more compact
            hint_container.clear()
            # In review mode, use local review state; in normal mode, use game state
            show_hint_now = review_show_hint['value'] if game.is_reviewing() else game.show_hint
            if show_hint_now:
                hint_text = game.get_hint_text_for_movie(display_movie) if game.is_reviewing() else game.get_hint_text()
                with hint_container:
                    with ui.element('div').classes('hint-box').style('padding: 6px 12px; margin-top: 4px;'):
                        ui.label(f"💡 {hint_text}").style(
                            'color: #1A0A14; font-size: clamp(0.8rem, 2.5vw, 1rem);'
                        )

            # Update answer - more compact
            answer_container.clear()
            # In review mode, use local review state; in normal mode, use game state
            show_answer_now = review_show_answer['value'] if game.is_reviewing() else game.show_answer
            if show_answer_now:
                with answer_container:
                    with ui.element('div').classes('answer-box').style('padding: 6px 12px; margin-top: 4px;'):
                        ui.label(f"🎬 {display_movie['movie_name']}").classes('movie-answer-text').style(
                            'color: #1A0A14; font-size: clamp(0.9rem, 3.5vw, 1.5rem); font-weight: 700; '
                            'font-family: "Rozha One", serif;'
                        )

            # Update next button (only in normal mode)
            if not game.is_reviewing() and next_btn:
                remaining = game.remaining_count()
                if remaining > 0:
                    next_btn.set_text("▶ NEXT")
                else:
                    next_btn.set_text("🏆 FINISH")

    # ---------- GAME OVER SCREEN ----------
    def show_game_over():
        """Display the game over celebration screen."""
        game.timer_active = False
        if countdown_overlay:
            countdown_overlay.style('display: none;')
        main_container.clear()

        with main_container:
            ui.run_javascript('playVictory(); createConfetti();')

            with ui.column().classes('celebration-container w-full items-center gap-6 py-8'):
                # Trophy
                ui.label("🏆").classes('trophy-icon')

                if game.team_mode:
                    # Team mode ending
                    winner_idx, is_tie = game.get_winner()

                    if is_tie:
                        ui.label("IT'S A TIE!").classes('main-title').style(
                            'font-size: clamp(1.5rem, 7vw, 2.5rem); white-space: nowrap;'
                        )
                        ui.label("Both teams are winners!").style(
                            'color: #1A0A14; font-size: 1.1rem; opacity: 0.8;'
                        )
                    else:
                        winner_name = game.team_names[winner_idx]
                        winner_emoji = "🔴" if winner_idx == 0 else "🔵"
                        winner_color = "#E91E63" if winner_idx == 0 else "#2196F3"
                        loser_idx = 1 - winner_idx

                        ui.label(f"{winner_emoji} {winner_name} WINS!").classes('main-title').style(
                            f'font-size: clamp(1.3rem, 6vw, 2.2rem); white-space: nowrap; color: {winner_color};'
                        )

                        # Theme-appropriate winner phrase
                        phrase = random.choice(game.get_theme_config()['winner_phrases'])
                        ui.label(f'"{phrase}"').style(
                            'color: #1A0A14; font-size: clamp(0.8rem, 3vw, 1rem); font-style: italic; '
                            'opacity: 0.8; text-align: center; max-width: 300px;'
                        )

                    # Final scores
                    ui.label("✦ ✦ ✦").style(f'color: {game.get_theme_colors()["primary"]}; font-size: 1rem; letter-spacing: 12px; margin: 8px 0;')

                    with ui.row().classes('gap-8'):
                        # Team A final score
                        team_a_winner = winner_idx == 0 if not is_tie else False
                        with ui.column().classes('items-center'):
                            ui.label(f"🔴 {game.team_names[0]}").style(
                                f'color: #E91E63; font-weight: {"800" if team_a_winner else "600"}; font-size: 1rem;'
                            )
                            ui.label(f"{game.team_scores[0]}").style(
                                f'color: #1A0A14; font-size: {"2rem" if team_a_winner else "1.5rem"}; font-weight: 700;'
                            )
                            ui.label("points").style('color: #666; font-size: 0.8rem;')

                        # Team B final score
                        team_b_winner = winner_idx == 1 if not is_tie else False
                        with ui.column().classes('items-center'):
                            ui.label(f"🔵 {game.team_names[1]}").style(
                                f'color: #2196F3; font-weight: {"800" if team_b_winner else "600"}; font-size: 1rem;'
                            )
                            ui.label(f"{game.team_scores[1]}").style(
                                f'color: #1A0A14; font-size: {"2rem" if team_b_winner else "1.5rem"}; font-weight: 700;'
                            )
                            ui.label("points").style('color: #666; font-size: 0.8rem;')

                    # Loser phrase (if not tie)
                    if not is_tie:
                        loser_phrase = random.choice(game.get_theme_config()['loser_phrases'])
                        loser_emoji = "🔵" if winner_idx == 0 else "🔴"
                        ui.label(f'{loser_emoji} {loser_phrase}').style(
                            'color: #666; font-size: 0.85rem; font-style: italic; margin-top: 8px;'
                        )
                else:
                    # Solo mode ending
                    ui.label("PICTURE PERFECT!").classes('main-title').style(
                        'font-size: clamp(1.5rem, 7vw, 2.5rem); white-space: nowrap;'
                    )
                    ui.label(f"You've seen all {game.total_count()} movies!").style(
                        'color: #1A0A14; font-size: 1.3rem; opacity: 0.8;'
                    )

                # Decorative stars
                ui.label("⭐ 🌟 ⭐ 🌟 ⭐").style('font-size: 2rem; margin: 16px 0;')

                # Play again button
                ui.button("🎬 PLAY AGAIN", on_click=start_new_game).classes(
                    'bollywood-btn btn-gold'
                ).style('font-size: 1.1rem; padding: 18px 48px;')

    # ---------- TIMER START (after image loads) ----------
    def start_timer_after_load():
        """Start the timer once the image has loaded."""
        # Don't auto-start timer in review mode
        if game.is_reviewing():
            return
        if not game.timer_active and not game.show_answer and not game.game_over:
            game.timer_active = True

    # ---------- FEATURE 1: History Navigation (Review Mode) ----------
    # Local state for review mode hint/answer display
    review_show_hint = {'value': False}
    review_show_answer = {'value': False}

    def on_dot_click(index):
        """Handle click on a completed progress dot."""
        # Only allow clicking completed dots (not current or future)
        if index >= game.shown_count() - 1:
            return
        if game.is_reviewing():
            # If already reviewing, can switch to different completed item
            if index < game.shown_count() - 1:
                game.enter_review(index)
                review_show_hint['value'] = False
                review_show_answer['value'] = False
                build_game_screen()  # Rebuild to show review mode
            return
        # Stop timer and enter review mode
        game.timer_active = False
        game.enter_review(index)
        review_show_hint['value'] = False
        review_show_answer['value'] = False
        build_game_screen()  # Rebuild to show review mode

    def exit_review_mode():
        """Exit review mode and return to current game."""
        game.exit_review()
        review_show_hint['value'] = False
        review_show_answer['value'] = False
        build_game_screen()  # Rebuild for normal game

    def show_review_hint():
        """Show hint in review mode."""
        review_show_hint['value'] = True
        refresh_game_content()

    def show_review_answer():
        """Show answer in review mode."""
        review_show_answer['value'] = True
        refresh_game_content()

    # ---------- FEATURE 2: Click Timer to Pause ----------
    def on_timer_click():
        """Handle click on the timer to pause (one-way action)."""
        if game.is_reviewing():
            return  # No timer interaction in review mode
        if game.show_answer:
            return  # Answer already revealed
        if game.game_over:
            return  # Game is over
        if game.timer_paused:
            return  # Already paused - no restart allowed

        if game.timer_active:
            # Pause the timer (one-way action - user uses nav buttons when ready)
            game.timer_active = False
            game.timer_paused = True
            # Blur clears instantly (handled in calculate_blur)
            # Answer stays hidden (show_answer remains False)
            if countdown_overlay:
                countdown_overlay.style('display: none;')
            # Remove clickable class from timer (no more hand cursor)
            if timer_container_el:
                timer_container_el.classes(remove='timer-clickable')
            # Update image to clear blur and remove clickable class
            if image_element:
                image_element.classes(remove='image-clickable')
                image_element.style(
                    'max-height: min(55vh, 450px); object-fit: contain; '
                    'filter: blur(0px); transition: filter 0.3s ease-out;'
                )

    # ---------- FEATURE 3: Click Image to Clear Blur ----------
    def on_image_click():
        """Handle click on the image to clear blur."""
        if game.is_reviewing():
            return  # No effect in review mode
        if game.show_answer:
            return  # Already revealed
        if game.calculate_blur() == 0:
            return  # Already clear

        game.image_revealed = True
        # Timer continues (we don't stop it)
        # Answer stays hidden (show_answer remains False)
        # Update image to clear blur and remove clickable class (no more hand cursor)
        if image_element:
            image_element.classes(remove='image-clickable')
            image_element.style(
                'max-height: min(55vh, 450px); object-fit: contain; '
                'filter: blur(0px); transition: filter 0.3s ease-out;'
            )

    # ---------- BUTTON HANDLERS ----------
    def show_hint_click():
        game.show_hint = True
        game.hint_used = True  # Track for scoring penalty
        refresh_game_content()

    def reveal_answer_click():
        game.show_answer = True
        game.timer_active = False
        # Clear blur instantly on reveal
        if image_element:
            image_element.style(
                'max-height: min(55vh, 450px); object-fit: contain; '
                'filter: blur(0px); transition: filter 0.3s ease-out;'
            )
        # In team mode, show scoring buttons
        if game.team_mode:
            game.awaiting_score = True
            if scoring_buttons_container:
                scoring_buttons_container.clear()
                with scoring_buttons_container:
                    # Simple icon buttons for scoring - colored icons on light backgrounds
                    ui.button("✓", on_click=lambda: score_answer(True)).style(
                        'background: white; color: #2E7D32; border: 3px solid #4CAF50; '
                        'border-radius: 50%; width: 40px; height: 40px; min-width: 40px; '
                        'font-size: 1.4rem; font-weight: 900; padding: 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15);'
                    ).tooltip('Correct - award points')
                    ui.button("✗", on_click=lambda: score_answer(False)).style(
                        'background: white; color: #C62828; border: 3px solid #F44336; '
                        'border-radius: 50%; width: 40px; height: 40px; min-width: 40px; '
                        'font-size: 1.4rem; font-weight: 900; padding: 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15);'
                    ).tooltip('Wrong - no points')
                scoring_buttons_container.style('display: flex;')
        refresh_game_content()

    def score_answer(correct: bool):
        """Handle coordinator marking answer as correct or wrong."""
        points = game.award_points(correct)
        game.awaiting_score = False

        # Hide scoring buttons
        if scoring_buttons_container:
            scoring_buttons_container.style('display: none;')

        # Show points awarded notification
        if correct and points > 0:
            ui.notify(f"+{points} points for {game.get_current_team_name()}!", color='positive')
        elif not correct:
            ui.notify(f"No points - switching teams", color='warning')

        # Switch teams and go to next movie
        proceed_to_next()

    def proceed_to_next():
        """Move to next movie, switching teams in team mode."""
        if game.team_mode:
            game.switch_team()

        if game.remaining_count() > 0:
            game.next_movie()
            if countdown_overlay:
                countdown_overlay.style('display: none;')
            build_game_screen()  # Rebuild to update turn indicator
        else:
            show_game_over()

    def next_movie_click():
        # In team mode with awaiting score, don't allow skipping
        if game.team_mode and game.awaiting_score:
            ui.notify("Please mark the answer as Correct or Wrong first!", color='warning')
            return

        # In team mode, auto-score as wrong if skipping without reveal
        if game.team_mode and not game.show_answer:
            game.award_points(False)

        proceed_to_next()

    def start_new_game():
        game.reset_game()
        if countdown_overlay:
            countdown_overlay.style('display: none;')
        build_game_screen()

    def start_game_from_welcome():
        game.current_screen = 'game'
        game.next_movie()
        build_game_screen()

    # ---------- WELCOME SCREEN ----------
    def build_welcome_screen():
        """Build the dramatic welcome/splash screen with theme toggle."""
        main_container.clear()

        # Container references for dynamic updates
        team_options_container = None
        team_names_label = None
        timer_label = None
        title_label = None
        movie_count_label = None
        bollywood_btn = None
        hollywood_btn = None

        def select_theme(theme_name):
            """Switch to selected theme and refresh welcome screen."""
            game.set_theme(theme_name)
            # Refresh styles for new theme
            ui.query('body').style(generate_body_bg(game.get_theme_colors()))
            # Rebuild welcome screen with new theme
            build_welcome_screen()

        def toggle_team_mode(e):
            """Toggle between solo and team mode."""
            game.team_mode = e.value
            if team_options_container:
                team_options_container.style(f"display: {'flex' if e.value else 'none'};")
            update_timer_label()

        def randomize_names():
            """Randomize team names and update display."""
            game.randomize_team_names()
            if team_names_label:
                team_names_label.set_text(f"🔴 {game.team_names[0]}  vs  🔵 {game.team_names[1]}")

        def update_timer_duration(e):
            """Update timer duration from input."""
            try:
                game.timer_duration = int(e.value)
            except ValueError:
                game.timer_duration = 45
            update_timer_label()

        def update_timer_label():
            """Update the timer info label."""
            if timer_label:
                duration = game.timer_duration if game.team_mode else GAME_DURATION_SEC
                timer_label.set_text(f"⏱️ {duration} seconds per round")

        # Get current theme config
        theme_config = game.get_theme_config()
        colors = game.get_theme_colors()

        with main_container:
            with ui.column().classes('w-full items-center justify-center gap-1 sm:gap-2 md:gap-4 py-2 sm:py-4 md:py-6'):
                # Film reel decoration
                ui.label("🎞️").style('font-size: clamp(1.5rem, 6vw, 3rem); animation: reelSpin 4s linear infinite;')

                # Main title - dynamic based on theme
                title_label = ui.label(theme_config['title_text']).classes('main-title').style(
                    'font-size: clamp(1.8rem, 8vw, 3rem); margin-bottom: -8px;'
                )
                ui.label("FRAMES").classes('main-title').style('font-size: clamp(1.8rem, 8vw, 3rem);')

                # Subtitle
                ui.label("THE ULTIMATE MOVIE GUESSING GAME").style(
                    f'color: {colors["text_dark"]}; font-size: clamp(0.6rem, 2.5vw, 0.95rem); letter-spacing: 2px; '
                    'text-transform: uppercase; opacity: 0.7; margin-top: 4px;'
                )

                # Decorative elements
                ui.label("✦ ✦ ✦").style(f'color: {colors["primary"]}; font-size: 1rem; letter-spacing: 12px; margin: 2px 0;')

                # ---------- THEME TOGGLE ----------
                with ui.row().classes('items-center gap-2 mt-1'):
                    bollywood_btn = ui.button("🎬 Bollywood", on_click=lambda: select_theme('bollywood')).classes(
                        f'theme-toggle-btn {"active" if game.theme == "bollywood" else "inactive"}'
                    )
                    hollywood_btn = ui.button("🎥 Hollywood", on_click=lambda: select_theme('hollywood')).classes(
                        f'theme-toggle-btn {"active" if game.theme == "hollywood" else "inactive"}'
                    )

                # Movie count info - uses current theme's data
                movie_count = len(game.valid_movies)
                movie_count_label = ui.label(f"🎬 {movie_count} Movies to Guess").style(
                    f'color: {colors["text_dark"]}; font-size: clamp(0.9rem, 3vw, 1.1rem); font-weight: 600; margin-top: 2px;'
                )

                # ---------- GAME OPTIONS ----------
                with ui.column().classes('items-center gap-1 sm:gap-2 mt-2 sm:mt-4'):
                    # Team mode toggle
                    with ui.row().classes('items-center gap-4'):
                        ui.label("Game Mode:").style(f'color: {colors["text_dark"]}; font-weight: 600;')
                        ui.switch("Team Battle", value=game.team_mode, on_change=toggle_team_mode).style(
                            f'color: {colors["accent_dark"]};'
                        )

                    # Progressive reveal toggle
                    with ui.row().classes('items-center gap-4'):
                        ui.label("Progressive Reveal:").style(f'color: {colors["text_dark"]}; font-weight: 600;')
                        ui.switch("", value=game.progressive_reveal,
                                  on_change=lambda e: setattr(game, 'progressive_reveal', e.value)).style(
                            f'color: {colors["secondary"]};'
                        ).tooltip('Image starts blurred and clears over time')

                # ---------- TEAM OPTIONS (shown when team mode enabled) ----------
                team_options_container = ui.column().classes('items-center gap-1 sm:gap-3 mt-1 sm:mt-2 w-full')
                team_options_container.style(f"display: {'flex' if game.team_mode else 'none'};")

                with team_options_container:
                    # Team names display - centered with dice on right
                    with ui.element('div').style(
                        'display: flex; justify-content: center; width: 100%; position: relative;'
                    ):
                        # Centered team names (no wrap)
                        team_names_label = ui.label(f"🔴 {game.team_names[0]}  vs  🔵 {game.team_names[1]}").style(
                            f'color: {colors["text_dark"]}; font-size: clamp(0.85rem, 3.5vw, 1.3rem); font-weight: 700; '
                            f'background: {colors["primary"]}33; padding: 8px 16px; border-radius: 8px; '
                            'text-align: center; white-space: nowrap;'
                        )
                        # Dice icon positioned to the right of the label
                        ui.button("🎲", on_click=randomize_names).style(
                            'background: transparent; border: none; font-size: 1.3rem; cursor: pointer; '
                            'padding: 2px; min-width: auto; box-shadow: none; margin-left: 4px;'
                        ).props('flat dense').tooltip('Randomize team names')

                    # Timer configuration
                    with ui.row().classes('items-center justify-center gap-2'):
                        ui.label("⏱️ Timer:").style(f'color: {colors["text_dark"]}; font-size: 0.9rem;')
                        ui.number(value=game.timer_duration, min=15, max=120, step=5,
                                  on_change=update_timer_duration).style(
                            'width: 70px;'
                        ).props('dense outlined')
                        ui.label("seconds").style(f'color: {colors["text_dark"]}; font-size: 0.9rem;')

                # Start button
                ui.button("🎬 START THE SHOW", on_click=start_game_from_welcome).classes(
                    'bollywood-btn btn-magenta'
                ).style('font-size: clamp(0.8rem, 2.5vw, 1rem); padding: 10px 28px; margin-top: 6px;')

                # Timer info
                duration = game.timer_duration if game.team_mode else GAME_DURATION_SEC
                timer_label = ui.label(f"⏱️ {duration} seconds per round").style(
                    f'color: {colors["accent_dark"]}; font-size: clamp(0.75rem, 2.5vw, 0.9rem); margin-top: 8px;'
                )

    # ---------- GAME SCREEN ----------
    def build_game_screen():
        """Build the main game screen."""
        nonlocal timer_display, timer_container_el, image_container, hint_container, answer_container, progress_container, next_btn
        nonlocal scoreboard_container, scoring_buttons_container, countdown_overlay

        main_container.clear()

        with main_container:
            # Film strip top border
            ui.element('div').classes('film-strip-border w-full')

            with ui.column().classes('w-full p-1 sm:p-2 md:p-4 gap-1 md:gap-2'):
                # ---------- HEADER ROW ----------
                with ui.row().classes('w-full justify-between items-center gap-2').style('flex-wrap: nowrap;'):
                    # Left side: Title and progress
                    with ui.column().classes('gap-0'):
                        ui.label("🎬 GUESS THE MOVIE").classes('main-title').style(
                            'font-family: "Rozha One", serif; font-size: clamp(1rem, 4vw, 1.5rem); '
                            'letter-spacing: 1px; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.3));'
                        )
                        # Progress indicator
                        progress_container = ui.element('div').classes('mt-1')

                    # Timer - compact circular design (clickable to pause, one-way action)
                    timer_clickable = not game.is_reviewing() and not game.show_answer and not game.game_over and not game.timer_paused
                    timer_classes = 'timer-container' + (' timer-clickable' if timer_clickable else '')
                    timer_container_el = ui.element('div').classes(timer_classes).style('width: 50px; height: 50px;')
                    if timer_clickable:
                        timer_container_el.on('click', on_timer_click)
                    with timer_container_el:
                        with ui.element('div').classes('timer-inner').style('width: 100%; height: 100%;'):
                            timer_display = ui.label(f"{game.time_left // 60}:{game.time_left % 60:02d}").classes('timer-text').style('font-size: 1.1rem;')

                # ---------- REVIEW MODE INDICATOR (Feature 1) ----------
                if game.is_reviewing():
                    with ui.row().classes('w-full justify-center items-center gap-3'):
                        ui.label("📖 Reviewing Previous").classes('review-badge')
                        ui.button("← Back to Game", on_click=exit_review_mode).classes('back-btn')

                # ---------- TEAM TURN INDICATOR (Team mode only, not in review mode) - styled badge ----------
                elif game.team_mode:
                    team_color = "#E91E63" if game.current_team == 0 else "#2196F3"
                    team_gradient = "linear-gradient(135deg, #E91E63, #C2185B)" if game.current_team == 0 else "linear-gradient(135deg, #2196F3, #1565C0)"
                    team_emoji = "🔴" if game.current_team == 0 else "🔵"
                    with ui.row().classes('w-full justify-center'):
                        ui.label(f"✨ {game.get_current_team_name()}'s Turn ✨").style(
                            f'color: white; font-size: clamp(0.8rem, 3vw, 1rem); font-weight: 700; '
                            f'padding: 6px 16px; background: {team_gradient}; border-radius: 25px; '
                            f'box-shadow: 0 3px 10px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.2); '
                            f'border: 1px solid rgba(255,255,255,0.3); text-shadow: 0 1px 2px rgba(0,0,0,0.3);'
                        )

                # ---------- IMAGE AREA (with relative positioning for countdown overlay) ----------
                image_container = ui.element('div').classes(
                    'w-full flex justify-center items-center py-1 sm:py-2 image-area-container'
                ).style('min-height: 150px; position: relative;')

                # ---------- CONTROL BUTTONS (different in review mode) ----------
                if game.is_reviewing():
                    with ui.row().classes('w-full justify-center gap-1 md:gap-3 flex-wrap'):
                        ui.button("💡 HINT", on_click=show_review_hint).classes('bollywood-btn btn-gold')
                        ui.button("🎬 REVEAL", on_click=show_review_answer).classes('bollywood-btn btn-magenta')
                else:
                    with ui.row().classes('w-full justify-center gap-1 md:gap-3 flex-wrap'):
                        ui.button("💡 HINT", on_click=show_hint_click).classes('bollywood-btn btn-gold')
                        ui.button("🎬 REVEAL", on_click=reveal_answer_click).classes('bollywood-btn btn-magenta')
                        next_btn = ui.button("▶ NEXT", on_click=next_movie_click).classes('bollywood-btn btn-turquoise')

                # ---------- SCORING BUTTONS (Team mode, shown after reveal, not in review mode) ----------
                if game.team_mode and not game.is_reviewing():
                    scoring_buttons_container = ui.row().classes('w-full justify-center items-center gap-3')
                    scoring_buttons_container.style('display: none;')  # Hidden initially

                # ---------- HINT/ANSWER AREAS ----------
                hint_container = ui.element('div').classes('w-full')
                answer_container = ui.element('div').classes('w-full')

                # ---------- TEAM SCOREBOARD (Team mode only) ----------
                if game.team_mode:
                    scoreboard_container = ui.element('div').classes('w-full mt-1')
                    with scoreboard_container:
                        # Compact single-line scoreboard
                        with ui.row().classes('w-full justify-center items-center gap-2').style('flex-wrap: nowrap;'):
                            # Team A score - compact inline
                            team_a_active = game.current_team == 0
                            with ui.row().classes('items-center gap-1').style(
                                f'background: {"rgba(233,30,99,0.2)" if team_a_active else "rgba(0,0,0,0.05)"}; '
                                f'padding: 4px 8px; border-radius: 6px; '
                                f'border: 2px solid {"#E91E63" if team_a_active else "transparent"};'
                            ):
                                ui.label(f"🔴 {game.team_names[0]}").style(
                                    'color: #E91E63; font-weight: 700; font-size: clamp(0.7rem, 2.5vw, 0.85rem); white-space: nowrap;'
                                )
                                ui.label(f"{game.team_scores[0]}").style(
                                    'color: #1A0A14; font-size: clamp(0.9rem, 3vw, 1.1rem); font-weight: 700;'
                                )

                            # VS divider
                            ui.label("vs").style('color: #888; font-weight: 700; font-size: 0.8rem;')

                            # Team B score - compact inline
                            team_b_active = game.current_team == 1
                            with ui.row().classes('items-center gap-1').style(
                                f'background: {"rgba(33,150,243,0.2)" if team_b_active else "rgba(0,0,0,0.05)"}; '
                                f'padding: 4px 8px; border-radius: 6px; '
                                f'border: 2px solid {"#2196F3" if team_b_active else "transparent"};'
                            ):
                                ui.label(f"🔵 {game.team_names[1]}").style(
                                    'color: #2196F3; font-weight: 700; font-size: clamp(0.7rem, 2.5vw, 0.85rem); white-space: nowrap;'
                                )
                                ui.label(f"{game.team_scores[1]}").style(
                                    'color: #1A0A14; font-size: clamp(0.9rem, 3vw, 1.1rem); font-weight: 700;'
                                )

            # Film strip bottom border
            ui.element('div').classes('film-strip-border w-full').style('border-radius: 0 0 12px 12px;')

        # Initialize content
        refresh_game_content()

    # ==========================================================================
    # BUILD THE PAGE
    # ==========================================================================

    # Add head HTML (styles, fonts, scripts) with theme colors
    ui.add_head_html(generate_theme_css(game.get_theme_colors()))

    # Set body background with theme colors
    ui.query('body').style(generate_body_bg(game.get_theme_colors()))

    # Main layout container
    with ui.column().classes('w-full max-w-4xl mx-auto p-1 sm:p-4 md:p-8'):
        # Game card container
        main_container = ui.element('div').classes('game-card w-full')

    # Start with welcome screen
    build_welcome_screen()

    # Start timer
    ui.timer(1.0, update_timer)


# =============================================================================
# APP ENTRY POINT
# =============================================================================
@ui.page('/')
def main_page():
    """Main page route."""
    create_game_ui()


if __name__ in {"__main__", "__mp_main__"}:
    # Port/host configurable via environment (for Render deployment)
    # Locally: defaults to localhost:8080
    # Render: sets PORT env var, requires 0.0.0.0
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 8080))

    ui.run(
        title="🎬 Bollywood Frames",
        host=host,
        port=port,
        reload=False,
        favicon="🎬"
    )
