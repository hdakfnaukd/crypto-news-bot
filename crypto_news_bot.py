#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
from datetime import datetime
import google.genai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_crypto_news():
    prompt = """あなたは経済ニュースサイトです。最近の重要な仮想通貨ニュースを5つ挙げて下さい。

出力形式：
【日付】YYYY-MM-DD
【タイトル】タイトル
内容：内容
市場の影響度：★★★★★

その後、以下も追加：
【現在、市場参加者が特に注目しているテーマ】
- テーマ1
- テーマ2
- テーマ3

【今後数日で注目すべきイベント】
- イベント1
- イベント2
- イベント3"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"エラー: {e}")
        return None

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload )
        return response.status_code == 200
    except Exception as e:
        print(f"エラー: {e}")
        return False

def main():
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not GEMINI_API_KEY or not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ 環境変数が不足しています")
        return False
    
    print("📰 ニュースを生成中...")
    news = generate_crypto_news()
    
    if not news:
        print("❌ ニュース生成失敗")
        return False
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"🔔 *仮想通貨ニュース速報*\n📅 {timestamp}\n━━━━━━━━━━━━━━━━━━━━━━\n\n{news}\n\n━━━━━━━━━━━━━━━━━━━━━━\n📊 毎日自動配信中"
    
    print("📤 Telegramに送信中...")
    if send_to_telegram(message):
        print("✅ 完了")
        return True
    else:
        print("❌ 失敗")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
