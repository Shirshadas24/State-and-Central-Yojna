from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_model import load_fine_tuned_model, generate_chat_response, FINE_TUNED_MODEL_PATH
import os

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Global variables to hold the loaded model and tokenizer
model = None
tokenizer = None
conversation_history = {} # A dictionary to store chat history per session/user if needed

# --- Model Loading moved to if __name__ == '__main__': block ---
# This block will handle loading the model and tokenizer only once when the server starts.
# No decorator is needed here, as it runs sequentially before app.run()

@app.route('/chat', methods=['POST'])
def chat():
    # Ensure model and tokenizer are loaded. This check is redundant if loaded in main,
    # but good for safety, especially if not run via `app.run` directly in production setups.
    if model is None or tokenizer is None:
        return jsonify({"error": "Model not loaded. Server is not ready."}), 503

    data = request.json
    user_message = data.get('message')
    user_id = data.get('user_id', 'default_user')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    try:
        response = generate_chat_response(
            model=model,
            tokenizer=tokenizer,
            user_input=user_message,
            chat_history=conversation_history[user_id]
        )
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error during chat generation: {e}")
        return jsonify({"error": "An error occurred during response generation."}), 500

@app.route('/reset', methods=['POST'])
def reset_chat():
    user_id = request.json.get('user_id', 'default_user')
    if user_id in conversation_history:
        del conversation_history[user_id]
        return jsonify({"message": f"Chat history for {user_id} reset successfully."})
    else:
        return jsonify({"message": f"No chat history found for {user_id} to reset."}), 200

@app.route('/')
def index():
    return "Chatbot API is running. Send POST requests to /chat"

if __name__ == '__main__':
    print("Attempting to load model and tokenizer for Flask app...")
    model, tokenizer = load_fine_tuned_model(FINE_TUNED_MODEL_PATH)

    if model and tokenizer:
        print("Model and Tokenizer loaded successfully for API. Starting Flask app...")
        app.run(host='0.0.0.0', port=5000, debug=False) # Changed to False
    else:
        print("Failed to load model and tokenizer. Flask app will not start.")