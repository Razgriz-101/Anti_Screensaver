import pyautogui
import tkinter as tk


class App(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.master.title('Anti Screensaver')  # タイトル
        self.master.geometry("500x200")  # ウィンドウサイズを「500*200」に設定
        self.master.propagate(0)  # ウィンドウがウィジェットに合わせて小さくなることを禁止

        # BASE64でタイトルアイコンを挿入
        path = r"E:\Anti_Screensaver.txt"
        with open(path, 'r') as f:
            icon = f.read()
        self.master.iconphoto(False, tk.PhotoImage(data=icon))

        self.anti_s_state = 0  # アンチスクリーンセーバーの作動状態を保持

        # ラベルの変数
        self.label_text_list = ["Anti Screensaver is Disable\n", "Anti Screensaver is Enable\n"]
        self.label_text = tk.StringVar()
        self.label = tk.Label(self.master, textvariable=self.label_text)

        # ボタンの変数
        self.button_text_list = ["Turn ON", "Turn OFF"]
        self.button_text = tk.StringVar()
        self.button = tk.Button(self.master, textvariable=self.button_text, bg='#ffffff', activebackground='#dddddd')

        # ウィジェット作成
        self.create_widgets()

    def create_widgets(self):

        # ラベルの配置
        self.label_text.set(self.label_text_list[self.anti_s_state])
        self.label.pack(pady=25)  # Y軸のパッディングを25ピクセルに設定

        # ボタンウィジェットをメインウィンドウに配置、イベントを登録
        self.button_text.set(self.button_text_list[self.anti_s_state])
        self.button.bind("<Button-1>", self.switcher)  # ボタンが押されたら「switcher」を実行
        self.button.pack(after=self.label)

    def switcher(self, event):  # 「anti_s_state」の値を変更、それにともなってラベルとボタンのテキストを更新
        self.anti_s_state = (self.anti_s_state + 1) % 2
        self.label_text.set(self.label_text_list[self.anti_s_state])
        self.button_text.set(self.button_text_list[self.anti_s_state])

        if self.anti_s_state == 1:  # 「anti_s_state」が「1」の時「anti_screensaver」を実行
            self.anti_screensaver()

    def anti_screensaver(self):

        if self.anti_s_state == 1:
            try:
                # キーボードのスクロールロックを押した時の信号を送る
                pyautogui.PAUSE = 0
                pyautogui.keyDown('scrolllock')  # Scroll lock 'On'
                pyautogui.keyUp('scrolllock')

                pyautogui.keyDown('scrolllock')  # Scroll lock 'Off'
                pyautogui.keyUp('scrolllock')

                return self.master.after(5000, self.anti_screensaver)  # 5秒ごとに同じ処理を実行

            except pyautogui.FailSafeException:  # フェイルセーフ（マウスポインターを「X:0, Y:0」へ動かすことで実行される）

                # [anti_s_state」を初期化、ラベルにフェイルセーフが実行されたことを表示、ボタンのテキストを「Turn ON」に変更
                self.anti_s_state = 0
                self.label_text.set("Fail-safe executed\nAnti Screensaver : OFF")
                self.button_text.set(self.button_text_list[self.anti_s_state])


if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
