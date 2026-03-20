from flask import Flask, request, abort
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "my_secret_123")
APP_ID = os.environ.get("APP_ID")
APP_SECRET = os.environ.get("APP_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

# Webhook 驗證
@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        abort(403)

# Webhook 接收事件
@app.route('/webhook', methods=['POST'])
def receive():
    data = request.json
    print("📩 收到事件：", data)
    return 'OK', 200

# 用戶登入後導回這裡
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return '登入失敗', 400

    # 用授權碼換取 Access Token
    res = requests.get('https://api.instagram.com/oauth/access_token', params={
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    })

    token_data = res.json()
    print("✅ Access Token：", token_data)
    return f"登入成功！Token: {token_data.get('access_token')}", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
