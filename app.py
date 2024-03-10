from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# 環境変数からOpenAI APIキーをロード
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/api/openai_chat", methods=["POST"])
def openai_chat():
    data = request.json
    if not data or "messages" not in data:
        return jsonify({"error": "Invalid request. 'messages' field is required."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", response_format={ "type": "json_object" },messages=data["messages"]
        )
        return jsonify(response)

    except Exception as e:
        # その他の未知のエラー
        return (
            jsonify({"error": "An unexpected error occurred.", "details": str(e)}),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True)
