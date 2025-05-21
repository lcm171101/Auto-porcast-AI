from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
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

    if hour == 11 and 0 <= minute <= 50000:
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
    return [
        "Google Trends：輝達台灣設總部",
        "Dcard 熱門：畢業季感言刷屏",
        "PTT：太妍大巨蛋演唱會熱烈討論",
        "YouTube：世壯運影片爆紅",
        "LINE TODAY：三峽車禍關注",
        "Facebook：貴婦奈奈返台懺悔文",
        "Instagram：白沙屯媽祖圖集洗版",
        "新聞媒體：核電退役討論白熱化",
        "Twitter/X：剴剴案引全球關注",
        "論壇綜合：罷免影片引爆評論潮"
    ]

if __name__ == "__main__":
    app.run()
