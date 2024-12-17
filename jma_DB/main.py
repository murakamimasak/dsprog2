import flet as ft
import requests
import sqlite3
import os
import json

# --- APIエンドポイント ---
FORECAST_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# --- SQLiteデータベースの初期化 ---
DB_PATH = "weather_forecast.db"

def init_db():
    """データベースとテーブルを初期化"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_forecast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_code TEXT NOT NULL,
            date_time TEXT NOT NULL,
            weather TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- 天気情報をAPIから取得し、DBに保存 ---
def fetch_and_store_weather(area_code):
    """APIから天気情報を取得し、データベースに保存"""
    try:
        url = FORECAST_URL_TEMPLATE.format(area_code=area_code)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        weather_data = response.json()

        # 天気情報の解析
        time_series = weather_data[0]["timeSeries"][0]
        times = time_series["timeDefines"]
        areas = time_series["areas"][0]["weathers"]

        # データベースに保存
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for i, time in enumerate(times):
            cursor.execute(
                "INSERT INTO weather_forecast (area_code, date_time, weather) VALUES (?, ?, ?)",
                (area_code, time, areas[i]),
            )

        conn.commit()
        conn.close()
        print("天気情報をデータベースに保存しました。")

    except Exception as e:
        print(f"エラー: {e}")

# --- DBから天気情報を取得 ---
def get_weather_from_db(area_code):
    """データベースから天気情報を取得"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date_time, weather FROM weather_forecast WHERE area_code = ?",
        (area_code,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

# --- アプリケーションUI ---
def main(page: ft.Page):
    page.title = "天気予報アプリ (DB版)"
    page.padding = 20

    # UIコンポーネント
    area_code_input = ft.TextField(label="地域コード", width=300)
    fetch_button = ft.ElevatedButton(text="天気を取得・保存")
    weather_list_view = ft.ListView(expand=True, spacing=10)

    # 天気情報取得と表示
    def fetch_and_display_weather(e):
        area_code = area_code_input.value.strip()
        if not area_code:
            page.snack_bar = ft.SnackBar(ft.Text("地域コードを入力してください！"))
            page.snack_bar.open = True
            page.update()
            return

        # 天気情報取得＆DB保存
        fetch_and_store_weather(area_code)

        # DBからデータ取得
        weather_data = get_weather_from_db(area_code)
        weather_list_view.controls.clear()
        for date_time, weather in weather_data:
            weather_list_view.controls.append(ft.Text(f"{date_time} - {weather}"))
        page.update()

    # ボタンイベント
    fetch_button.on_click = fetch_and_display_weather

    # UIレイアウト
    page.add(
        ft.Column(
            [
                ft.Row([area_code_input, fetch_button]),
                ft.Text("天気予報一覧:", size=16, weight="bold"),
                weather_list_view,
            ]
        )
    )

# データベース初期化とアプリ起動
if __name__ == "__main__":
    init_db()
    ft.app(target=main)
