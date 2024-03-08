from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# 環境変数からOpenAI APIキーをロード
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/openai_chat', methods=['POST'])
def openai_chat():
    data = request.json
    try:
        # 新しいAPIインターフェースを使用してチャットの応答を生成
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=data["messages"]
        )
        # 応答をJSON形式で返す
        return jsonify(response)
    except Exception as e:
        # エラー処理
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
