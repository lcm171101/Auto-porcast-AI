from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from linebot.exceptions import InvalidSignatureError
import os
from datetime import datetime, timedelta
from crawler import get_hot_topics

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

@app.route("/", methods=["GET"])
def index():
    return "LINE 熱門話題爬蟲整合服務"

@app.route("/trigger", methods=["GET"])
def trigger_push():
    taiwan_now = datetime.utcnow() + timedelta(hours=8)
    hour = taiwan_now.hour
    minute = taiwan_now.minute
    if hour == 11 and 0 <= minute <= 10:
        return push_hot_topics()
    else:
        return f"目前時間 {taiwan_now.strftime('%H:%M')}，非觸發推播時段（每日 11:00～11:10）"

@app.route("/push_hot", methods=["POST"])
def push_hot_topics():
    hot_topics = get_hot_topics()
    message = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(hot_topics)])
    line_bot_api.push_message(os.environ.get("LINE_TARGET_ID"), TextSendMessage(text=f"【今日熱門話題】\n{message}"))
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    if text == "今日話題":
        hot_topics = get_hot_topics()
        message = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(hot_topics)])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"【今日熱門話題】\n{message}"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入「今日話題」來查詢最新熱門資訊"))
