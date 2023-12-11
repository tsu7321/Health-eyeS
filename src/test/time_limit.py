import tkinter as tk
import time
# import threading

#時間を計測する関数-----------------------------------------------------------
def clock():
    global time_limit_count
    global time_label
    #1秒ごとにカウントを増やす
    time_limit_count += 1
    print(time_limit_count)
    #ラベルの表示を更新する
    time_label.config(text=time_limit_count)
    if time_limit_count > 0:
        time_limit.after(1000, clock)
#----------------------------------------------------------------------------
def time_lim():
    if __name__ == '__main__':
        time_limit = tk.Tk()
        time_limit.geometry('250x200')
        time_limit.title('時間計測')

        #起動してから経過した時間を表示する
        time_limit_count = 0
        #時間を計測して表示する
        time_start = time.perf_counter()
        time_label = tk.Label(text=time_limit_count)
        time_label.pack()
        # #時間を計測する関数-----------------------------------------------------------
        # def clock():
        #     global time_limit_count
        #     global time_label
        #     while True:
        #         #1秒ごとにカウントを増やす
        #         time.sleep(1)
        #         time_limit_count += 1
        #         print(time_limit_count)
        #         #ラベルの表示を更新する
        #         time_label.config(text=time_limit_count)
        # #----------------------------------------------------------------------------

        #マルチスレッドでclockを実行する
        # def update_time_label():
        #     time_label.config(text=time_limit_count)
        #     time_limit.after(1000, update_time_label)

        # # # 初回呼び出し
        # # update_time_label()
        # thread1 = threading.Thread(target=clock)
        # thread1.start()
        clock()
        time_limit.mainloop()