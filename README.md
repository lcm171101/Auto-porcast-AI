# 📣 LINE 熱門話題推播系統（爬蟲整合版）

本專案為一套 LINE Bot 系統，可每日整合台灣多個熱門網站之即時熱門話題，並提供手動或定時推播功能。

---

## ✅ 功能簡介

| 功能名稱             | 說明 |
|----------------------|------|
| 🔹 熱門資料整合       | 從 Google 熱搜、PTT、Dcard、Yahoo 新聞自動擷取熱門話題 |
| 🔹 LINE 主動推播     | 可透過 `/trigger` 或 `/push_hot` 自動推送當日話題 |
| 🔹 LINE 指令觸發     | 使用者傳送「今日話題」文字，即可觸發熱門話題回覆 |
| 🔹 多來源爬蟲整合     | 使用 pytrends、requests、BeautifulSoup、feedparser 等套件擷取內容 |

---

## 🔗 資料來源

- [Google Trends](https://trends.google.com.tw/trends/trendingsearches/daily?geo=TW)
- [PTT Gossiping](https://www.ptt.cc/bbs/Gossiping/index.html)
- [Dcard 熱門 API](https://www.dcard.tw/f)
- [Yahoo 新聞 RSS](https://tw.news.yahoo.com/rss/)

---

## 📁 專案結構

```
.
├── app.py                 # 主程式：Flask + LINE webhook + 路由
├── crawler.py             # 熱門話題擷取邏輯（爬蟲 + API 整合）
├── requirements.txt       # 所需套件
└── .env.example           # 環境變數設定範例
```

---

## 🚀 快速啟動方式

### 1️⃣ 安裝套件

```bash
pip install -r requirements.txt
```

### 2️⃣ 建立 `.env` 檔案

```env
LINE_CHANNEL_ACCESS_TOKEN=你的Channel Access Token
LINE_CHANNEL_SECRET=你的Channel Secret
LINE_TARGET_ID=你的userId或群組ID
```

### 3️⃣ 執行 Flask 開發伺服器

```bash
python app.py
```

或部署至 Render 時使用：

```bash
gunicorn app:app
```

---

## 🌐 路由說明

| 路由          | 方法 | 說明                          |
|---------------|------|-------------------------------|
| `/`           | GET  | 首頁狀態確認                   |
| `/trigger`    | GET  | 11:00–11:10 可手動觸發推播     |
| `/push_hot`   | POST | 後台手動推播（整合話題）       |
| `/webhook`    | POST | LINE Webhook 接收訊息          |

---

## 🧪 測試方式

1. 使用 Postman / curl 呼叫 `/trigger`
2. 在 LINE 傳送文字：「今日話題」
3. 查看是否收到整合熱門話題推播

---

## 📦 使用套件

- Flask
- line-bot-sdk
- gunicorn
- pytrends
- feedparser
- requests
- beautifulsoup4

---

## 📌 備註

- PTT 需帶上 `cookies={'over18': '1'}` 才能避免 18 禁跳轉
- YouTube 熱門頁為 JavaScript 載入，不適合簡單爬蟲（建議 Selenium）
- 可擴充 Mobile01、ETtoday、Instagram 熱門貼文

---

## 📬 聯絡方式

若需進一步整合部署、語音轉換、Google Sheets 紀錄功能，可與我聯繫。
