import flet as ft
import math

# ボタンのクラス（ここでは電卓のボタンを定義）
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text

# 電卓アプリケーション
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        CalcButton(text="AC", button_clicked=self.button_clicked),
                        CalcButton(text="+/-", button_clicked=self.button_clicked),
                        CalcButton(text="%", button_clicked=self.button_clicked),
                        CalcButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        CalcButton(text="7", button_clicked=self.button_clicked),
                        CalcButton(text="8", button_clicked=self.button_clicked),
                        CalcButton(text="9", button_clicked=self.button_clicked),
                        CalcButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        CalcButton(text="4", button_clicked=self.button_clicked),
                        CalcButton(text="5", button_clicked=self.button_clicked),
                        CalcButton(text="6", button_clicked=self.button_clicked),
                        CalcButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        CalcButton(text="1", button_clicked=self.button_clicked),
                        CalcButton(text="2", button_clicked=self.button_clicked),
                        CalcButton(text="3", button_clicked=self.button_clicked),
                        CalcButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        CalcButton(text="0", expand=2, button_clicked=self.button_clicked),
                        CalcButton(text=".", button_clicked=self.button_clicked),
                        CalcButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
                # 科学計算モードのボタンを追加
                ft.Row(
                    controls=[
                        CalcButton(text="sin", button_clicked=self.scientific_button_clicked),
                        CalcButton(text="cos", button_clicked=self.scientific_button_clicked),
                        CalcButton(text="tan", button_clicked=self.scientific_button_clicked),
                        CalcButton(text="log", button_clicked=self.scientific_button_clicked),
                        CalcButton(text="exp", button_clicked=self.scientific_button_clicked),
                    ]
                ),
            ]
        )

    # 通常の計算ボタンが押されたときの処理
    def button_clicked(self, e):
        data = e.control.data
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data
        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
            self.operator = data
            self.operand1 = float(self.result.value)
            self.new_operand = True
        elif data in ("="):
            self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
            self.reset()
        elif data in ("%"):
            self.result.value = float(self.result.value) / 100
            self.reset()
        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(abs(float(self.result.value)))
        self.update()

    # 科学計算モードボタンが押されたときの処理
    def scientific_button_clicked(self, e):
        data = e.control.data
        try:
            if data == "sin":
                self.result.value = math.sin(math.radians(float(self.result.value)))
            elif data == "cos":
                self.result.value = math.cos(math.radians(float(self.result.value)))
            elif data == "tan":
                self.result.value = math.tan(math.radians(float(self.result.value)))
            elif data == "log":
                self.result.value = math.log(float(self.result.value))
            elif data == "exp":
                self.result.value = math.exp(float(self.result.value))
        except ValueError:
            self.result.value = "Error"
        self.update()

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return operand1 + operand2
        elif operator == "-":
            return operand1 - operand2
        elif operator == "*":
            return operand1 * operand2
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return operand1 / operand2

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

# メイン関数
def main(page: ft.Page):
    page.title = "Calculator App"
    # 電卓アプリのインスタンスを作成
    calc = CalculatorApp()
    # ページにアプリを追加
    page.add(calc)

# アプリを実行
ft.app(target=main)
