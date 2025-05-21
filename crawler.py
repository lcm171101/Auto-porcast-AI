import requests
from bs4 import BeautifulSoup
import feedparser
from pytrends.request import TrendReq

def get_ptt_hot_titles():
    url = "https://www.ptt.cc/bbs/Gossiping/index.html"
    cookies = {'over18': '1'}
    resp = requests.get(url, cookies=cookies, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')
    results = []
    for div in soup.select('div.title'):
        if div.a:
            results.append("[PTT] " + div.a.text.strip())
    return results[:3]

def get_dcard_hot_titles():
    url = "https://www.dcard.tw/service/api/v2/posts?popular=true&limit=5"
    resp = requests.get(url, timeout=10)
    posts = resp.json()
    return [f"[Dcard] {p['title']}" for p in posts]

def get_yahoo_hot_news():
    rss_url = "https://tw.news.yahoo.com/rss/"
    feed = feedparser.parse(rss_url)
    return [f"[Yahoo] {entry.title}" for entry in feed.entries[:3]]

def get_google_trends():
    pytrends = TrendReq(hl='zh-TW', tz=480)
    trending_searches_df = pytrends.trending_searches(pn='taiwan')
    top10 = trending_searches_df.head(3)[0].tolist()
    return [f"[Google 熱搜] {item}" for item in top10]

def get_hot_topics():
    return get_google_trends() + get_ptt_hot_titles() + get_dcard_hot_titles() + get_yahoo_hot_news()
