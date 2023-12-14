import tkinter as tk
import timeset 


#×で閉じられないようにする関数
def click_close():
    pass

def pass_open():
    timeset.value_check(passset_text,warning_pass_label)
    #数値の入力方式が正しいか判定
    if timeset.value_check(passset_text,warning_pass_label) == True:
        input_pass = passset_text.get()
        
        # password.txtを読み込んでパスワードを取得
        f = open('password.txt', 'r')
        password = f.read()
        f.close()
        # パスワードが一致したら終了
        if input_pass == password:
            passbox_form.destroy()
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
    
    #×で閉じられないようにする
    passbox_form.protocol("WM_DELETE_WINDOW", click_close)
    
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