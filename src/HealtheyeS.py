# 顔を認識し、カメラから顔(目)までの距離を出す
# 一定間隔おきに距離を出す
# キー入力「0」で即座に距離を出す（精度低）
# キー入力「1」でcmの表記位置変更
# キー入力「Esc」で終了
# 画面サイズ1280,720で計測

# 追加行大体 importでファイルtimesetを追加
# 148
# 194から203ぐらい

# import
import cv2
import sys
import statistics   # 最頻値
import tkinter as tk
import threading
import time
from plyer import notification
import timeset
# ぼかしの処理
import numpy as np
import win32gui
import win32con
import win32ui
import win32api
import ctypes

import timeset
# import time_limit
import setting
#グローバル変数をセット
import end_flg_value as gend # 終了フラグ 0:継続 1:終了(flg)
import time_limit_value as glimit   # 制限時間 (val)
import time_count_value as gtime_cnt    # 時間計測のカウント (val)
import time_count_flg as gtime_flg  # 計測フラグ 0:時間計測中 1:時間計測終了 (flg)
import pass_sec_value as gpass_sec # 入力されたパスワード (val)
import restart_flg as grestart_flg # 再起動フラグ 0:再起動待機 1:再起動 (flg)

import password_input
# import mosaic
# import refreshfream

# --------------------------------------------------------------------------------------------------------
def global_set():
    gtime_cnt.val = 0   # 時間計測のカウント
    gend.flg = 0        # 終了フラグ 0:継続 1:終了
    gtime_flg.flg = 1   # 計測フラグ 0:時間計測中 1:時間計測終了
    gpass_sec.flg = 0   # パスワードが解かれたか 0:ロック 1:解除 (flg)
    grestart_flg.flg = 0    # 再起動フラグ 0:再起動待機 1:再起動 (flg)
    
#再起動する関数
def restart_app():
    global f_limit
    while True:
        
        if grestart_flg.flg == 1:
            #制限時間を更新
            f = open("src/limit.txt", "r")
            f_limit = int(f.read())
            f.close()
            print("制限時間:%d" % f_limit)
            grestart_flg.flg = 0
            print("カメラを再起動しています…")
            
            #時間計測開始
            # setting.time_start_click()

            HealtheyeS(cnt, fwcount, ewcount, fw, ew, disAns, textChange, fx, fy, ex, ey, sampleLen, fwSample, ewSample, MODECOUNT)
        elif gend.flg == 1:
            break

# グローバル変数: オリジナルのデスクトップ画像
original_desktop_image = None
screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) * 2
screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) * 2

# 初回のぼかし処理フラグ
first_mosaic = True

# ウィンドウを非表示にする関数

def hide_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

# ウィンドウを表示にする関数

def show_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)

# ぼかしをかける関数

def mosaic():
    global original_desktop_image, first_mosaic

    # ウィンドウスクリーンのキャプチャ
    hwnd = win32gui.GetDesktopWindow()
    hide_window(hwnd)  # ウィンドウを非表示にする

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, screen_width, screen_height)
    save_dc.SelectObject(save_bitmap)
    save_dc.BitBlt((0, 0), (screen_width, screen_height),
                   mfc_dc, (0, 0), win32con.SRCCOPY)

    # ビットマップから画像データを取得
    bmp_info = save_bitmap.GetInfo()
    bmp_data = save_bitmap.GetBitmapBits(True)
    image_np = np.frombuffer(bmp_data, dtype=np.uint8).reshape(
        screen_height, screen_width, 4)

    # 画像データを保存
    if first_mosaic:
        original_desktop_image = image_np.copy()
        first_mosaic = False

    # 画面全体にぼかしをかける
    blur_kernel_size = (101, 101)
    blurred_image = cv2.GaussianBlur(image_np, blur_kernel_size, 0)

    # デスクトップにぼかしを適用
    img_data = blurred_image.tobytes()
    set_blur(img_data)

    show_window(hwnd)  # ウィンドウを再表示

# ぼかし解除の関数


def unmosaic():
    global original_desktop_image

    if original_desktop_image is not None:
        # 開いているウィンドウを閉じる
        cv2.destroyAllWindows()

        # オリジナルのデスクトップ画像に戻す
        img_data = original_desktop_image.tobytes()
        set_blur(img_data)

# ぼかしをセットする関数


def set_blur(img_data):
    # BITMAPINFOHEADER構造体の作成
    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ("biSize", ctypes.c_uint32),
            ("biWidth", ctypes.c_long),
            ("biHeight", ctypes.c_long),
            ("biPlanes", ctypes.c_short),
            ("biBitCount", ctypes.c_short),
            ("biCompression", ctypes.c_uint32),
            ("biSizeImage", ctypes.c_uint32),
            ("biXPelsPerMeter", ctypes.c_long),
            ("biYPelsPerMeter", ctypes.c_long),
            ("biClrUsed", ctypes.c_uint32),
            ("biClrImportant", ctypes.c_uint32),
        ]

    bmi_header = BITMAPINFOHEADER()
    bmi_header.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi_header.biWidth = screen_width
    bmi_header.biHeight = -screen_height
    bmi_header.biPlanes = 1
    bmi_header.biBitCount = 32
    bmi_header.biCompression = win32con.BI_RGB

    # BITMAPINFO構造体の作成
    class BITMAPINFO(ctypes.Structure):
        _fields_ = [("bmiHeader", BITMAPINFOHEADER),
                    ("bmiColors", ctypes.c_ulong * 3)]

    bmi = BITMAPINFO()
    bmi.bmiHeader = bmi_header

    hdc = win32gui.GetDC(0)
    ctypes.windll.gdi32.SetDIBitsToDevice(
        hdc, 0, 0, screen_width, screen_height,
        0, 0, 0, screen_height, img_data, ctypes.byref(
            bmi), win32con.DIB_RGB_COLORS
    )
    win32gui.ReleaseDC(0, hdc)


# 入力された値(fw,ew)から距離を求める関数--------------------------------------------------------------------


def distance(sampleLen, fwSample, ewSample, fw, ew):
    valuesAbs = []      # 入力された値xと事前に計測された値との絶対値を格納
    cnt = 0             # カウントの役割をする変数
    ans = 0             # 顔と画面との距離を格納
    standard = 90       # ewとfwのどちらを距離算出に使うかの基準数値 (90は50cmのとき)

    if ew >= standard:             # ewが基準値より小さければewを計算に使用
        for i in ewSample:          # ewとの差の絶対値を格納
            valuesAbs.insert(cnt, abs(i - ew))
            cnt += 1

        valuesAbs_sorted = sorted(valuesAbs)        # 絶対値の値たちを昇順にソートして格納

        cnt = 0
        for i in valuesAbs:         # ewに一番近い値（絶対値）の要素番号を見つける
            if i == valuesAbs_sorted[0]:
                break
            cnt += 1

        if ew > ewSample[0]:        # 距離が恐らく10cm以下の場合
            ans = -1
        elif ew == ewSample[cnt]:       # ewとewに最も近い値が等しい場合
            ans = sampleLen[cnt]
        elif ew > ewSample[cnt]:        # ewに最も近い値がewよりも小さい場合
            data1 = abs(ewSample[cnt] - ewSample[cnt-1])        # ewの大きさの差
            data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]
                        ) / data1  # 1cmごとに変化するewの大きさ
            # ewより小さくて最も近い値からどれだけの差があるか
            data3 = abs(ew - ewSample[cnt-1])
            data4 = data2 * data3                               # ewより小さくて最も近い値より何cm離れているか
            # どれだけ画面から離れているか
            ans = sampleLen[cnt-1] + data4
        else:                       # ewに最も近い値がewよりも大きい場合
            data1 = abs(ewSample[cnt] - ewSample[cnt+1])        # ewの大きさの差
            data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]
                        ) / data1  # ewが1増えるごとに何cm増えるか
            # ewより大きくて最も近い値からどれだけの差があるか
            data3 = abs(ew - ewSample[cnt])
            data4 = data2 * data3                               # ewより大きくて最も近い値より何cm離れているか
            # どれだけ画面から離れているか
            ans = sampleLen[cnt] + data4
    else:       # ewが基準値より大きければfwを計算に使用

        for i in fwSample:                      # fwとの差の絶対値を格納
            valuesAbs.insert(cnt, abs(i - fw))
            cnt += 1

        valuesAbs_sorted = sorted(valuesAbs)    # 絶対値の値たちをソート（昇順）を格納

        cnt = 0
        for i in valuesAbs:                     # fwに一番近い値（絶対値）の要素番号を見つける
            if i == valuesAbs_sorted[0]:
                break
            cnt += 1

        if fw < fwSample[len(fwSample)-1]:  # 距離が恐らく70cm以上の場合
            ans = -2
        elif fw == fwSample[cnt]:       # fwとfwに最も近い値が等しい場合
            ans = sampleLen[cnt]
        elif fw > fwSample[cnt]:        # fwに最も近い値がfwよりも小さい場合
            data1 = abs(fwSample[cnt] - fwSample[cnt-1])        # fwの大きさの差
            data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]
                        ) / data1  # 1cmごとに変化するfwの大きさ
            # fwより小さくて最も近い値からどれだけの差があるか
            data3 = abs(fw - fwSample[cnt-1])
            data4 = data2 * data3                               # fwより小さくて最も近い値より何cm離れているか
            # どれだけ画面から離れているか
            ans = sampleLen[cnt-1] + data4
        else:                           # fwに最も近い値がfwよりも大きい場合
            data1 = abs(fwSample[cnt] - fwSample[cnt+1])        # fwの大きさの差
            data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]
                        ) / data1  # fwが1増えるごとに何cm増えるか
            # fwより大きくて最も近い値からどれだけの差があるか
            data3 = abs(fw - fwSample[cnt])
            data4 = data2 * data3                               # fwより大きくて最も近い値より何cm離れているか
            # どれだけ画面から離れているか
            ans = sampleLen[cnt] + data4
    return ans


# ---------------------------------------------------------------------------------------------------------
# 時間の設定のフォーム
# timeset.timeset_task()
global f_limit
global_set()
f = open("src/limit.txt", "r")
f_limit = int(f.read())
f.close()
print("制限時間:%d" % f_limit)


thread_setting = threading.Thread(target=setting.setting)
thread_setting.start()

print("カメラを起動中…")


# カスケード分類器のパスを各変数に代入
# pythonの実行
fase_cascade_path = 'data\haarcascades\haarcascade_frontalface_default.xml'
eye_cascade_path = 'data\haarcascades\haarcascade_eye.xml'
# カスケード分類器の読み込み
face_cascade = cv2.CascadeClassifier(fase_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

# Webカメラの準備（引数でカメラ指定、0は内臓カメラ）
cap = cv2.VideoCapture(0)

FRAME_LINESIZE = 2       # 顔に四角を描画する際の線の太さ
FRAME_RGB_G = (0, 255, 0)  # 四角形を描画する際の色を格納(緑)
FRAME_RGB_B = (255, 0, 0)  # 四角形を描画する際の色を格納(青)
cnt = 0     # カウントの際に使用
textChange = 0  # cmの表記を画面上部に固定にするか、顔に追従するかの切り替え
fw = 100    # 顔の大きさの初期値（起動時エラー回避のため初期値設定）
fx = 100    # 顔のx座標の初期値
fy = 100    # 顔のy座標の初期値
ew = 100    # 目の大きさの初期値
ex = 100    # 目のx座標の初期値
ey = 100    # 目のy座標の初期値
disAns = 0  # 計測した距離を格納
fwcount = []  # fwを一時的に格納（最頻値を出すために使用）
ewcount = []  # ewを一時的に格納（最頻値を出すために使用）
MODECOUNT = 50  # 最頻値を出すときの要素数（この値を変更することで計測値(cm)の正確性と計測にかかる時間が変化）
# fwSample,ewSampleに対応した顔とカメラとの距離(cm)
sampleLen = [10,   15,  20,  30,  40,  50,  60,  70]
fwSample = [999, 999, 999, 999, 431, 348, 292, 253]       # 事前に計測した距離に対応する顔の大きさ
ewSample = [268, 214, 161, 118,  90,  62,  59,  54]       # 事前に計測した距離に対応する目の大きさ

# cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
# cap.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラ画像の縦幅を720に設定
# print cap.get(cv2.CAP_PROP_FPS)
# print cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# print cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


# -----------------------------------------------------------
# もしカメラが起動していなかったら終了する
if cap.isOpened() is False:
    print("カメラが起動していないため終了しました")
    sys.exit()



#時間計測開始
setting.time_start_click()

# 無限ループで読み取った映像に変化を加える（1フレームごとに区切って変化）
# count = 0
def HealtheyeS(cnt, fwcount, ewcount, fw, ew, disAns, textChange, fx, fy, ex, ey, sampleLen, fwSample, ewSample, MODECOUNT):
    while True:
        # count += 1
        ret, frame = cap.read()

        # カラーをモノクロ化したキャプチャを代入(グレースケール化)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔の検出
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

        # 目の検出
        eyes = eye_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

    #デバック-------------------------------------------------
        # # 第1引数   効果を適応する画像
        # # 第2引数   矩形の左上隅の座標
        # # 第3引数   矩形の右下隅の座標
        # # 第4引数   矩形の色
        # # 第5引数   描画する線の太さ（-1以下だと塗りつぶし）
        # # 顔に四角形(矩形)を描画する
        # for (fx, fy, fw, fh) in faces:
        #     cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh),
        #                   FRAME_RGB_G, FRAME_LINESIZE)

        # # 目に四角形(矩形)を描画する
        # for (ex, ey, ew, eh) in eyes:
        #     cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh),
        #                   FRAME_RGB_B, FRAME_LINESIZE)
    # -----------------------------------------------------------
        if cnt < MODECOUNT:
            fwcount.insert(cnt, fw)
            ewcount.insert(cnt, ew)
            cnt += 1
        else:
            cnt = 0
            disAns = distance(sampleLen, fwSample, ewSample,
                            statistics.mode(fwcount), statistics.mode(ewcount))
            if disAns == -1:
                # ぼかしの処理
                mosaic()
                # コマンドライン
                print('10cm以下です!近すぎます!!\n')
            elif disAns == -2:
                # ぼかしの処理
                if f_limit > gtime_cnt.val:
                    unmosaic()
                    print('70cm以上離れています!!\n')
            else:
                if disAns < 30:
                    # ぼかしの処理
                    mosaic()
                    # # 通知の設定
                    # notification_title = 'ちかい'
                    # notification_message = 'ちかづきすぎですはなれて！'
                    # notification_timeout = 10  # 表示時間（秒）

                    # # 通知を送る
                    # notification.notify(
                    #     title=notification_title,
                    #     message=notification_message,
                    #     timeout=notification_timeout
                    # )
                    # コマンドライン
                    print('顔が近いので少し離れてください')
                elif disAns >= 30:
                    if f_limit > gtime_cnt.val:
                        unmosaic()
                        print('%.2fcm\n' % disAns)    # 小数第２位まで出力

    # カウントのリセット
            fwcount = []
            ewcount = []

        # 画面に距離を表示
        if disAns == -1:
            # imshowで表示させている
            cv2.putText(frame,
                        # テキスト(英数字のみ)
                        text="Less than 10 cm! Please stay away!!",
                        org=(0, 30),       # 座標
                        # フォント(デフォルト cv2.FONT_HERSHEY_SIMPLEX)
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        # 文字の縮尺(本来は1.0を設定すればいいが顔の大きさに連動して文字も縮尺を変えるためfwを掛け、微調整で255で割っている)
                        fontScale=(1.0),
                        color=(0, 0, 255),  # 文字の色(顔枠と別の色)
                        thickness=2,        # 文字の太さ
                        lineType=cv2.LINE_AA)    # アルゴリズムの種類（文字を滑らかにするかどうか,デフォルトはcv2.LINE_8）
        elif disAns == -2:
            # 元データ
            cv2.putText(frame,
                        text="Over 70 cm! Please come closer!!",
                        org=(0, 30),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=(1.0),
                        color=(0, 0, 255),
                        thickness=2,
                        lineType=cv2.LINE_AA)
        else:
            if disAns < 30 and disAns != 0:     # 30cm未満の場合、警告を出す
                cv2.putText(frame,
                            text="Less than 30 cm! Please stay away!!",
                            org=(370, 60),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=(1.0),
                            color=(0, 0, 255),
                            thickness=2,
                            lineType=cv2.LINE_AA)
            if textChange == 0:     # 現在cmのテキストを頭上に表示する
                cv2.putText(frame,
                            text=str(round(disAns, 2))+"cm",
                            org=(fx, fy-6),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=(1.0),
                            color=(0, 255, 0),
                            thickness=2,
                            lineType=cv2.LINE_AA)
            else:                   # 現在cmのテキストを画面上部に固定で表示する
                cv2.putText(frame,
                            text=str(round(disAns, 2))+"cm",
                            org=(600, 30),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=(1.0),
                            color=(0, 255, 0),
                            thickness=2,
                            lineType=cv2.LINE_AA)

        # 結果を表示
        # cv2.imshow('gray', gray)
        # 画像の表示
        # cv2.imshow('YourFace', frame)

        # キー入力を10ms待つ
        # 「Esc」を押すと無限ループから抜けて終了処理に移る
        key = cv2.waitKey(10)
        if key == 27:
            break
        elif key == ord('0'):       # 「0」を押すと距離が即座に出る
            disAns = distance(sampleLen, fwSample, ewSample, fw, ew)
            print('%.2fcm\n' % disAns)
        elif key == ord('1'):
            if textChange == 0:     # 現在cmのテキストを頭上に表示している場合、画面上部に固定化する
                textChange = 1
            else:                  # 現在cmのテキストを画面上部に固定化している場合、頭上に表示する
                textChange = 0
    #time_limitの変更箇所-----------------------------------------

        #制限時間を超えたらパスワード入力画面を表示
        # if f_limit <= gtime_cnt.val:
        if gtime_flg.flg == 0:
            f = open('src/limit.txt', 'r')
            f_limit = int(f.read())
            f.close()
            if f_limit <= gtime_cnt.val:
                gtime_flg.flg = 1
                # gtime_cnt.val = 0
                #print("timeflg:%d" % gtime_flg.flg)
                # thread2 = threading.Thread(target=password_input.passbox)
                # thread2.start()
                # mosaic()
                # password_input.passbox()
                print("モザイクとパスワードを出す")
            
        #終了フラグまたは再起動フラグが立ったら終了
        if gend.flg == 1 or grestart_flg.flg == 1:
            print("終了します")
            time.sleep(1)
            break
        
        if gpass_sec.flg == 1:
            unmosaic()

# thread_restart = threading.Thread(target=restart_app)
# thread_restart.start()

HealtheyeS(cnt, fwcount, ewcount, fw, ew, disAns, textChange, fx, fy, ex, ey, sampleLen, fwSample, ewSample, MODECOUNT)
restart_app()
# -----------------------------------------------------------
print("関数終了処理-------------------------------------------")
# gtime_flg.flg = 1
thread_setting.join()
print("thread_settingを終了しました")
print("Healtheyes-Super終了処理-------------------------------")
# カメラのリソースを開放する
cap.release()
# OpenCVのウィンドウをすべて閉じる
cv2.destroyAllWindows()
print("カメラが終了しました")
# password_input.passbox_end()
print("正常に終了しました")
