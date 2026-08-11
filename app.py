from flask import Flask, render_template, request, jsonify

from chatbot.chatbot_engine import get_response

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "response": "Please enter a question."
            })

        # Send the student's question to the chatbot engine
        response = get_response(user_message)

        return jsonify({
            "response": response
        })

    except Exception as e:
        print("CHAT ERROR:", e)

        return jsonify({
            "response": "Sorry, something went wrong while processing your question."
        }), 500


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)