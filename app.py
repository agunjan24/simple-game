import streamlit as st
import os
import pandas as pd
import random
import time
import uuid

# --- CONFIGURATION ---
IMAGE_FOLDER = 'images'
CSV_FILE = 'data.csv'
APP_TITLE = "🎬 Bollywood Frames"
GAME_DURATION_SEC = 60

# --- SETUP PAGE ---
st.set_page_config(page_title="Bollywood Guess", page_icon="🎥")
st.title(APP_TITLE)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    """Loads the CSV and ensures we only use rows where images exist."""
    if not os.path.exists(CSV_FILE):
        st.error(f"❌ Missing file: {CSV_FILE}. Please upload your spreadsheet!")
        return pd.DataFrame()
    
    df = pd.read_csv(CSV_FILE)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def get_valid_game_data(df):
    """Filters the dataframe to include only images that actually exist in the folder."""
    if df.empty:
        return []
    valid_rounds = []
    for index, row in df.iterrows():
        image_path = os.path.join(IMAGE_FOLDER, row['filename'])
        if os.path.exists(image_path):
            valid_rounds.append(row.to_dict())
    return valid_rounds

def next_movie():
    """Picks a random row from the valid data, excluding previously shown ones."""
    df = load_data()
    valid_data = get_valid_game_data(df)
    
    shown_list = st.session_state.get('shown_movies', [])
    available_movies = [m for m in valid_data if m['filename'] not in shown_list]
    
    if available_movies:
        choice = random.choice(available_movies)
        st.session_state.current_round = choice
        st.session_state.shown_movies.append(choice['filename'])
        
        # Reset UI flags
        st.session_state.show_answer = False
        st.session_state.show_hint = False
        st.session_state.game_over = False
        
        # --- NEW: Reset Timer ---
        st.session_state.start_time = time.time()
    else:
        st.session_state.game_over = True
        st.session_state.current_round = None

# --- CUSTOM TIMER INJECTION ---
def inject_timer():
    """
    Injects HTML/JS for the clock and countdown overlay.
    Uses unique IDs to ensure reliable updates on Streamlit reruns.
    """
    
    # 1. Calculate remaining time
    if 'start_time' in st.session_state:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, GAME_DURATION_SEC - int(elapsed))
    else:
        remaining = 0

    # 2. Generate unique IDs for this specific render
    # This prevents the "old" timer (from before you clicked a button) 
    # from interfering with the "new" timer.
    unique_id = str(uuid.uuid4())[:8]
    hand_id = f"sec-hand-{unique_id}"
    overlay_id = f"overlay-text-{unique_id}"

    # 3. HTML/CSS/JS Block
    timer_html = f"""
    <style>
        /* TOP RIGHT CLOCK STYLES */
        .clock-container-{unique_id} {{
            position: fixed;
            top: 60px;
            right: 20px;
            z-index: 99999;
            background: white;
            border: 3px solid #333;
            border-radius: 50%;
            width: 80px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}
        .clock-face-{unique_id} {{
            position: relative;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: #f0f0f0;
        }}
        /* The Hand */
        #{hand_id} {{
            position: absolute;
            bottom: 50%;
            left: 50%;
            width: 3px;
            height: 35px;
            background: red;
            transform-origin: bottom center;
            /* Smooth transition for the ticking effect */
            transition: transform 0.2s cubic-bezier(0.4, 2.3, 0.3, 1);
        }}
        /* Center Pin */
        .clock-face-{unique_id}::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 8px;
            height: 8px;
            background: #333;
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }}

        /* CENTER OVERLAY STYLES */
        #{overlay_id} {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 10rem;
            font-weight: 900;
            color: rgba(255, 0, 0, 0.8);
            text-shadow: 0px 0px 20px white; /* Halo for readability */
            z-index: 100000;
            display: none;
            pointer-events: none;
            font-family: sans-serif;
        }}
    </style>

    <div class="clock-container-{unique_id}">
        <div class="clock-face-{unique_id}">
            <div id="{hand_id}"></div>
        </div>
    </div>
    <div id="{overlay_id}"></div>

    <script>
    (function() {{
        let timeLeft = {remaining};
        const hand = document.getElementById('{hand_id}');
        const overlay = document.getElementById('{overlay_id}');
        
        function updateTimer() {{
            // SAFETY CHECK: If the element is gone (page refresh), stop the timer.
            if (!hand) {{ 
                return; 
            }}
            
            // LOGIC
            if (timeLeft > 0) {{
                // Calculate angle: 60 seconds = 360 degrees, so 6 deg per second
                // We invert it so it ticks clockwise from 12 o'clock
                // (60 - timeLeft) * 6
                let secondsElapsed = 60 - timeLeft;
                let deg = secondsElapsed * 6;
                hand.style.transform = `rotate(${{deg}}deg)`;

                // Countdown Overlay (Last 10 seconds)
                if (timeLeft <= 10) {{
                    overlay.style.display = 'block';
                    overlay.innerText = timeLeft;
                }} else {{
                    overlay.style.display = 'none';
                }}
                
                timeLeft--;
                
            }} else {{
                // TIME IS UP
                hand.style.transform = `rotate(360deg)`;
                overlay.style.display = 'block';
                overlay.innerText = "TIME UP";
                overlay.style.fontSize = "5rem";
            }}
        }}

        // Start immediately
        updateTimer();
        
        // Update every second
        const intervalId = setInterval(updateTimer, 1000);
        
        // Cleanup function if the script runs again
        // (This helps prevent ghost timers in some browsers)
        window.addEventListener('beforeunload', () => clearInterval(intervalId));
    }})();
    </script>
    """
    
    st.markdown(timer_html, unsafe_allow_html=True)
    
# --- INITIALIZATION ---
if 'shown_movies' not in st.session_state:
    st.session_state.shown_movies = []

if 'current_round' not in st.session_state:
    next_movie()

# --- GAME UI ---

# Check if the game is over
if st.session_state.get('game_over', False):
    st.success("🎉 You have gone through all the movies in the list!")
    if st.button("🔄 Start Over"):
        st.session_state.shown_movies = []
        st.session_state.game_over = False
        next_movie()
        st.rerun()

elif 'current_round' in st.session_state and st.session_state.current_round:
    
    # --- CALL THE TIMER FUNCTION ---
    inject_timer()
    
    current = st.session_state.current_round
    
    # 1. Display Image
    image_path = os.path.join(IMAGE_FOLDER, current['filename'])
    st.image(image_path, use_container_width=True)

    # 2. Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 Show Hint"):
            st.session_state.show_hint = True
            
    with col2:
        if st.button("👁️ Reveal Answer"):
            st.session_state.show_answer = True
            
    with col3:
        df = load_data()
        total_valid = len(get_valid_game_data(df))
        shown_count = len(st.session_state.shown_movies)
        remaining = total_valid - shown_count
        
        if st.button(f"⏭️ Next ({remaining} left)"):
            next_movie()
            st.rerun()

    # 3. Dynamic Information
    st.markdown("---")
    
    if st.session_state.show_hint:
        custom_hint = current.get('hint', '')
        if pd.isna(custom_hint) or custom_hint == '':
             movie_name = current['movie_name']
             hint_text = f"Starts with **{movie_name[0]}**... ({len(movie_name)} chars)"
        else:
             hint_text = custom_hint
             
        st.info(f"**Hint:** {hint_text}")

    if st.session_state.show_answer:
        st.success(f"🎉 The Movie is: **{current['movie_name']}**")

else:
    st.warning("Please upload `data.csv` and images to start.")
