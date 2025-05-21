import requests
from bs4 import BeautifulSoup
import feedparser
from pytrends.request import TrendReq

def get_google_trends_tw():
    pytrends = TrendReq(hl='zh-TW', tz=480)
    try:
        pytrends.build_payload([""], geo='TW')
        related = pytrends.related_queries()
        rising = related.get("", {}).get("rising")

        if rising is None or rising.empty:
            return ["[Google 熱搜 TW] 暫無資料"]

        return [f"[Google 熱搜 TW] {row['query']}" for _, row in rising.head(3).iterrows()]
    except Exception as e:
        print("🔥 Google 熱搜擷取失敗：", e)
        return ["[Google 熱搜 TW] 擷取失敗"]

def get_ptt_hot_titles():
    url = "https://www.ptt.cc/bbs/Gossiping/index.html"
    cookies = {'over18': '1'}
    try:
        resp = requests.get(url, cookies=cookies, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for div in soup.select('div.title'):
            if div.a:
                results.append("[PTT] " + div.a.text.strip())
        return results[:3]
    except Exception as e:
        print("🔥 PTT 擷取失敗：", e)
        return ["[PTT] 擷取失敗"]

def get_dcard_hot_titles():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = "https://www.dcard.tw/service/api/v2/posts?popular=true&limit=5"
        resp = requests.get(url, headers=headers, timeout=10)

        if not resp.content.strip():  # 空白內容
            raise ValueError("Dcard response is empty")

        posts = resp.json()
        return [f"[Dcard] {p['title']}" for p in posts]
    except Exception as e:
        print("🔥 Dcard 擷取失敗：", e)
        return ["[Dcard] 擷取失敗"]

def get_yahoo_hot_news():
    try:
        rss_url = "https://tw.news.yahoo.com/rss/"
        feed = feedparser.parse(rss_url)
        return [f"[Yahoo] {entry.title}" for entry in feed.entries[:3]]
    except Exception as e:
        print("🔥 Yahoo 擷取失敗：", e)
        return ["[Yahoo] 擷取失敗"]

def get_hot_topics():
    return get_google_trends_tw() + get_ptt_hot_titles() + get_dcard_hot_titles() + get_yahoo_hot_news()
