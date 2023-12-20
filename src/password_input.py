import tkinter as tk
import timeset
#グローバル変数をセット
import pass_sec_value as gpass_sec  # パスワードが解かれたか 0:ロック 1:解除 (flg)
import end_flg_value as gend        # 終了フラグ 0:継続 1:終了(flg)

#×で閉じられないようにする関数
def click_close():
    pass

def passbox_end():
    print("パスワードのウインドウを閉じました")
    passbox_form.quit()

def pass_open():
    timeset.value_check(passset_text,warning_pass_label)
    #数値の入力方式が正しいか判定
    if timeset.value_check(passset_text,warning_pass_label) == True:
        # 入力されたパスワードを取得(int変換)
        input_pass = int(passset_text.get())
        
        # password.txtを読み込んでパスワードを取得
        f = open('src/password.txt', 'r')
        password = int(f.read())
        f.close()
        # パスワードが一致したら終了
        if input_pass == password:
            gpass_sec.flg = 1
            passbox_form.quit()
        else:
            warning_pass_label.config(text='パスワードが違います')
    else:
        return


def passbox():
    global passbox_form
    global passset_text
    global warning_pass_label
    passbox_form = tk.Tk()
    passbox_form.geometry('250x200')
    passbox_form.title('パスワードを入力してください')
    
    # #×で閉じられないようにする
    # passbox_form.protocol("WM_DELETE_WINDOW", click_close)
    
    # フォームのパスワード設定ラベル
    pass_label = tk.Label(text='パスワードを設定してください(半角数字4桁)')
    pass_label.pack()
    # 入力の制限
    validation_pass = passbox_form.register(timeset.on_validate_pass)

    # パスワード入力のテキストボックス
    passset_text = tk.Entry(passbox_form, validate="key", validatecommand=(
        validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
    passset_text.pack()
    
    warning_pass_label = tk.Label(passbox_form,text='')
    warning_pass_label.pack()

    # 入力決定のボタン
    timeset_button = tk.Button(
        passbox_form,
        text='決定',
        command=lambda: pass_open()
    ).pack()
    
    
    passbox_form.mainloop()

if __name__ == '__main__':
    passbox()