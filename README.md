# 🏛️ YojnaBot — AI-Powered Chatbot for Indian Government Schemes - Sate and Central 🇮🇳

**YojnaBot** is an intelligent chatbot built with **LangChain** and **Devstral 2505 (Mistral fine-tune)** that helps users understand and access **central and state government schemes** through a conversational interface — currently deployed on **Telegram** and can be integrated into government websites via an already **fine-tuned LLaMA model**.

> 💬 Ask in **Hindi, English, or Hinglish** — YojnaBot speaks your language.

---

## 🚀 Live Project Links

-  [Try the Telegram Bot](https://t.me/YOUR_BOT_USERNAME) *(Currently runs only when the respective python file is ran on our system.)*
-  Web Integration: Fine-tuned LLaMA backend

---

## 🎯 Project Aim

Many Indian citizens are unaware of the benefits they’re entitled to under government schemes. YojnaBot breaks this barrier by:

- Understanding natural-language queries from citizens
- Fetching accurate information from a structured database
- Giving simple, personalized responses in multiple languages
- Running 24/7 on platforms like Telegram and government portals

---

## 💡 Features

* Query in **Hindi**, **English**, or **Hinglish**  
* Uses **LangChain** with **Devstral-2505** via Hugging Face for Telegram bot
* With auto language detection
* Dynamic retrieval with fuzzy & exact matching
* MongoDB-based logging for analysis  
* Powerful web chatbot (LLaMA fine-tuned)   
* Will support **more Indian languages**  
* Can run **forever** using startup scheduling (Telegram bot) and deployment (Website bot)

---

## 🧠 Architecture

- **Query Handler** → Cleans, detects language, retrieves matching schemes
- **Retriever** → TF-IDF & fuzzy matching from JSON knowledge base
- **LLM Generator** → Powered by `langchain.HuggingFaceEndpoint` with Devstral-2505
- **Telegram Integration** → Real-time interaction with `/start` & messages
- **Database Logger** → Saves every interaction with timestamp, user ID, query, and language

---

## 🛠️ Tech Stack

| Area              | Stack                            |
|-------------------|----------------------------------|
| Bot Framework     | Python + `python-telegram-bot`   |
| LLM API           | **Devstral-2505** via LangChain  |
| NLP Middleware    | Langchain `PromptTemplate`       |
| Fuzzy Matching    | `thefuzz` (FuzzyWuzzy)           |
| Database          | MongoDB (via PyMongo)            |
| Hosting Support   | `pm2`, `.env`, virtualenv        |

---

## 📁 Project Structure
```bash
yojnabot/
│
├── backend/
│ ├── data/schemes.json # Government schemes dataset
│ ├── telegram_bot.py # Telegram bot
│ ├── query_handler.py # Core logic using Devstral + LangChain
│ ├── utils/
│ │ ├── retriever.py # Fuzzy & TF-IDF retrieval
│ │ └── db_logger.py # MongoDB logger
│ ├── .env # Contains API keys (ignored)
│ ├── requirements.txt
```

---

## 🔧 How to Run

```bash
# Clone the repo
git clone https://github.com/Shirshadas24/State-and-Central-Yojna.git
cd State-and-Central-Yojna/backend

# Set up virtual environment
python -m venv venv
venv\Scripts\activate         # (on Windows)

# Install requirements
pip install -r requirements.txt

# Set your bot token
echo TELEGRAM_BOT_TOKEN=your_token_here > .env

# Run the Telegram bot
python telegram_bot.py
```
##  Team
| Member                                                     | Role                                                  |
|------------------------------------------------------------|-------------------------------------------------------|
| [Shirsha Das](https://shirshadas.vercel.app/)              | Telegram bot, LangChain integration, query logic      |
| [Pritam Kumar Roy](https://pritam-kumar-roy.vercel.app/)   | Fine-tuned LLaMA model, frontend website integration  |


##  Future Enhancements
🌐 Website integration with chatbot UI

🗣 Support for Bengali, Tamil, Telugu, Marathi, etc.

🔁 Continuous learning from user queries

📊 Admin analytics panel for scheme tracking

🔒 User verification and eligibility prediction

## 📜 License
MIT License.
Use freely for social good, with proper credit.

### 🇮🇳 Making governance accessible — one message at a time.
🙌 Jai Hind!
