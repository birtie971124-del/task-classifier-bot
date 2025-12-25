from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    return "OK", 200

# 給 Vercel 用（一定要）
app = app
