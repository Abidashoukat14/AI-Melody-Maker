import streamlit as st
from openai import OpenAI
import requests
import os
import time
from dotenv import load_dotenv
from pathlib import Path
import base64

# Load environment variables
load_dotenv("key.env")
st.set_page_config(page_title="AI Melody Maker", page_icon="🎵")
def set_custom_background(image_file):
    image_path = Path(image_file)
    if image_path.exists():
        with open(image_path, "rb") as img_file:
            b64_encoded = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{b64_encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                font-family: 'Segoe UI', sans-serif;
            }}
            h1 {{
                text-align: center;
                font-size: 3em;
                background: linear-gradient(90deg, #ff00ff, #00ffff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
                margin-top: 20px;
            }}
            .block-container {{
                background-color: rgba(0, 0, 0, 0.6);
                padding: 2rem;
                border-radius: 20px;
                margin-top: 30px;
            }}
            .stTextInput > div > input,
            .stSelectbox > div,
            .stTextArea textarea {{
                background-color: rgba(255, 255, 255, 0.1) !important;
                color: white !important;
                border: 1px solid #00ffff;
                border-radius: 10px;
            }}
            .stButton button {{
                background-image: linear-gradient(to right, #ff00ff, #6600ff);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 10px;
                font-weight: bold;
                box-shadow: 0 0 10px #ff00ff;
            }}
            .stSubheader, .stMarkdown, .stText, .stAudio {{
                color: white;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

set_custom_background("background.webp")

# --- API KEYS ---
AIML_API_KEY = "8f3498fe90434e61a5913cb35000b4ff"  # For both GPT and Stable Audio

if not AIML_API_KEY:
    st.error("❌ AIML_API_KEY not found. Make sure it's set in key.env.")
    st.stop()

# --- Initialize AI/ML GPT-4o client ---
try:
    aiml_api = OpenAI(
        api_key=AIML_API_KEY,
        base_url="https://api.aimlapi.com/v1"
    )
    st.info("✅ AIML API client initialized.")
except Exception as e:
    st.error(f"❌ Failed to initialize AIML API client: {e}")
    st.stop()

st.title("🎵 AI Melody Maker")
st.markdown("Generate **lyrics**, **melodies**, and **titles** with the power of Generative AI!")

# --- UI for inputs ---
mood = st.selectbox("Choose a mood", ["Happy", "Sad", "Chill", "Energetic"])
genre = st.selectbox("Choose a genre", ["Pop", "Hip Hop", "Classical", "EDM", "Rock"])
keywords = st.text_input("Enter keywords (optional)", placeholder="e.g., love, rain, party")

if st.button("Generate Song"):
    with st.spinner("Creating your AI song..."):
        st.info("🎤 Generating lyrics...")

        try:
            # --- Lyrics generation ---
            lyric_prompt = f"Write song lyrics in {genre} style with a {mood} mood. Use themes: {keywords or 'any'}."
            lyrics_result = aiml_api.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": lyric_prompt}],
                temperature=0.7,
                max_tokens=300
            )
            lyrics = lyrics_result.choices[0].message.content
            st.success("✅ Lyrics generated.")
        except Exception as e:
            st.error(f"❌ Failed to generate lyrics: {e}")
            st.stop()

        st.info("🧠 Generating title...")

        try:
            # --- Title suggestion ---
            title_prompt = f"Give a short, catchy title for this song: {lyrics}"
            title_result = aiml_api.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": title_prompt}],
                temperature=0.7,
                max_tokens=20
            )
            title = title_result.choices[0].message.content.strip().strip('"')
            st.success("✅ Title generated.")
        except Exception as e:
            st.error(f"❌ Failed to generate title: {e}")
            title = "Untitled"

# ... (keep all previous imports and setup code until the melody generation part)

        st.info("🎼 Generating melody...")

        # --- Stable Audio Generation ---
        try:
            # API Configuration
            STABLE_AUDIO_ENDPOINT = "https://api.aimlapi.com/v2/generate/audio"
            headers = {
                "Authorization": f"Bearer {AIML_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "*/*"
            }
            
            payload = {
                "model": "stable-audio",
                "prompt": f"A {mood.lower()} {genre.lower()} melody about {keywords or 'anything'}",
                "seconds_start": 1,
                "seconds_total": 30,
                "steps": 100
            }

            # Submit generation request
            response = requests.post(STABLE_AUDIO_ENDPOINT, headers=headers, json=payload)
            
            if response.status_code == 201:  # Changed from 200 to 201
                generation_data = response.json()
                generation_id = generation_data.get("id")
                initial_status = generation_data.get("status")
                
                st.success(f"✅ Melody generation {initial_status} (ID: {generation_id})")
                
                # Poll for completion
                max_attempts = 20  # Increased to ~100 seconds total wait time
                progress_bar = st.progress(0)
                status_text = st.empty()
                audio_url = None
                
                for attempt in range(max_attempts):
                    time.sleep(5)  # Check every 5 seconds
                    progress = (attempt + 1) / max_attempts
                    progress_bar.progress(progress)
                    
                    # Check generation status
                    status_response = requests.get(
                        STABLE_AUDIO_ENDPOINT,
                        headers=headers,
                        params={"generation_id": generation_id}
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        current_status = status_data.get("status")
                        status_text.info(f"Generation Status: {current_status} (Attempt {attempt + 1}/{max_attempts})")
                        
                        if current_status == "completed":
                            audio_url = status_data.get("audio_file", {}).get("url")
                            if audio_url:
                                st.success("✅ Audio generation complete!")
                                break
                        elif current_status == "failed":
                            error_msg = status_data.get("error", "Unknown error")
                            st.error(f"❌ Generation failed: {error_msg}")
                            break
                        # Add handling for other statuses if needed
                    else:
                        status_text.warning(f"Status check failed (HTTP {status_response.status_code})")
                
                progress_bar.empty()
                
                # Display results
                if audio_url:
                    st.subheader("🎧 Melody Preview")
                    
                    # Display audio player with retry option if loading fails
                    audio_placeholder = st.empty()
                    try:
                        audio_placeholder.audio(audio_url)
                    except:
                        st.warning("Audio preview unavailable - try downloading instead")
                    
                    # Download button with error handling
                    try:
                        audio_data = requests.get(audio_url).content
                        st.download_button(
                            label="⬇️ Download Melody",
                            data=audio_data,
                            file_name=f"{title.replace(' ', '_')}_melody.wav",
                            mime="audio/wav"
                        )
                    except Exception as e:
                        st.error(f"Failed to download audio: {str(e)}")
                else:
                    st.warning("⚠️ Audio generation did not complete. Try again later.")
            
            else:
                st.error(f"❌ Failed to start audio generation: {response.status_code}")
                st.json(response.json())
        
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")

# ... (rest of your existing code)

        # --- Display Results ---
        st.subheader("🎶 Title:")
        st.write(title)

        st.subheader("📝 Lyrics:")
        st.text(lyrics)

        st.download_button("📄 Download Lyrics", lyrics, file_name=f"{title}_lyrics.txt")