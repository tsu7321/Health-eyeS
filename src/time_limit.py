import tkinter as tk
import time
#ファイルをインポート
import setting
#グローバル変数をセット
import end_flg_value as gend # 終了フラグ 0:継続 1:終了(flg)
import time_count_value as gtime_cnt # 時間計測のカウント (val)
import time_count_flg as gtime_flg # 計測フラグ 0:時間計測中 1:時間計測終了 (flg)

#ファイル単体で実行する用初期化関数
def global_set():
    time_limit_count = 0
    gtime_cnt.val = 0
    gend.flg = 0
    gtime_flg.flg = 1

#×で閉じられないようにする関数
def click_close():
    pass

# 時間を計測する関数
def clock():
    time_limit_count = 0
    while gtime_flg.flg == 0:
        time.sleep(1)
        time_limit_count += 1
        gtime_cnt.val = time_limit_count
        print(time_limit_count)
        # 経過時間ラベルの更新
        setting.limit_label_update()
    gtime_flg.flg = 1
    # 時間計測終了
    time_limit_count = 0
    print("時間計測を終了しました")
    # time_label.config(text="時間です")

    # if time_limit_count > 0:
    #     # lambdaを使って引数を渡す
    #     after(1000, lambda: clock(time_limit_count))
    # if gend.flg == 1:
    #     time_limit.destroy()



# def apli_end_click(time_limit):
#     gend.flg = 1
#     # print("endflg:%d" % gend.flg)
    
#time_,limitを終了する関数
# def time_limit_end():
#     print("時間制限のウインドウを閉じました")
#     time_limit.quit()

# def time_lim():
#     global time_limit
#     # メインウィンドウ
#     time_limit = tk.Tk()
#     time_limit.geometry('250x200')
#     time_limit.title('時間計測')
#     #×で閉じられないようにする
#     time_limit.protocol("WM_DELETE_WINDOW", click_close)
#     # 終了ボタン
#     apli_end_btn = tk.Button(text='終了', command=lambda: apli_end_click(time_limit))
#     apli_end_btn.pack()
#     #カウント開始
#     time_limit_count = 0
#     time_label = tk.Label(text=time_limit_count)
#     time_label.pack()
#     # clock関数を呼び出す
#     clock(time_limit, time_limit_count, time_label)

    # time_limit.mainloop()
if __name__ == '__main__':
    global_set()
    clock()
