import tkinter as tk
from tkinter import messagebox
import threading
import time
#ファイルをインポート
import time_limit
import password_input
#グローバル変数
import end_flg_value as gend # 終了フラグ 0:継続 1:終了(flg)
import time_count_value as gtime_cnt # 時間計測のカウント(val)
import time_count_flg as gtime_flg # 計測フラグ 0:時間計測中 1:時間計測終了(flg)
import pass_sec_value as gpass_sec  # パスワードが解かれたか 0:ロック 1:解除 (flg)
import restart_flg as grestart_flg # 再起動フラグ 0:再起動待機 1:再起動 (flg)



# ファイル単体で実行する用初期化関数
def global_set():
    gend.flg = 0
    gtime_cnt.val = 0
    gtime_flg.flg = 1
    gpass_sec.flg = 0
    grestart_flg.flg = 0    # 再起動フラグ 0:再起動待機 1:再起動 (flg)

def time_start_click():
    f = open('src/limit.txt', 'r')
    f_limit = int(f.read())
    f.close()

    if gtime_cnt.val >= f_limit:
        messagebox.showinfo('警告','制限時間を過ぎています')
    else:
        if gtime_flg.flg == 1:
            gtime_flg.flg = 0   #計測する
            # thread_time_start = threading.Thread(target=time_limit.clock)
            thread_time_start = threading.Thread(target=clock)
            thread_time_start.start()
            # time_limit.clock()
            print("計測開始")
        
def time_stop_click():
    if gtime_flg.flg == 0:
        gtime_flg.flg = 1   #計測を止める
        # print("計測停止")


# 時間を計測する関数
def clock():
    
    # time_limit_count = 0
    while gtime_flg.flg == 0:
        f = open('src/limit.txt', 'r')
        f_limit = int(f.read())
        f.close()
        
        # 制限時間を過ぎたとき
        if gtime_cnt.val >= f_limit:
            gtime_flg.flg = 1
            break
        elif gend.flg == 1:
            gtime_flg.flg = 1
            print("thread_time_startを終了しました")
            break

        # time_limit_count += 1
        # gtime_cnt.val = time_limit_count
        gtime_cnt.val += 1
        print(gtime_cnt.val)
        # 経過時間ラベルの更新
        # limitlablがないときの例外処理
        try:
            limit_label_update()
        except NameError:
            pass
        time.sleep(1)
    # 制限時間を過ぎたとき
    if gtime_cnt.val >= f_limit:
        #パスワードを再取得
        fp = open('src/password.txt', 'r')
        f_password = fp.read()
        fp.close()
        # 時間計測終了
        # time_limit_count = 0
        # gtime_cnt.val = 0
        #メッセージを表示
        messagebox.showinfo('時間制限','制限時間を超えました')

        print("時間計測を終了しました")
        if f_password =="":
            print("パスワード認証をスキップ")
        else:
            password_input.passbox()
    else:
        print("計測停止")
    
def limit_label_update():
    global limit_label
    # 経過時間ラベルの更新
    limit_label.config(text='経過時間:%d' % gtime_cnt.val)

def setting():
    
    def setting_end():
        #パスワードを再取得
        fp = open('src/password.txt', 'r')
        f_password = fp.read()
        fp.close()
        #パスワードを設定していないなら
        if f_password =="":
            print("パスワード認証をスキップ")
            gend.flg = 1 #終了フラグを立てる
            print("設定のウインドウを閉じました")
            setting_form.quit()
        else:
        # print(gpass_sec.flg)
            password_input.passbox()
        if gpass_sec.flg == 1:
            gend.flg = 1 #終了フラグを立てる
            print("設定のウインドウを閉じました")
            setting_form.quit()

#内容確認関連の関数-----------------------------------------------------------------
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
        
    # 数値のみ入力を受け付ける処理
    def on_validate(d, i, P, s, S, v, V, W):
        # Pが数字の場合はTrue、それ以外はFalse
        return (P.isdigit() and len(P) <= 4) or P == ""
#----------------------------------------------------------------------------------

#ボタンクリック関連の関数------------------------------------------------------------
    # パスワード設定ボタンを押したときの処理
    def password_set_click():
        def pass_dicide_click():
            # パスワードを取得
            password = pass_entry.get()
            # パスワードをpassword.txtに保存
            f = open('src/password.txt', 'w')
            f.write(str(password))
            f.close()
            
            #空白なら警告
            if password == '':
                #メッセージを表示
                messagebox.showinfo('パスワード設定','パスワードなしで設定しました')
            else:
                #メッセージを表示
                messagebox.showinfo('パスワード設定','パスワードを設定しました')
            # メッセージのOKボタンを押したらウインドウを閉じる
            if messagebox.OK:
                pass_win.destroy()
            
            
        pass_win = tk.Toplevel()
        pass_win.title('パスワード設定')
        pass_win.geometry('400x300')
        # モーダルダイアログにする
        pass_win.grab_set()
        # パスワード設定ラベル
        dic_label = tk.Label(pass_win,text='パスワードを設定してください(半角数字4桁)')
        dic_label.place(x=0,y=0)
        
        validation_pass = pass_win.register(on_validate)
        # パスワード入力のテキストボックス
        pass_entry = tk.Entry(pass_win, validate="key", validatecommand=(
            validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        pass_entry.pack()
        #警告ラベル
        warning_label = tk.Label(pass_win,text='')
        warning_label.place(x=0,y=40)
        #決定ボタン
        pass_decide_btn = tk.Button(pass_win,text='決定',command=lambda:pass_dicide_click())
        pass_decide_btn.place(x=0,y=60)
        
    def limit_set_click():
        def limit_dicide_click():
            # パスワードを取得
            limit = limit_entry.get()
            #空白なら警告
            if limit == '':
                messagebox.showinfo('制限時間設定','制限時間を設定してください(分)')
                #limit_winを最前面へ
                limit_win.lift()
                return
            else:
                #分
                # limit_minut = int(limit) * 60
                #秒
                limit_minut = int(limit)
                # 制限時間をlimit.txtに保存
                f = open('src/limit.txt', 'w')
                f.write(str(limit_minut))
                f.close()
                #メッセージを表示
                messagebox.showinfo('制限時間設定','制限時間を設定しました')
                # メッセージのOKボタンを押したらウインドウを閉じる
                if messagebox.OK:
                    limit_win.destroy()
            
        
        limit_win = tk.Toplevel()
        limit_win.title('制限時間設定')
        limit_win.geometry('400x300')
        # モーダルダイアログにする
        limit_win.grab_set()

        # 制限時間設定ラベル
        dic_label = tk.Label(limit_win,text='制限時間を設定してください(半角数字4桁)')
        dic_label.place(x=0,y=0)
        
        validation_pass = limit_win.register(on_validate)
        # 制限時間入力のテキストボックス
        limit_entry = tk.Entry(limit_win, validate="key", validatecommand=(
            validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        limit_entry.pack()
        #警告ラベル
        warning_label = tk.Label(limit_win,text='')
        warning_label.place(x=0,y=40)
        #決定ボタン
        limit_decide_btn = tk.Button(limit_win,text='決定',command=lambda:limit_dicide_click())
        limit_decide_btn.place(x=0,y=60)
    
    
    def app_restart_click():
        grestart_flg.flg = 1
        print("thread_time_startを終了しました")
#----------------------------------------------------------------------------------
    global limit_label
    global f_limit
    global f_password
    f = open('src/limit.txt', 'r')
    f_limit = int(f.read())
    f.close()
    
    fp = open('src/password.txt', 'r')
    f_password = fp.read()
    fp.close()
    
    # メインウィンドウ
    setting_form = tk.Tk()
    form_x = 500
    form_y = form_x * 3 / 4
    setting_form.geometry('%dx%d' % (form_x, form_y))
    setting_form.title('設定画面')
    #フレームの作成
    setting_frame = tk.Frame(setting_form,width=form_x,height=form_y)
    
    # パスワード設定
    password_set_label = tk.Label(setting_frame,text='パスワードを設定できます')
    password_set_btn = tk.Button(setting_frame,text='パスワード設定',command=lambda:password_set_click())
    #制限時間の設定
    limit_set_label = tk.Label(setting_frame,text='制限時間を設定できます')
    limit_set_btn = tk.Button(setting_frame,text='制限時間設定',command=lambda:limit_set_click())
    #経過時間
    limit_label = tk.Label(setting_frame,text='経過時間:-')
    #計測開始ボタン
    time_start_btn = tk.Button(setting_frame,text='計測開始',command=lambda:time_start_click())
    #計測停止ボタン
    time_stop_btn = tk.Button(setting_frame,text='計測停止',command=lambda:time_stop_click())
    #再起動ボタン
    app_restart_btn = tk.Button(text='アプリを再起動',command=lambda:app_restart_click())
    #終了ボタン
    app_end_btn = tk.Button(text='アプリを終了',command=lambda:setting_end())

    # パスワード設定の配置
    password_set_label.place(x=0,y=0)
    password_set_btn.place(x=200,y=0)
    # 制限時間設定の配置
    limit_set_label.place(x=0,y=30)
    limit_set_btn.place(x=200,y=30)
    # 経過時間ラベルの配置
    limit_label.place(x=form_x*(7/10),y=form_x*(7/10))
    # 計測開始ボタンの配置
    time_start_btn.place(x=120,y=60)
    # 計測停止ボタンの配置
    time_stop_btn.place(x=120,y=100)
    # 再起動ボタンの配置
    app_restart_btn.place(x=180,y=120)
    # 終了ボタンの配置
    app_end_btn.place(x=0,y=60)
    
    setting_frame.pack()


    setting_form.mainloop()
    
if __name__ == '__main__':
    global_set()
    # setting()
    thread1 = threading.Thread(target=setting)
    thread1.start()
    
    
    
