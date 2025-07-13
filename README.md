<h1 align="center">🏛️ YojnaBot – AI-Powered Chatbot for Indian Government Schemes 🇮🇳</h1>

<p align="center">
  <b>Empowering citizens with easy access to central and state government schemes.</b><br />
  <i>Built using LangChain, Devstral-2505, and a fine-tuned LLaMA model</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/NLP-GovSchemes-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/LLM-LLaMA--based-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Platform-Telegram%20%7C%20Web-critical?style=flat-square" />
  <img src="https://img.shields.io/badge/Language-Hindi%2FEnglish%2FHinglish-informational?style=flat-square" />
</p>

---

## 🔗 Live Project Links

- 🤖 [**Try the Telegram Bot**](https://t.me/YOUR_BOT_USERNAME) *(Available when backend is active locally)*
- 💬 **Web Chatbot** powered by fine-tuned LLaMA *(Localhost only for now)*

---

## 🎯 Objective

> Many Indian citizens are unaware of the government schemes they are eligible for.  
> **YojnaBot** bridges this gap using natural language conversation.

- Understands user queries in **English, Hindi, and Hinglish**
- Fetches personalized answers from central/state **Yojna databases**
- Available on **Telegram** and **Web Portals**
- Plans to scale across **vernacular languages** and official **government sites**

---

## ✨ Key Features

✅ Multilingual: English, Hindi, Hinglish  
✅ Smart retrieval: Fuzzy + semantic matching  
✅ Dual LLM engine:
- 📱 **Telegram** – LangChain + Devstral-2505
- 🌐 **Web** – Fine-tuned **TinyLLaMA-1.1B-Chat**

✅ Optimized for local CPU deployment  
✅ MongoDB logging for analytics  
✅ React-based frontend integration  
✅ Future-ready with multiple state integrations

---

---

## 🛠 Tech Stack

| Area             | Technologies |
|------------------|--------------|
| Bot Framework    | Python, Telegram Bot API |
| LLM Models       | Devstral-2505 (LangChain), Fine-tuned TinyLLaMA |
| Retrieval Engine | TF-IDF, FuzzyWuzzy (`thefuzz`) |
| NLP Pipeline     | LangChain, PromptTemplate |
| Backend API      | Flask + Flask-CORS |
| Frontend         | React.js + CSS |
| Database         | MongoDB |
| Deployment Tools | `pm2`, `venv`, `.env` |

---

## 🧠 Telegram Bot Architecture

```
backend/
├── data/
│   └── schemes.json                # Knowledge base (state + central yojnas)
├── utils/
│   ├── db_logger.py                # Logs user queries and responses to MongoDB
│   └── retriever.py                # Fuzzy + TF-IDF-based scheme retriever
├── query_handler.py                # Core NLP logic with LangChain
├── telegram_bot.py                 # Telegram Bot API handler
├── app.py                          # (Optional) API entry if reused
├── requirements.txt                # All backend dependencies
└── .gitignore

```

## 🌐 Yojna Web Chatbot Structure

```
WEB/
├── chatbot_backend/                # Flask API for chatbot
│   ├── fine_tuned_tiny_llama/
│   │   ├── adapter_config.json
│   │   ├── adapter_model.safetensors
│   │   ├── chat_template.jinja
│   │   ├── optimizer.pt
│   │   ├── rng_state.pth
│   │   ├── scaler.pt
│   │   ├── scheduler.pt
│   │   ├── special_tokens_map.json
│   │   ├── tokenizer_config.json
│   │   ├── tokenizer.json
│   │   ├── tokenizer.model
│   │   ├── trainer_state.json
│   │   └── training_args.bin
│   ├── chatbot_model.py            # Loads model + handles prompt/response
│   ├── app.py                      # Flask server + CORS config
│   └── requirements.txt
│
└── chatbot_frontend/chatbot/       # React.js frontend (Vite)
    ├── public/
    ├── src/
    │   ├── assets/
    │   ├── App.jsx
    │   ├── App.css
    │   ├── index.css
    │   └── main.jsx
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── README.md

```

---

## ⚙️ How to Run

### 🚀 Telegram Bot (Devstral via LangChain)

```bash
# Clone the repo and navigate to backend
git clone https://github.com/Shirshadas24/State-and-Central-Yojna.git
cd State-and-Central-Yojna/backend

# Setup virtualenv and activate it
python -m venv venv
venv\Scripts\activate             # Windows
# source venv/bin/activate       # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Create .env and set token
echo TELEGRAM_BOT_TOKEN=your_token_here > .env

# Run the bot
python telegram_bot.py
```

---

### 🌐 Web Chatbot (React + Flask + Fine-Tuned LLaMA)

1. **Start Flask API (Backend):**

```bash
cd State-and-Central-Yojna/backend
venv\Scripts\activate
python app.py
```

📍 *Runs at:* `http://localhost:5000/chat`

2. **Start React App (Frontend):**

```bash
cd ../frontend/chatbot_frontend
npm install
npm start
```

📍 *Runs at:* `http://localhost:3000`

> React frontend sends POST requests to the Flask backend which uses your fine-tuned LLaMA to generate responses.

---

## 👨‍💻 Contributors

| Name | Role |
|------|------|
| [Shirsha Das](https://shirshadas.vercel.app/) | Telegram Bot, LangChain/NLP pipeline |
| [Pritam Kumar Roy](https://pritam-kumar-roy.vercel.app/) | Fine-tuned LLaMA, Web frontend integration |

---

## 🌱 Future Roadmap

- ✅ Web chatbot interface (DONE!)
- 🌐 Deploy on government portals
- 🔠 Support major Indian languages (Bengali, Tamil, Telugu, Marathi)
- 🎯 Eligibility engine (predict if user qualifies)
- 📊 Admin dashboard for scheme tracking
- 🔐 Aadhar-based secure login (optional)

---

## 📜 License

MIT License — Free to use for public welfare. Attribution appreciated.

---

<p align="center"><b>🇮🇳 Making governance accessible — one message at a time.</b><br/><i>🙌 Jai Hind!</i></p>
