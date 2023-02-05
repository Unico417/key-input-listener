import sys

from pynput import keyboard
from pynput.keyboard import Key
import tkinter as tk

# debug
from pprint import pprint

# TODO:
# 入力履歴を dict
# キーとラベルオブジェクトを同時に管理
# ラベルの描画・削除

WIDTH = 400
HEIGHT = 600
X = 0
Y = 1080 - HEIGHT

class KeyInputViewer(tk.Tk):
    def __init__(self):
        ''' コンストラクタ '''
        super().__init__()
        self.input_history = []
        self.labels = []
        self.font = ('Meiryo', 30)
        # キー入力リスナーを起動
        self.keyboard = keyboard.Listener(
            on_press=self.pressed,
            on_release=self.released
        )
        self.keyboard.start()
        # Tkinter (GUI)
        self.geometry(f'{WIDTH}x{HEIGHT}+{X}+{Y}')
        self.overrideredirect(True) # ボーダレスウィンドウ
        # 背景色を透明
        # 'white' --> 透明
        self.configure(background='white')
        self.wm_attributes('-transparentcolor', 'white')

    def pressed(self, key):
        ''' キー押下時に呼び出されるメソッド '''
        history = list(self.input_history)
        font = self.font
        # 押されたキーが履歴にあればスキップ
        history_keys = [ h for h in history]
        if key in history_keys:
            return
        # キーを履歴に残す
        history.append(key)
        # 重複キーがあれば削除（順序保持）
        self.input_history = tuple(sorted(set(history), key=history.index))
        # ラベルを作成
        label = tk.Label(self, text=key, font=font, background='white')
        label.place(x=100, y=100)
        print(f'\r{self.input_history}', end=' '*10)

    def released(self, key):
        ''' キー引戻時に呼び出されるメソッド '''
        # 履歴から離されたキーを削除
        histories = list(self.input_history)
        for n, history in enumerate(self.input_history):
            if key == history:
                histories.pop(n)
        self.input_history = tuple(sorted(set(histories), key=histories.index))
        print(f'\r{self.input_history}          ')
        # 重複キーがあれば削除（順序保持）
        if key in (Key.pause,):
            self.quit()

    def quit(self):
        ''' 終了 '''
        self.keyboard.stop()
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = KeyInputViewer()
    app.mainloop()
