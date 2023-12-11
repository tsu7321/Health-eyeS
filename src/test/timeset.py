# tkinterのimport
import tkinter as tk
# 時間表示

# ボタンを押したときの判定


def settimebutton_push():
    # 数字の判定
    if int(timeset_text.get()) > 0:
        # フォームを閉じる
        time_form.destroy()
    else:
        return

# 数値のみ


def on_validate(d, i, P, s, S, v, V, W):
    # Pが数字の場合はTrue、それ以外はFalse
    return P.isdigit() and len(P) <= 4


# フォームの生成
def timeset_task():
    # グローバル変数で宣言
    global time_form
    global timeset_text
    # 時間入力のform
    time_form = tk.Tk()

    # ウィンドウのサイズ
    time_form.geometry('250x200')
    # ウィンドウの大きさ固定
    time_form.resizable(width=False, height=False)

    # 画面のタイトル
    time_form.title('時間を設定')

    # フォームのラベル
    timeset_label = tk.Label(text='時間を入力してください(分)')
    timeset_label.place(x=30, y=50)

    # 入力の制限
    validation = time_form.register(on_validate)

    # 入力のテキストボックス
    timeset_text = tk.Entry(time_form, validate="key", validatecommand=(
        validation, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
    timeset_text.place(x=30, y=70)

    # 入力決定のボタン
    timeset_button = tk.Button(
        time_form,
        text='設定',
        command=settimebutton_push
    ).place(x=100, y=150)

    # フォームのループ
    time_form.mainloop()