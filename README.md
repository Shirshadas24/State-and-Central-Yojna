````markdown
# 🏛️ YojnaBot — AI-Powered Chatbot for Indian Government Schemes - State and Central 🇮🇳

**YojnaBot** is an intelligent chatbot built with **LangChain** and **Devstral 2505 (Mistral fine-tune)**, alongside a **custom fine-tuned LLaMA model**, that helps users understand and access **central and state government schemes** through a conversational interface.

Currently deployed on **Telegram**, YojnaBot also offers a powerful **web-based chatbot** for seamless integration into government websites.

> 💬 Ask in **Hindi, English, or Hinglish** — YojnaBot speaks your language.

---

## 🚀 Live Project Links

-   [Try the Telegram Bot](https://t.me/YOUR_BOT_USERNAME) *(Currently runs only when the respective python file is ran on our system.)*
-   Web Integration: Fine-tuned LLaMA backend (Local Development for now)

---

## 🎯 Project Aim

Many Indian citizens are unaware of the benefits they’re entitled to under government schemes. YojnaBot breaks this barrier by:

-   Understanding natural-language queries from citizens
-   Fetching accurate information from a structured database
-   Giving simple, personalized responses in multiple languages
-   Running 24/7 on platforms like Telegram and government portals

---

## 💡 Features

* Query in **Hindi**, **English**, or **Hinglish** 🗣️
* **Dual LLM Approach**:
    * Uses **LangChain** with **Devstral-2505** via Hugging Face for the Telegram bot 🤖
    * Powers the web chatbot with a **custom fine-tuned LLaMA model** for efficient, localized inference 💻
* With auto language detection 🌐
* Dynamic retrieval with fuzzy & exact matching 🔍
* MongoDB-based logging for analysis 📊
* Will support **more Indian languages** in the future 🇮🇳
* Can run **forever** using startup scheduling (Telegram bot) and deployment (Website bot) ♾️

---

## 🧠 Architecture

-   **Query Handler** → Cleans, detects language, retrieves matching schemes
-   **Retriever** → TF-IDF & fuzzy matching from JSON knowledge base
-   **LLM Generators** →
    * Powered by `langchain.HuggingFaceEndpoint` with Devstral-2505 (for Telegram)
    * **Fine-tuned LLaMA model** integrated via a **Flask API backend** (for Web)
-   **Telegram Integration** → Real-time interaction with `/start` & messages
-   **Web Integration** → React-based frontend communicates with Flask API for real-time chat 💬
-   **Database Logger** → Saves every interaction with timestamp, user ID, query, and language 💾

---

## 🛠️ Tech Stack

| Area              | Stack                               |
|-------------------|-------------------------------------|
| Bot Framework     | Python + `python-telegram-bot`      |
| LLM APIs          | **Devstral-2505** via LangChain, **Fine-tuned LLaMA** (Local) |
| NLP Middleware    | Langchain `PromptTemplate`          |
| Fuzzy Matching    | `thefuzz` (FuzzyWuzzy)              |
| Database          | MongoDB (via PyMongo)               |
| Web Backend       | Flask, `Flask-CORS`                 |
| Web Frontend      | React.js, HTML, CSS                 |
| Hosting Support   | `pm2`, `.env`, virtualenv           |

---

## 📁 Project Structure

```bash
yojnabot/
│
├── backend/
│   ├── data/
│   │   └── schemes.json        # Government schemes dataset
│   ├── telegram_bot.py         # Telegram bot application
│   ├── query_handler.py        # Core logic using Devstral + LangChain
│   ├── utils/
│   │   ├── retriever.py        # Fuzzy & TF-IDF retrieval
│   │   └── db_logger.py        # MongoDB logger
│   ├── fine_tuned_tiny_llama/  # Directory for fine-tuned LLaMA model (for web chatbot)
│   │   ├── adapter_config.json
│   │   ├── adapter_model.safetensors
│   │   └── ...                 # Other model files
│   ├── chatbot_model.py        # LLaMA model loading & generation logic (used by web backend)
│   ├── app.py                  # Flask API for web chatbot
│   ├── .env                    # Contains API keys (ignored)
│   └── requirements.txt        # For backend dependencies
│
└── frontend/
    └── chatbot_frontend/       # React application for web chatbot UI
        ├── public/
        ├── src/
        │   ├── App.js
        │   ├── App.css
        │   └── ...
        ├── package.json
        └── ...
````

-----

## 🔧 How to Run

### Telegram Bot

```bash
# Clone the repo (if not already cloned)
git clone [https://github.com/Shirshadas24/State-and-Central-Yojna.git](https://github.com/Shirshadas24/State-and-Central-Yojna.git)
cd State-and-Central-Yojna/backend

# Set up virtual environment
python -m venv venv
venv\Scripts\activate          # (on Windows)
# source venv/bin/activate     # (on Linux/macOS)

# Install requirements
pip install -r requirements.txt

# Set your Telegram bot token
echo TELEGRAM_BOT_TOKEN=your_token_here > .env

# Run the Telegram bot
python telegram_bot.py
```

### Web Chatbot (Local Development)

To run the web chatbot, ensure your Telegram bot's `requirements.txt` has `Flask`, `Flask-CORS`, `peft`, and `safetensors` added.

1.  **Start the Flask Backend:**

    ```bash
    # Navigate to the backend directory
    cd State-and-Central-Yojna/backend

    # Ensure your virtual environment is active
    venv\Scripts\activate # (on Windows)
    # source venv/bin/activate # (on Linux/macOS)

    # Run the Flask application
    python app.py
    ```

    *(The backend will start and load the fine-tuned LLaMA model, typically accessible at `http://localhost:5000`)*

2.  **Start the React Frontend:**

    ```bash
    # Navigate to the frontend directory
    cd State-and-Central-Yojna/frontend/chatbot_frontend

    # Install frontend dependencies (if not already done)
    npm install

    # Start the React development server
    npm start
    ```

    *(The frontend will open in your browser, typically at `http://localhost:3000`)*

-----

## 👥 Team

| Member                                              | Role                                                    |
|-----------------------------------------------------|---------------------------------------------------------|
| [Shirsha Das](https://shirshadas.vercel.app/)       | Telegram bot, LangChain integration, query logic        |
| [Pritam Kumar Roy](https://pritam-kumar-roy.vercel.app/) | Fine-tuned LLaMA model, frontend website integration    |

## 🚀 Future Enhancements

🌐 Website integration with chatbot UI (achieved locally, planning for deployment\!)

🗣 Support for Bengali, Tamil, Telugu, Marathi, etc.

🔁 Continuous learning from user queries

📊 Admin analytics panel for scheme tracking

🔒 User verification and eligibility prediction

## 📜 License

MIT License.
Use freely for social good, with proper credit.

### 🇮🇳 Making governance accessible — one message at a time.

🙌 Jai Hind\!

```
```
