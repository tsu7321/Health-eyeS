# tkinterのimport
import tkinter as tk
#グローバル変数をセット
import time_limit_value as glimit

# 時間表示
#×で閉じられないようにする関数
def click_close():
    pass

#入力内容確認の関数
def value_check(entry_text,warning_label):
    # 数字の判定
    if entry_text.get().isdigit():
        return True
    else:
        warning_label.config(text='数字を入力してください' )
        return
    # 桁数の判定
    if len(entry_text.get()) > 4:
        warning_label.config(text='%sは4桁以内で入力してください' % entry_text.get())
        return

# ボタンを押したときの判定
def settimebutton_push(warning_time_label,warning_pass_label):
    # 数字の判定
    # if timeset_text.get() == "":
    # warning_label.configer(text="数値を入力してください")
    
    #数値の入力方式が正しいか判定
    if value_check(timeset_text,warning_time_label) == True and value_check(passset_text,warning_pass_label) == True:
    # if int(timeset_text.get()) > 0:
        glimit.val = int(timeset_text.get())
        gpass = int(passset_text.get())
        print("timeset:%d" % glimit.val)
        print("passset:%d" % gpass)
        # フォームを閉じる
        time_form.destroy()
        
        f = open('password.txt', 'w')
        f.write(str(gpass))
        f.close()
    else:
        return

# 数値のみ


def on_validate_time(d, i, P, s, S, v, V, W):
    # Pが数字の場合はTrue、それ以外はFalse
    return (P.isdigit() and len(P) <= 4) or P == ""

def on_validate_pass(d, i, P, s, S, v, V, W):
    # Pが数字の場合はTrue、それ以外はFalse
    return (P.isdigit() and len(P) <= 4) or P == ""



# フォームの生成
def timeset_task():
    # グローバル変数で宣言
    global time_form
    global timeset_text
    global passset_text
    # 時間入力のform
    time_form = tk.Tk()

    # ウィンドウのサイズ
    time_form.geometry('250x200')
    # ウィンドウの大きさ固定
    time_form.resizable(width=False, height=False)

    # 画面のタイトル
    time_form.title('時間を設定')
    
    #×で閉じられないようにする
    time_form.protocol("WM_DELETE_WINDOW", click_close)

    # フォームの制限時間入力ラベル
    timeset_label = tk.Label(text='時間を入力してください(分)')
    timeset_label.pack()

    # 入力の制限
    validation_time = time_form.register(on_validate_time)
    validation_pass = time_form.register(on_validate_pass)


    # 制限時間入力のテキストボックス
    timeset_text = tk.Entry(time_form, validate="key", validatecommand=(
        validation_time, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
    timeset_text.pack()
    
    # フォームのパスワード設定ラベル
    timeset_label = tk.Label(text='パスワードを設定してください(半角数字4桁)')
    timeset_label.pack()
    
    # パスワード入力のテキストボックス
    passset_text = tk.Entry(time_form, validate="key", validatecommand=(
        validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
    passset_text.pack()

    #警告ラベル
    warning_time_label = tk.Label(text='')
    warning_time_label.pack()
    
    warning_pass_label = tk.Label(text='')
    warning_pass_label.pack()

    
    # 入力決定のボタン
    timeset_button = tk.Button(
        time_form,
        text='設定',
        command=lambda: settimebutton_push(warning_time_label,warning_pass_label)
    ).pack()

    # フォームのループ
    time_form.mainloop()

if __name__ == '__main__':
    timeset_task()