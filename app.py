import streamlit as st
import os
import random

# --- CONFIGURATION ---
IMAGE_FOLDER = 'images'
APP_TITLE = "🎬 Bollywood Visuals Challenge"

# --- SETUP PAGE ---
st.set_page_config(page_title="Bollywood Guess", page_icon="🎥")
st.title(APP_TITLE)

# --- FUNCTIONS ---
def get_images():
    """Reads all image files from the folder."""
    if not os.path.exists(IMAGE_FOLDER):
        st.error(f"Folder '{IMAGE_FOLDER}' not found! Please create it.")
        return []
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    return [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(valid_extensions)]

def next_movie():
    """Picks a random movie and resets state."""
    images = get_images()
    if images:
        st.session_state.current_image = random.choice(images)
        st.session_state.show_answer = False
        st.session_state.show_hint = False
    else:
        st.error("No images found in the folder!")

# --- INITIALIZATION ---
if 'current_image' not in st.session_state:
    next_movie()

# --- GAME UI ---
if 'current_image' in st.session_state and st.session_state.current_image:
    image_file = st.session_state.current_image
    # Remove extension to get movie name (e.g., "Sholay.jpg" -> "Sholay")
    movie_name = os.path.splitext(image_file)[0]
    
    # 1. Display the Image
    st.image(os.path.join(IMAGE_FOLDER, image_file), use_container_width=True)

    # 2. Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 Show Hint"):
            st.session_state.show_hint = True
            
    with col2:
        if st.button("👁️ Reveal Answer"):
            st.session_state.show_answer = True
            
    with col3:
        if st.button("⏭️ Next Movie"):
            next_movie()
            st.rerun()

    # 3. Dynamic Information
    st.markdown("---")
    
    if st.session_state.show_hint:
        # Simple hint logic: First letter + length
        hint_text = f"Starts with **{movie_name[0]}**... ({len(movie_name)} characters)"
        st.info(f"Hint: {hint_text}")

    if st.session_state.show_answer:
        st.success(f"🎉 The Movie is: **{movie_name}**")

else:
    st.warning("Please add images to the 'bollywood_images' folder to start.")

# --- SIDEBAR (Optional Instructions) ---
with st.sidebar:
    st.header("How to Play")
    st.write("1. Look at the visual cue.")
    st.write("2. Guess the Bollywood movie!")
    st.write("3. Use hints if you're stuck.")
    st.write(f"**Total Images Loaded:** {len(get_images())}")
