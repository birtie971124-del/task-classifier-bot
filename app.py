from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# 你的 LINE Bot 金鑰
LINE_CHANNEL_ACCESS_TOKEN = "JbOsAjV/xBwd2VSebFVc5bidob35inj+IuXFXKyKzULvs0AoWZ3rsysGITiSTVoDpHzFwWHktcmUs5KvUb89y6yRNs1hgp9tiwgVKOtQvgaughLtNJ1FXPjHKyv9p88Ay+fgGFZlcBtJPEO2PiAsPQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0f5e2e395355f37edac942132d703cf0"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Google Sheets 授權
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(
    "formal-archive-468002-i2-0601638b6375.json",
    scopes=scope
)
client = gspread.authorize(creds)
sheet = client.open("任務分類表").sheet1


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    # 寫入 Google Sheets
    sheet.append_row([text])

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"已收到並記錄：{text}")
    )


@app.route("/")
def home():
    return "LINE Bot is running!"


if __name__ == "__main__":
    app.run()
