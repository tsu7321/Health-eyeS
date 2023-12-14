import tkinter as tk
import time
#グローバル変数をセット
import end_flg_value as gend
import time_count_value as gtime_cnt
import time_count_flg as gtime_flg
import sys


gend.flg = 0

#×で閉じられないようにする関数
def click_close():
    pass

# 時間を計測する関数
def clock(time_limit, time_limit_count, time_label):

    if gtime_flg.flg == 0:
        time_limit_count += 1
        gtime_cnt.val = time_limit_count
        print(time_limit_count)
        # カウントラベルを更新
        time_label.config(text=time_limit_count)
    else:
        time_limit_count = 0
        time_label.config(text="時間です")

    if time_limit_count > 0:
        # lambdaを使って引数を渡す
        time_limit.after(1000, lambda: clock(time_limit, time_limit_count, time_label))
    # if gend.flg == 1:
    #     time_limit.destroy()



def apli_end_click(time_limit):
    gend.flg = 1
    # print("endflg:%d" % gend.flg)
    
#time_,limitを終了する関数
def time_limit_end():
    print("ウインドウを閉じました")
    time_limit.quit()

def time_lim():
    global time_limit
    # メインウィンドウ
    time_limit = tk.Tk()
    time_limit.geometry('250x200')
    time_limit.title('時間計測')
    #×で閉じられないようにする
    time_limit.protocol("WM_DELETE_WINDOW", click_close)
    # 終了ボタン
    apli_end_btn = tk.Button(text='終了', command=lambda: apli_end_click(time_limit))
    apli_end_btn.pack()
    #カウント開始
    time_limit_count = 0
    time_label = tk.Label(text=time_limit_count)
    time_label.pack()
    # clock関数を呼び出す
    clock(time_limit, time_limit_count, time_label)
    
    time_limit.mainloop()
if __name__ == '__main__':
    time_lim()
