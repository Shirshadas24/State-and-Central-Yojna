# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from query_handler import handle_query

# app = Flask(__name__)
# CORS(app)

# @app.route("/api/chat", methods=["POST"])
# def chat():
#     user_query = request.json.get("query")
#     language = request.json.get("language", "Hinglish")  # Default: Hinglish
#     response = handle_query(user_query, language)
#     return jsonify({"response": response})

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from query_handler import handle_query

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query")
    language = request.json.get("language", "Hinglish")
    user_id = request.json.get("user_id", "anonymous")

    print("📩 Incoming Request:", user_query, language)  # Log incoming request
    response_text = handle_query(user_query, language,user_id)
    print("📤 Final Response Sent:", response_text)  # Log outgoing response

    # Force uncached, fresh response to client
    response = make_response(jsonify({"response": response_text}))
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, threaded=False)
