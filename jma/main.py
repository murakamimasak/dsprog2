import flet as ft
import requests
import json
import os

# --- APIエンドポイント ---
AREA_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

# --- 天気情報取得用のヘッダー ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# --- 地域リスト取得関数 ---
def fetch_area_data():
    """気象庁APIから地域データを取得"""
    try:
        response = requests.get(AREA_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"地域データ取得エラー: {e}")
        return None

# --- 天気情報取得関数 ---
def fetch_weather(area_code):
    """指定された地域コードで天気情報を取得"""
    try:
        url = FORECAST_URL_TEMPLATE.format(area_code=area_code)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"天気情報取得エラー: {e}")
        return None

# --- アプリのメイン関数 ---
def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.window_width = 900
    page.window_height = 700
    page.padding = 20

    # UI用コンポーネント
    area_list_view = ft.ListView(expand=True, spacing=10)
    weather_info_view = ft.Column(spacing=10, expand=True)
    status_text = ft.Text("地域データを取得中...", size=14)

    # 地域データ読み込み関数
    def load_area_data():
        status_text.value = "地域データを取得中..."
        page.update()

        area_data = fetch_area_data()
        if area_data:
            area_list_view.controls.clear()
            for center_id, center_info in area_data["centers"].items():
                area_list_view.controls.append(
                    ft.ExpansionTile(
                        title=ft.Text(center_info["name"]),
                        controls=[
                            ft.ListTile(
                                title=ft.Text(f"地域コード: {child}"),
                                on_click=lambda e, code=child: display_weather(code),
                            )
                            for child in center_info["children"]
                        ],
                    )
                )
            status_text.value = "地域データ取得完了！"
        else:
            status_text.value = "地域データの取得に失敗しました。"
        page.update()

    # 天気情報表示関数
    def display_weather(area_code):
        status_text.value = f"{area_code} の天気情報を取得中..."
        page.update()

        weather_data = fetch_weather(area_code)
        weather_info_view.controls.clear()

        if weather_data:
            time_series = weather_data[0]["timeSeries"][0]  # 天気情報の部分
            times = time_series["timeDefines"]
            areas = time_series["areas"][0]["weathers"]

            weather_info_view.controls.append(ft.Text(f"地域コード: {area_code}", size=16, weight="bold"))
            for i, time in enumerate(times):
                weather_info_view.controls.append(
                    ft.Text(f"{time} の天気: {areas[i]}", size=14)
                )
        else:
            weather_info_view.controls.append(ft.Text("天気情報の取得に失敗しました。", color="red"))

        status_text.value = "天気情報取得完了！"
        page.update()

    # UIレイアウト
    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.NavigationRail(
                        expand=True,
                        destinations=[
                            ft.NavigationRailDestination(
                                icon=ft.icons.LOCATION_ON, label="地域リスト"
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.CLOUD, label="天気情報"
                            ),
                        ],
                        selected_index=0,
                        on_change=lambda e: load_area_data(),
                    ),
                    expand=1,
                ),
                ft.VerticalDivider(),
                ft.Container(content=area_list_view, expand=2),
                ft.VerticalDivider(),
                ft.Container(content=weather_info_view, expand=3),
            ],
            expand=True,
        ),
        ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
    )

    # 初期読み込み
    load_area_data()

# アプリ起動
if __name__ == "__main__":
    ft.app(target=main)
