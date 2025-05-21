from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from linebot.exceptions import InvalidSignatureError
import os
from datetime import datetime, timedelta

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

@app.route("/", methods=["GET"])
def index():
    return "LINE 熱門話題推播服務運作中"

@app.route("/trigger", methods=["GET"])
def trigger_push():
    taiwan_now = datetime.utcnow() + timedelta(hours=8)
    hour = taiwan_now.hour
    minute = taiwan_now.minute

    if hour == 11 and 0 <= minute <= 10:
        return push_hot_topics()
    else:
        return f"目前時間 {taiwan_now.strftime('%H:%M')}，非觸發推播時段（每日 11:00～11:10），請稍後再試。"

@app.route("/push_hot", methods=["POST"])
def push_hot_topics():
    hot_topics = get_hot_topics()
    message = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(hot_topics)])
    line_bot_api.push_message(os.environ.get("LINE_TARGET_ID"), TextSendMessage(text=f"【今日熱門話題】\n{message}"))
    return "OK"

def get_hot_topics():
    # 模擬「台灣前十大網站」的熱門話題整合
    return [
        "Google 熱搜：AI 面試趨勢崛起",
        "YouTube 熱門：周杰倫新歌登榜首",
        "Facebook 熱門貼文：選舉假消息澄清潮",
        "PTT 熱門：太妍大巨蛋演唱會討論破千樓",
        "Dcard 熱門：畢業季大頭貼回顧潮",
        "Yahoo 新聞：輝達設台灣總部引爆AI股",
        "LINE TODAY：三峽國小車禍引政府關注",
        "ETtoday 熱門：星座配對趣味分析",
        "Mobile01 討論：電動車補助新規公布",
        "Instagram 熱門貼文：白沙屯媽祖圖集爆紅"
    ]

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
    user_id = getattr(event.source, 'user_id', None)
    group_id = getattr(event.source, 'group_id', None)

    text = event.message.text.strip()
    reply = ""

    if text == "今日話題":
        hot_topics = get_hot_topics()
        message = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(hot_topics)])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"【今日熱門話題】\n{message}"))
        return
    else:
        reply = "收到訊息～\n"
        if user_id:
            reply += f"userId: {user_id}"
        elif group_id:
            reply += f"groupId: {group_id}"
        else:
            reply += "來源不明"

        print("[Webhook] 來源ID =>", reply.replace("\n", " | "))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
