"""
🎬 BOLLYWOOD FRAMES - Movie Guessing Game
==========================================
A Bollywood-themed game app with premium, cinematic UI design.

DESIGN PHILOSOPHY:
- Inspired by Filmfare Awards, movie premieres, and Indian wedding aesthetics
- Color palette: Gold, Magenta, Turquoise, Deep Maroon
- Typography: Rozha One (dramatic headlines) + Poppins (modern body)
- Elements: Film reels, spotlights, star motifs, gold accents
- Feel: Premium, celebratory, culturally authentic

DESIGN REFERENCES:
- Modern Bollywood posters (Gully Boy, Padmaavat, Rocky Aur Rani)
- Zee Cine Awards / Filmfare Awards visual identity
- Traditional Indian festival colors and patterns
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
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, 'images')
CSV_FILE = os.path.join(SCRIPT_DIR, 'data.csv')
APP_TITLE = "Bollywood Frames"
DEFAULT_DURATION_SEC = 60

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

# =============================================================================
# DESIGN SYSTEM - Bollywood-Inspired Theme
# =============================================================================
"""
COLOR PALETTE:
- Inspired by Filmfare Awards, Bollywood posters, and Indian festivals
- Gold represents awards, luxury, and Bollywood glamour
- Magenta/Pink is the quintessential Bollywood celebration color
- Deep maroon creates a cinematic, theater-like atmosphere
- Turquoise adds a modern Indian design touch (peacock inspired)
"""

COLORS = {
    # Primary colors
    'gold': '#D4AF37',           # Bollywood gold - awards, luxury
    'gold_light': '#F4D03F',     # Lighter gold for highlights
    'gold_dark': '#B8860B',      # Darker gold for depth

    # Secondary colors
    'magenta': '#E91E63',        # Rani pink - celebration, drama
    'magenta_dark': '#880E4F',   # Deep magenta for gradients
    'turquoise': '#00BFA5',      # Peacock blue - modern Indian

    # Background colors (Cinema hall inspired)
    'bg_dark': '#0D0208',        # Near black - cinema darkness
    'bg_maroon': '#1A0A14',      # Deep maroon - velvet curtains
    'bg_purple': '#150520',      # Deep purple - luxury

    # Accent colors
    'red': '#C41E3A',            # Sindoor red - traditional
    'orange': '#FF6B35',         # Festival orange
    'cream': '#FFF8E7',          # Ivory - elegant text

    # UI colors
    'card_bg': 'rgba(255, 248, 231, 0.95)',  # Cream with transparency
    'text_dark': '#1A0A14',
    'text_light': '#FFF8E7',
}

# =============================================================================
# STYLES - Reusable CSS Components
# =============================================================================
"""
COMPONENT LIBRARY:
- Buttons with Bollywood gradients and gold borders
- Cards with spotlight effects
- Typography with cinematic flair
- Animations for dramatic reveals and celebrations
"""

STYLES = {
    # Global animations and fonts
    'head_html': '''
    <!-- Google Fonts: Rozha One for dramatic headlines, Poppins for modern body -->
    <link href="https://fonts.googleapis.com/css2?family=Rozha+One&family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet">

    <style>
        /* ===== BASE STYLES ===== */
        * {
            font-family: 'Poppins', sans-serif;
        }

        /* ===== BOLLYWOOD HEADLINE FONT ===== */
        /* Rozha One has a dramatic, cinematic quality perfect for Bollywood */
        .bollywood-title {
            font-family: 'Rozha One', serif !important;
            letter-spacing: 2px;
        }

        /* ===== ANIMATIONS ===== */

        /* Gold shimmer effect - like stage lights catching gold jewelry */
        @keyframes goldShimmer {
            0% { background-position: -200% center; }
            100% { background-position: 200% center; }
        }

        /* Spotlight pulse - simulates theater spotlight */
        @keyframes spotlightPulse {
            0%, 100% { opacity: 0.8; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.02); }
        }

        /* Star twinkle - for celebration moments */
        @keyframes twinkle {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.8); }
        }

        /* Curtain reveal - dramatic entrance */
        @keyframes curtainReveal {
            0% { transform: scaleY(0); opacity: 0; }
            100% { transform: scaleY(1); opacity: 1; }
        }

        /* Float up - for celebration elements */
        @keyframes floatUp {
            0% { transform: translateY(100px); opacity: 0; }
            100% { transform: translateY(0); opacity: 1; }
        }

        /* Glow pulse - for important elements */
        @keyframes glowPulse {
            0%, 100% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); }
            50% { box-shadow: 0 0 40px rgba(212, 175, 55, 0.8), 0 0 60px rgba(233, 30, 99, 0.4); }
        }

        /* Film reel rotation */
        @keyframes reelSpin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Countdown pulse - urgent */
        @keyframes countdownPulse {
            0%, 100% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(1.1); }
        }

        /* Confetti fall */
        @keyframes confettiFall {
            0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
        }

        /* ===== COMPONENT STYLES ===== */

        /* Main title with gold gradient */
        .main-title {
            font-family: 'Rozha One', serif !important;
            font-size: 3.5rem;
            background: linear-gradient(
                90deg,
                #D4AF37 0%,
                #F4D03F 25%,
                #D4AF37 50%,
                #F4D03F 75%,
                #D4AF37 100%
            );
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: goldShimmer 3s linear infinite;
            text-shadow: none;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }

        /* Subtitle styling */
        .subtitle {
            font-family: 'Poppins', sans-serif;
            color: #FFF8E7;
            font-size: 1.1rem;
            letter-spacing: 4px;
            text-transform: uppercase;
            opacity: 0.9;
        }

        /* Game card with spotlight effect */
        .game-card {
            background: linear-gradient(145deg, rgba(255,248,231,0.98), rgba(255,248,231,0.92));
            border-radius: 24px;
            box-shadow:
                0 25px 50px rgba(0,0,0,0.4),
                0 0 100px rgba(212,175,55,0.2),
                inset 0 1px 0 rgba(255,255,255,0.8);
            animation: spotlightPulse 4s ease-in-out infinite;
            border: 2px solid rgba(212,175,55,0.3);
        }

        /* Film strip decoration - top border */
        .film-strip-border {
            background: repeating-linear-gradient(
                90deg,
                #1A0A14 0px,
                #1A0A14 10px,
                #D4AF37 10px,
                #D4AF37 12px,
                #1A0A14 12px,
                #1A0A14 22px
            );
            height: 12px;
            border-radius: 12px 12px 0 0;
        }

        /* Bollywood button base - compact size */
        .bollywood-btn {
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 0.75rem;
            padding: 8px 18px;
            border-radius: 25px;
            border: 1.5px solid #D4AF37;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow:
                0 2px 8px rgba(0,0,0,0.2),
                inset 0 1px 0 rgba(255,255,255,0.3);
            /* iOS touch fixes */
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
            user-select: none;
        }

        .bollywood-btn:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow:
                0 8px 25px rgba(0,0,0,0.4),
                0 0 20px rgba(212,175,55,0.4);
        }

        .bollywood-btn:active {
            transform: translateY(0) scale(0.98);
        }

        /* iOS needs explicit active state trigger */
        @media (pointer: coarse) {
            .bollywood-btn:active {
                transform: scale(0.95);
            }
        }

        /* Button variants */
        .btn-gold {
            background: linear-gradient(145deg, #F4D03F, #D4AF37, #B8860B);
            color: #1A0A14;
        }

        .btn-magenta {
            background: linear-gradient(145deg, #E91E63, #C2185B, #880E4F);
            color: white;
        }

        .btn-turquoise {
            background: linear-gradient(145deg, #00BFA5, #00897B, #00695C);
            color: white;
        }

        /* Image frame - like a movie poster */
        .movie-frame {
            position: relative;
            border-radius: 16px;
            overflow: hidden;
            box-shadow:
                0 10px 40px rgba(0,0,0,0.4),
                0 0 0 4px #D4AF37,
                0 0 0 8px #1A0A14,
                0 0 60px rgba(212,175,55,0.2);
        }

        /* Timer styling - Filmfare award trophy inspired */
        .timer-container {
            background: linear-gradient(145deg, #D4AF37, #B8860B);
            border-radius: 50%;
            padding: 4px;
            box-shadow:
                0 4px 20px rgba(212,175,55,0.5),
                inset 0 2px 4px rgba(255,255,255,0.3);
        }

        .timer-inner {
            background: linear-gradient(145deg, #1A0A14, #2D1B28);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .timer-text {
            font-family: 'Poppins', sans-serif;
            font-weight: 800;
            color: #D4AF37;
            font-size: 1.5rem;
        }

        /* Hint box */
        .hint-box {
            background: linear-gradient(145deg, #FFF8E7, #F4D03F20);
            border: 2px solid #D4AF37;
            border-radius: 12px;
            padding: 16px 24px;
            animation: floatUp 0.5s ease-out;
        }

        /* Answer reveal */
        .answer-box {
            background: linear-gradient(145deg, #00BFA520, #00695C20);
            border: 2px solid #00BFA5;
            border-radius: 12px;
            padding: 16px 24px;
            animation: floatUp 0.5s ease-out;
        }

        /* Countdown overlay - positioned over image */
        .countdown-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Rozha One', serif;
            font-size: 8rem;
            font-weight: 400;
            color: #E91E63;
            text-shadow:
                0 0 40px rgba(233,30,99,0.8),
                0 0 80px rgba(233,30,99,0.4),
                0 4px 0 #880E4F;
            z-index: 100;
            pointer-events: none;
            animation: countdownPulse 1s ease-in-out infinite;
        }

        /* Image area container for relative positioning */
        .image-area-container {
            position: relative;
        }

        /* Star decoration */
        .star {
            color: #D4AF37;
            animation: twinkle 1.5s ease-in-out infinite;
        }

        /* Welcome screen curtain */
        .curtain-left, .curtain-right {
            position: fixed;
            top: 0;
            width: 50%;
            height: 100%;
            background: linear-gradient(180deg, #8B0000, #4A0000);
            z-index: 2000;
            transition: transform 1.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .curtain-left { left: 0; transform-origin: left; }
        .curtain-right { right: 0; transform-origin: right; }

        .curtains-open .curtain-left { transform: translateX(-100%); }
        .curtains-open .curtain-right { transform: translateX(100%); }

        /* Progress indicator */
        .progress-dots {
            display: flex;
            gap: 8px;
            justify-content: center;
        }

        .progress-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: rgba(212,175,55,0.3);
            transition: all 0.3s ease;
        }

        .progress-dot.completed {
            background: #D4AF37;
            box-shadow: 0 0 10px rgba(212,175,55,0.5);
        }

        .progress-dot.current {
            background: #E91E63;
            box-shadow: 0 0 15px rgba(233,30,99,0.6);
            animation: glowPulse 2s infinite;
        }

        /* Celebration confetti */
        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            z-index: 1001;
            animation: confettiFall 3s linear forwards;
        }

        /* Game over celebration */
        .celebration-container {
            animation: floatUp 0.8s ease-out;
        }

        .trophy-icon {
            font-size: 6rem;
            animation: glowPulse 2s infinite;
        }

        /* ===== MOBILE RESPONSIVE STYLES ===== */
        @media (max-width: 640px) {
            /* Smaller countdown overlay on mobile */
            .countdown-overlay {
                font-size: 4rem !important;
            }

            /* Smaller title */
            .main-title {
                font-size: 2rem;
            }

            /* Disable animation on mobile to fix iOS touch issues */
            .game-card {
                animation: none;
            }

            /* Compact buttons on mobile - icons + minimal text */
            .bollywood-btn {
                padding: 6px 10px;
                font-size: 0.7rem;
                border-radius: 20px;
                border-width: 1px;
                letter-spacing: 0;
            }

            /* Smaller timer */
            .timer-container {
                width: 50px !important;
                height: 50px !important;
            }

            .timer-text {
                font-size: 0.95rem;
            }

            /* Smaller trophy on game over */
            .trophy-icon {
                font-size: 4rem;
            }

            /* Reduce padding in game card */
            .game-card {
                border-radius: 16px;
            }

            /* Smaller image frame */
            .movie-frame {
                box-shadow:
                    0 5px 20px rgba(0,0,0,0.4),
                    0 0 0 2px #D4AF37,
                    0 0 0 4px #1A0A14;
            }

            /* Progress dots smaller */
            .progress-dot {
                width: 8px;
                height: 8px;
            }

            /* Hint/Answer boxes compact */
            .hint-box, .answer-box {
                padding: 4px 8px;
                border-radius: 6px;
            }

            /* Constrain image height on mobile */
            .game-image {
                max-height: 35vh !important;
            }
        }

        /* Mobile floating icon buttons */
        .mobile-icon-btn {
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .mobile-icon-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }

        .mobile-icon-btn:active {
            transform: scale(0.95);
        }
    </style>

    <script>
        // Audio context for sound effects
        let audioCtx = null;

        // Countdown beep - gets more urgent as time runs out
        function playTick(timeLeft) {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();

            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();

            // Higher pitch as time runs out (880Hz at 10s -> 1320Hz at 1s)
            const freq = 880 + (10 - timeLeft) * 44;
            osc.type = 'sine';
            osc.frequency.value = freq;

            // Shorter duration as time runs out
            const duration = 0.08 + (timeLeft / 10) * 0.12;

            gain.gain.setValueAtTime(0, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.01);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime + duration - 0.02);
            gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + duration);

            osc.connect(gain);
            gain.connect(audioCtx.destination);

            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }

        // Victory fanfare
        function playVictory() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();

            const notes = [523, 659, 784, 1047]; // C5, E5, G5, C6 - triumphant chord
            const now = audioCtx.currentTime;

            notes.forEach((freq, i) => {
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
            });
        }

        // Create confetti burst
        function createConfetti() {
            const colors = ['#D4AF37', '#E91E63', '#00BFA5', '#F4D03F', '#FF6B35'];

            for (let i = 0; i < 50; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 2 + 's';
                confetti.style.animationDuration = (2 + Math.random() * 2) + 's';
                document.body.appendChild(confetti);

                setTimeout(() => confetti.remove(), 5000);
            }
        }
    </script>
    ''',

    # Background gradient - cinema hall inspired
    'body_bg': '''
        background:
            radial-gradient(ellipse at top, rgba(212,175,55,0.1) 0%, transparent 50%),
            radial-gradient(ellipse at bottom, rgba(233,30,99,0.1) 0%, transparent 50%),
            linear-gradient(180deg, #0D0208 0%, #1A0A14 50%, #150520 100%);
        min-height: 100vh;
    ''',
}

# =============================================================================
# DATA LOADING
# =============================================================================
def load_data():
    """Loads the CSV and ensures we only use rows where images exist."""
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame()
    df = pd.read_csv(CSV_FILE)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def get_valid_game_data(df):
    """Filters the dataframe to include only images that actually exist."""
    if df.empty:
        return []
    valid_rounds = []
    for _, row in df.iterrows():
        image_path = os.path.join(IMAGE_FOLDER, row['filename'])
        if os.path.exists(image_path):
            valid_rounds.append(row.to_dict())
    return valid_rounds


# =============================================================================
# TEAM NAME PAIRS (Bollywood themed)
# =============================================================================
TEAM_NAME_PAIRS = [
    ("Shahenshah", "Mogambo"),
    ("Dilwale", "Dulhania"),
    ("Munna", "Circuit"),
    ("Jai", "Veeru"),
    ("Rahul", "Anjali"),
    ("Chulbul", "Pandey"),
    ("Gabbar", "Thakur"),
    ("Don", "Jaani"),
]

# Winning/losing phrases for teams
WINNER_PHRASES = [
    "Picture abhi baaki hai mere dost... oh wait, you won!",
    "Rishte mein toh hum tumhare baap lagte hain... CHAMPIONS!",
    "Vijay Dinanath Chauhan... WINNER!",
]

LOSER_PHRASES = [
    "Mogambo khush nahi hua!",
    "Kabhi kabhi jeetne ke liye kuch haarna padta hai",
    "Haar kar jeetne wale ko baazigar kehte hain... but not today!",
]


# =============================================================================
# GAME STATE
# =============================================================================
class GameState:
    """Manages the game logic and state."""

    def __init__(self):
        self.df = load_data()
        self.valid_movies = get_valid_game_data(self.df)
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
        self.team_names = list(random.choice(TEAM_NAME_PAIRS))  # ["Team A", "Team B"]
        self.team_scores = [0, 0]  # [Team A score, Team B score]
        self.current_team = 0  # 0 = Team A, 1 = Team B
        self.hint_used = False  # Track if hint was used this round
        self.awaiting_score = False  # Waiting for coordinator to mark correct/wrong

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
        """Pick a new random pair of team names."""
        self.team_names = list(random.choice(TEAM_NAME_PAIRS))

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

        if time_ratio > 0.66:  # First third of time
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


# =============================================================================
# MAIN UI
# =============================================================================
def create_game_ui():
    """Creates the main game interface with Bollywood theming."""

    game = GameState()

    # UI element references
    main_container = None
    timer_display = None
    countdown_overlay = None
    image_container = None
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
                        dot_class += ' completed'
                    elif i == game.shown_count() - 1:
                        dot_class += ' current'
                    ui.element('div').classes(dot_class)

        if game.game_over:
            show_game_over()
            return

        if game.current_movie:
            # Update image and countdown overlay
            nonlocal countdown_overlay
            image_container.clear()
            with image_container:
                # Image with onload handler to start timer
                img_path = os.path.join(IMAGE_FOLDER, game.current_movie['filename'])
                img = ui.image(img_path).classes('max-w-full rounded-lg game-image').style(
                    'max-height: min(45vh, 350px); object-fit: contain;'
                )
                # Start timer when image loads
                img.on('load', lambda: start_timer_after_load())
                # Re-create countdown overlay inside image container
                countdown_overlay = ui.label("").classes('countdown-overlay').style('display: none;')

            # Update hint - more compact
            hint_container.clear()
            if game.show_hint:
                with hint_container:
                    with ui.element('div').classes('hint-box').style('padding: 6px 12px; margin-top: 4px;'):
                        ui.label(f"💡 {game.get_hint_text()}").style(
                            'color: #1A0A14; font-size: clamp(0.8rem, 2.5vw, 1rem);'
                        )

            # Update answer - more compact
            answer_container.clear()
            if game.show_answer:
                with answer_container:
                    with ui.element('div').classes('answer-box').style('padding: 6px 12px; margin-top: 4px;'):
                        ui.label(f"🎬 {game.current_movie['movie_name']}").classes('movie-answer-text').style(
                            'color: #1A0A14; font-size: clamp(0.9rem, 3.5vw, 1.5rem); font-weight: 700; '
                            'font-family: "Rozha One", serif;'
                        )

            # Update next button
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

                        # Bollywood phrase
                        phrase = random.choice(WINNER_PHRASES)
                        ui.label(f'"{phrase}"').style(
                            'color: #1A0A14; font-size: clamp(0.8rem, 3vw, 1rem); font-style: italic; '
                            'opacity: 0.8; text-align: center; max-width: 300px;'
                        )

                    # Final scores
                    ui.label("✦ ✦ ✦").style('color: #D4AF37; font-size: 1rem; letter-spacing: 12px; margin: 8px 0;')

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
                        loser_phrase = random.choice(LOSER_PHRASES)
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
        if not game.timer_active and not game.show_answer and not game.game_over:
            game.timer_active = True

    # ---------- BUTTON HANDLERS ----------
    def show_hint_click():
        game.show_hint = True
        game.hint_used = True  # Track for scoring penalty
        refresh_game_content()

    def reveal_answer_click():
        game.show_answer = True
        game.timer_active = False
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
        """Build the dramatic welcome/splash screen."""
        main_container.clear()

        # Container for team options (to show/hide)
        team_options_container = None
        team_names_label = None
        timer_label = None

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

        with main_container:
            with ui.column().classes('w-full items-center justify-center gap-2 md:gap-4 py-4 md:py-6'):
                # Film reel decoration
                ui.label("🎞️").style('font-size: clamp(2rem, 6vw, 3rem); animation: reelSpin 4s linear infinite;')

                # Main title
                ui.label("BOLLYWOOD").classes('main-title').style('font-size: clamp(1.8rem, 8vw, 3rem); margin-bottom: -8px;')
                ui.label("FRAMES").classes('main-title').style('font-size: clamp(1.8rem, 8vw, 3rem);')

                # Subtitle - dark color for visibility on cream background
                ui.label("THE ULTIMATE MOVIE GUESSING GAME").style(
                    'color: #1A0A14; font-size: clamp(0.6rem, 2.5vw, 0.95rem); letter-spacing: 2px; '
                    'text-transform: uppercase; opacity: 0.7; margin-top: 4px;'
                )

                # Decorative elements
                ui.label("✦ ✦ ✦").style('color: #D4AF37; font-size: 1rem; letter-spacing: 12px; margin: 8px 0;')

                # Movie count info - dark color
                movie_count = len(get_valid_game_data(load_data()))
                ui.label(f"🎬 {movie_count} Movies to Guess").style(
                    'color: #1A0A14; font-size: clamp(0.9rem, 3vw, 1.1rem); font-weight: 600;'
                )

                # ---------- GAME MODE TOGGLE ----------
                with ui.row().classes('items-center gap-4 mt-4'):
                    ui.label("Game Mode:").style('color: #1A0A14; font-weight: 600;')
                    ui.switch("Team Battle", value=game.team_mode, on_change=toggle_team_mode).style(
                        'color: #880E4F;'
                    )

                # ---------- TEAM OPTIONS (shown when team mode enabled) ----------
                team_options_container = ui.column().classes('items-center gap-3 mt-2 w-full')
                team_options_container.style(f"display: {'flex' if game.team_mode else 'none'};")

                with team_options_container:
                    # Team names display - centered with dice on right
                    with ui.element('div').style(
                        'display: flex; justify-content: center; width: 100%; position: relative;'
                    ):
                        # Centered team names (no wrap)
                        team_names_label = ui.label(f"🔴 {game.team_names[0]}  vs  🔵 {game.team_names[1]}").style(
                            'color: #1A0A14; font-size: clamp(0.85rem, 3.5vw, 1.3rem); font-weight: 700; '
                            'background: rgba(212,175,55,0.2); padding: 8px 16px; border-radius: 8px; '
                            'text-align: center; white-space: nowrap;'
                        )
                        # Dice icon positioned to the right of the label
                        ui.button("🎲", on_click=randomize_names).style(
                            'background: transparent; border: none; font-size: 1.3rem; cursor: pointer; '
                            'padding: 2px; min-width: auto; box-shadow: none; margin-left: 4px;'
                        ).props('flat dense').tooltip('Randomize team names')

                    # Timer configuration
                    with ui.row().classes('items-center justify-center gap-2'):
                        ui.label("⏱️ Timer:").style('color: #1A0A14; font-size: 0.9rem;')
                        ui.number(value=game.timer_duration, min=15, max=120, step=5,
                                  on_change=update_timer_duration).style(
                            'width: 70px;'
                        ).props('dense outlined')
                        ui.label("seconds").style('color: #1A0A14; font-size: 0.9rem;')

                # Start button
                ui.button("🎬 START THE SHOW", on_click=start_game_from_welcome).classes(
                    'bollywood-btn btn-magenta'
                ).style('font-size: clamp(0.8rem, 2.5vw, 1rem); padding: 12px 32px; margin-top: 12px;')

                # Timer info - dark color
                duration = game.timer_duration if game.team_mode else GAME_DURATION_SEC
                timer_label = ui.label(f"⏱️ {duration} seconds per round").style(
                    'color: #880E4F; font-size: clamp(0.75rem, 2.5vw, 0.9rem); margin-top: 8px;'
                )

    # ---------- GAME SCREEN ----------
    def build_game_screen():
        """Build the main game screen."""
        nonlocal timer_display, image_container, hint_container, answer_container, progress_container, next_btn
        nonlocal scoreboard_container, scoring_buttons_container, countdown_overlay

        main_container.clear()

        with main_container:
            # Film strip top border
            ui.element('div').classes('film-strip-border w-full')

            with ui.column().classes('w-full p-2 md:p-4 gap-1 md:gap-2'):
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

                    # Timer - compact circular design
                    with ui.element('div').classes('timer-container').style('width: 50px; height: 50px;'):
                        with ui.element('div').classes('timer-inner').style('width: 100%; height: 100%;'):
                            timer_display = ui.label(f"{game.time_left // 60}:{game.time_left % 60:02d}").classes('timer-text').style('font-size: 1.1rem;')

                # ---------- TEAM TURN INDICATOR (Team mode only) - styled badge ----------
                if game.team_mode:
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

                # ---------- CONTROL BUTTONS ----------
                with ui.row().classes('w-full justify-center gap-1 md:gap-3 flex-wrap'):
                    ui.button("💡 HINT", on_click=show_hint_click).classes('bollywood-btn btn-gold')
                    ui.button("🎬 REVEAL", on_click=reveal_answer_click).classes('bollywood-btn btn-magenta')
                    next_btn = ui.button("▶ NEXT", on_click=next_movie_click).classes('bollywood-btn btn-turquoise')

                # ---------- SCORING BUTTONS (Team mode, shown after reveal) ----------
                if game.team_mode:
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

    # Add head HTML (styles, fonts, scripts)
    ui.add_head_html(STYLES['head_html'])

    # Set body background
    ui.query('body').style(STYLES['body_bg'])

    # Main layout container
    with ui.column().classes('w-full max-w-4xl mx-auto p-4 md:p-8'):
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
