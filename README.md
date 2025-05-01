# AI-Melody-Maker
A Web app that lets anyone create songs using AI.

**AI-Melody-Maker** is a Streamlit-based web app that generates complete song blueprints, including **lyrics**, **melody snippets**, and **suggested song titles**, based on your selected **mood**, **genre**, and **keywords**. It uses powerful AI APIs like GPT-4 and Stable Audio for creative content generation.

## 🚀 Features

- 🎭 Select a **mood** (e.g., Happy, Sad, Energetic, Chill)
- 🎶 Choose a **genre** (e.g., Pop, Hip Hop, Classical, EDM)
- 📝 Optionally enter **keywords or themes** (e.g., love, rain, party)
- ✍️ Generates **original song lyrics** using GPT-4 (via AIML API)
- 🎼 Produces **melody previews** using Stable Audio
- 🎤 Suggests creative **song titles**
- 📥 Download lyrics (`.txt`) and melodies (`.wav` or `.midi`)

---

## 🧠 Tech Stack

- **Frontend & Backend**: [Streamlit](https://streamlit.io)
- **Language Model**: GPT-4 via [AIML API](https://api.aimlapi.com)
- **Melody Generation**: [Stable Audio](https://www.stableaudio.com)
- **Language**: Python

---

## 📁 Project Structure

```
Music Melody/
├── app.py               # Main Streamlit app
├── key.env              # API keys (not pushed to GitHub)
├── requirements.txt     # Python dependencies
```

---

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ai-melody-maker.git
   cd ai-melody-maker
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**:
   Copy `key.env` to `.env` and add your API keys:
   ```
   AIML_API_KEY=your_aiml_api_key
   STABLE_AUDIO_API_KEY=your_stable_audio_api_key
   ```

---

## 🧪 Running Locally

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`.

---

## ☁️ Deployment

### Option 1: Deploy on [Streamlit Cloud](https://streamlit.io/cloud)

1. Push your code to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud), connect your GitHub repo.
3. Add your `AIML_API_KEY` and `STABLE_AUDIO_API_KEY` as **secrets** in the dashboard.
4. Deploy!

---

## 💻 Google Colab (for quick testing)

You can also run the app in Google Colab by adapting it with:

- `%pip install streamlit pyngrok`
- Launch a tunnel with `pyngrok` to expose your local app
- Run Streamlit in the background

---

## 🧠 Beginner Tip

Even if you're new to Generative AI or Streamlit, this project is a great starting point to learn how language and music models can work together.

---
---

## 🙌 Acknowledgments

- [OpenAI GPT-4](https://openai.com/)
- [Stable Audio](https://www.stableaudio.com)
- [Streamlit](https://streamlit.io)

---

## 📬 Contact
Lets connect on linkedIn:(https://www.linkedin.com/in/abida-shoukat-a5518831b/)
Feel free to reach out via issues or fork and enhance the app!

```

