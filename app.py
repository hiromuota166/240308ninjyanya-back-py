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
    if not data or 'messages' not in data:
        return jsonify({"error": "Invalid request. 'messages' field is required."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=data["messages"]
        )
        return jsonify(response)
    except openai.error.InvalidRequestError as e:
        # OpenAI APIの無効なリクエストに対するエラー処理
        return jsonify({"error": "Invalid request to OpenAI API.", "details": str(e)}), 400
    except openai.error.AuthenticationError:
        # 認証エラー（APIキーが無効または不足している）
        return jsonify({"error": "Authentication with OpenAI API failed."}), 401
    except openai.error.RateLimitError:
        # レート制限に達した場合
        return jsonify({"error": "Rate limit exceeded for OpenAI API."}), 429
    except openai.error.OpenAIError as e:
        # その他のOpenAI API関連のエラー
        return jsonify({"error": "An error occurred with the OpenAI API.", "details": str(e)}), 500
    except Exception as e:
        # その他の未知のエラー
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
