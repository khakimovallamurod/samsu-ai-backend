from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import config
import re

app = Flask(__name__)
CORS(app)

def decode_response_text(resp_text: str) -> str:

    cleaned = resp_text.replace("\n", "")

    parts = re.findall(r'0:"(.*?)"', cleaned)

    joined = "".join(parts)

    decoded = joined.encode("utf-16", "surrogatepass").decode("utf-16")
    return decoded.strip()


@app.route("/chat", methods=["POST"])
def chat_with_samdu():
    URL = config.get_url()
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Iltimos, 'message' maydonini yuboring."}), 400

    user_message = data["message"]

    payload = {
        "blockId": "cmgroxc0l0009nqgqabp29veu",
        "params": {
            "params": {
                "publishedPageParams": ["samdu"]
            }
        },
        "stream": True,
        "chatbotSessionId": "cmgrxwbgc015z5l0y9h8dixna",
        "predictionId": "853ff38c-b601-497e-b503-176bbfa73be3",
        "message": {
            "content": user_message,
            "parts": [
                {"type": "text", "text": user_message}
            ],
            "role": "user"
        }
    }

    headers = {"Content-Type": "application/json"}
    
    response = requests.post(URL, json=payload, headers=headers)
    result_text = decode_response_text(resp_text = response.text)
    if response.status_code != 200:
        return jsonify({
            "status": "error",
            "user_message": user_message,
            "response": None
        })

    return jsonify({
        "status": "success",
        "user_message": user_message,
        "response": result_text
    })


if __name__ == "__main__":
    app.run(debug=True)
