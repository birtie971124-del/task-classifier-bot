from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 從「環境變數」讀取金鑰（不是寫死）
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=["POST"])
def webhook():
    # 直接先回 200，讓 LINE Verify 不 timeout
    try:
        signature = request.headers.get("X-Line-Signature", "")
        body = request.get_data(as_text=True)

        # 如果是 Verify（通常沒有事件），直接回 OK
        if not body:
            return "OK"

        handler.handle(body, signature)
        return "OK"

    except InvalidSignatureError:
        # Verify 時最常進這裡，但也要回 200
        return "OK"

# ✅ 收到文字訊息就回一句
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="我有收到你的訊息！")
    )

if __name__ == "__main__":
    app.run()
