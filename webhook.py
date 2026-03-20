from flask import Flask, request, abort
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "my_secret_123")

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ 驗證成功！")
        return challenge, 200
    else:
        abort(403)

@app.route('/webhook', methods=['POST'])
def receive():
    data = request.json
    print("📩 收到事件：", data)
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
```

貼完後點下方 **Commit changes** → **Commit changes**

---

**第二個檔案：`requirements.txt`**

點 **Add file → Create new file**，檔名填 `requirements.txt`，內容：
```
flask
gunicorn
