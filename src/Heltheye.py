# 変更
# 顔を認識し、カメラから顔(目)までの距離を出す
# 一定間隔おきに距離を出す
# キー入力「0」で即座に距離を出す（精度低）
# キー入力「1」でcmの表記位置変更
# キー入力「Esc」で終了
# 画面サイズ1280,720で計測


import cv2
import sys
import statistics   # 最頻値

# 入力された値(fw,ew)から距離を求める関数--------------------------------------------------------------------
def distance(sample_len, fw_sample, ew_sample,fw,ew):
    value_abs = []      # 入力された値xと事前に計測された値との絶対値を格納
    value_abs_cnt = 0             # カウントの役割をする変数
    ans = 0             # 顔と画面との距離を格納
    standard = 90       # ewとfwのどちらを距離算出に使うかの基準数値 (90は50cmのとき)
    
    if ew >= standard :             # ewが基準値より小さければewを計算に使用
        for i in ew_sample:          # ewとの差の絶対値を格納
            value_abs.insert(value_abs_cnt,abs(i - ew))
            value_abs_cnt += 1
        
        values_abs_sorted = sorted(value_abs)        # 絶対値の値たちを昇順にソートして格納   
        
        value_abs_cnt = 0
        for i in value_abs:         # ewに一番近い値（絶対値）の要素番号を見つける
            if i == values_abs_sorted[0]:
                break
            value_abs_cnt += 1
        
        if ew > ew_sample[0]:        # 距離が恐らく10cm以下の場合
            ans = -1
        elif ew == ew_sample[value_abs_cnt]:       # ewとewに最も近い値が等しい場合
            ans = sample_len[value_abs_cnt]
        elif ew > ew_sample[value_abs_cnt]:        # ewに最も近い値がewよりも小さい場合
            few_diff = abs(ew_sample[value_abs_cnt] - ew_sample[value_abs_cnt-1])        # ewの大きさの差の絶対値ew_diffrence
            few_chg = abs(sample_len[value_abs_cnt] - sample_len[value_abs_cnt-1]) / few_diff # 1cmごとに変化するewの大きさew_chg
            few_chg_diff = abs(ew - ew_sample[value_abs_cnt-1])                   # ewより小さくて最も近い値からどれだけの差があるか
            few_add = few_chg * few_chg_diff                               # ewより小さくて最も近い値より何cm離れているか
            ans = sample_len[value_abs_cnt-1] + few_add                      # どれだけ画面から離れているか
        else:                       # ewに最も近い値がewよりも大きい場合
            few_diff = abs(ew_sample[value_abs_cnt] - ew_sample[value_abs_cnt+1])        # ewの大きさの差
            few_chg = abs(sample_len[value_abs_cnt] - sample_len[value_abs_cnt+1]) / few_diff # ewが1増えるごとに何cm増えるか
            few_chg_diff = abs(ew - ew_sample[value_abs_cnt])                     # ewより大きくて最も近い値からどれだけの差があるか
            few_add = few_chg * few_chg_diff                               # ewより大きくて最も近い値より何cm離れているか
            ans = sample_len[value_abs_cnt] + few_add                        # どれだけ画面から離れているか
    else:       # ewが基準値より大きければfwを計算に使用
        
        for i in fw_sample:                      # fwとの差の絶対値を格納
            value_abs.insert(value_abs_cnt,abs(i - fw))
            value_abs_cnt += 1
        
        values_abs_sorted = sorted(value_abs)    # 絶対値の値たちをソート（昇順）を格納
        
        value_abs_cnt = 0
        for i in value_abs:                     # fwに一番近い値（絶対値）の要素番号を見つける
            if i == values_abs_sorted[0]:
                break
            value_abs_cnt += 1
        
        if fw < fw_sample[len(fw_sample)-1]:  # 距離が恐らく70cm以上の場合
            ans = -2
        elif fw == fw_sample[value_abs_cnt]:       # fwとfwに最も近い値が等しい場合
            ans = sample_len[value_abs_cnt]
        elif fw > fw_sample[value_abs_cnt]:        # fwに最も近い値がfwよりも小さい場合
            few_diff = abs(fw_sample[value_abs_cnt] - fw_sample[value_abs_cnt-1])        # fwの大きさの差
            few_chg = abs(sample_len[value_abs_cnt] - sample_len[value_abs_cnt-1]) / few_diff # 1cmごとに変化するfwの大きさ
            few_chg_diff = abs(fw - fw_sample[value_abs_cnt-1])                   # fwより小さくて最も近い値からどれだけの差があるか
            few_add = few_chg * few_chg_diff                               # fwより小さくて最も近い値より何cm離れているか
            ans = sample_len[value_abs_cnt-1] + few_add                      # どれだけ画面から離れているか
        else:                           # fwに最も近い値がfwよりも大きい場合
            few_diff = abs(fw_sample[value_abs_cnt] - fw_sample[value_abs_cnt+1])        # fwの大きさの差
            few_chg = abs(sample_len[value_abs_cnt] - sample_len[value_abs_cnt+1]) / few_diff # fwが1増えるごとに何cm増えるか
            few_chg_diff = abs(fw - fw_sample[value_abs_cnt])                     # fwより大きくて最も近い値からどれだけの差があるか
            few_add = few_chg * few_chg_diff                               # fwより大きくて最も近い値より何cm離れているか
            ans = sample_len[value_abs_cnt] + few_add                        # どれだけ画面から離れているか
    return ans
# ---------------------------------------------------------------------------------------------------------

# カスケード分類器のパスを各変数に代入
fase_cascade_path = './data/haarcascades/haarcascade_frontalface_default.xml'
eye_cascade_path = './data/haarcascades/haarcascade_eye.xml'

# カスケード分類器の読み込み
face_cascade = cv2.CascadeClassifier(fase_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

# Webカメラの準備（引数でカメラ指定、0は内臓カメラ）
cap = cv2.VideoCapture(0)

FRAME_LINESIZE = 2       # 顔に四角を描画する際の線の太さ
FRAME_RGB_G = (0, 255, 0)  # 四角形を描画する際の色を格納(緑)
FRAME_RGB_B = (255, 0, 0)  # 四角形を描画する際の色を格納(青)
mode_cnt = 0     # カウントの際に使用
text_change = 0  # cmの表記を画面上部に固定にするか、顔に追従するかの切り替え
fw = 100    # 顔の大きさの初期値（起動時エラー回避のため初期値設定face_width）
fx = 100    # 顔のx座標の初期値face_x
fy = 100    # 顔のy座標の初期値face_y
ew = 100    # 目の大きさの初期値eyes_width
ex = 100    # 目のx座標の初期値eyes_x
ey = 100    # 目のy座標の初期値eyes_y
dis_ans = 0  # 計測した距離を格納distance_answer
fw_cnt = []  # fwを一時的に格納（最頻値を出すために使用）face_width_count
ew_cnt = []  # ewを一時的に格納（最頻値を出すために使用）eyws_width_count
MODE = 50  # 最頻値を出すときの要素数（この値を変更することで計測値(cm)の正確性と計測にかかる時間が変化）
SAMPLE_LEN = [ 10,   15,  20,  30,  40,  50,  60,  70]       # fwSample,ewSampleに対応した顔とカメラとの距離(cm)
FW_SAMPLE  = [ 999, 999, 999, 999, 431, 348, 292, 253]       # 事前に計測した距離に対応する顔の大きさ
EW_SAMPLE  = [ 268, 214, 161, 118,  90,  62,  59,  54]       # 事前に計測した距離に対応する目の大きさ

# cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
# cap.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラ画像の縦幅を720に設定
# print cap.get(cv2.CAP_PROP_FPS)
# print cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# print cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# もしカメラが起動していなかったら終了する
if cap.isOpened() is False:
    print("カメラが起動していないため終了しました")
    sys.exit()

# 無限ループで読み取った映像に変化を加える（1フレームごとに区切って変化）
while True:
    ret, frame = cap.read()

    # カラーをモノクロ化したキャプチャを代入(グレースケール化)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔の検出
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5)
    
    # 目の検出
    eyes = eye_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5)
    
    # 顔に四角形(矩形)を描画する
    # 第1引数   効果を適応する画像
    # 第2引数   矩形の左上隅の座標
    # 第3引数   矩形の右下隅の座標
    # 第4引数   矩形の色
    # 第5引数   描画する線の太さ（-1以下だと塗りつぶし）
    for (fx, fy, fw, fh) in faces:
        cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh),
                        FRAME_RGB_G, FRAME_LINESIZE)
        
    # 目に四角形(矩形)を描画する
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh),
                        FRAME_RGB_B, FRAME_LINESIZE)

    if mode_cnt < MODE: #もしmode_cntがMODEより小さければfwとewを格納
        fw_cnt.insert(mode_cnt,fw)
        ew_cnt.insert(mode_cnt,ew)
        mode_cnt += 1
    else:
        mode_cnt = 0
        dis_ans = distance(SAMPLE_LEN, FW_SAMPLE, EW_SAMPLE, statistics.mode(fw_cnt), statistics.mode(ew_cnt))
        if dis_ans == -1:
            print('10cm以下です!近すぎます!!\n')
        elif dis_ans == -2:
            print('70cm以上離れています!!\n')
        else:
            if dis_ans < 30:
                print('顔が近いので少し離れてください')
            print('%.2fcm\n' % dis_ans)    # 小数第２位まで出力
            
        fw_cnt = []
        ew_cnt = []

    # 画面に距離を表示
    if dis_ans == -1:
        cv2.putText(frame,
                        text="Less than 10 cm! Please stay away!!",    # テキスト(英数字のみ)
                        org=(0,30),       # 座標
                        # フォント(デフォルト cv2.FONT_HERSHEY_SIMPLEX)
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        # 文字の縮尺(本来は1.0を設定すればいいが顔の大きさに連動して文字も縮尺を変えるためfwを掛け、微調整で255で割っている)
                        fontScale=(1.0),
                        color=(0, 0, 255),  # 文字の色(顔枠と別の色)
                        thickness=2,        # 文字の太さ
                        lineType=cv2.LINE_AA)    # アルゴリズムの種類（文字を滑らかにするかどうか,デフォルトはcv2.LINE_8）
    elif dis_ans == -2:
                cv2.putText(frame,
                        text="Over 70 cm! Please come closer!!",    
                        org=(0,30),       
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=(1.0),
                        color=(0, 0, 255),  
                        thickness=2,        
                        lineType=cv2.LINE_AA)    
    else:
        if dis_ans < 30 and dis_ans != 0:     # 30cm未満の場合、警告を出す
            cv2.putText(frame,
                        text="Less than 30 cm! Please stay away!!",
                        org=(370,60),       
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=(1.0),
                        color=(0, 0, 255),  
                        thickness=2,        
                        lineType=cv2.LINE_AA)   
        if text_change == 0:     # 現在cmのテキストを頭上に表示する
            cv2.putText(frame,
                                text=str(round(dis_ans,2))+"cm",    
                                org=(fx, fy-6),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=(1.0),
                                color=(0, 255, 0),  
                                thickness=2,
                                lineType=cv2.LINE_AA)   
        else:                   # 現在cmのテキストを画面上部に固定で表示する
            cv2.putText(frame,
                                text=str(round(dis_ans,2))+"cm",
                                org=(600, 30),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=(1.0),
                                color=(0, 255, 0),
                                thickness=2,
                                lineType=cv2.LINE_AA)

    # 結果を表示
    # cv2.imshow('gray', gray)
    cv2.imshow('YourFace', frame)

    # キー入力を10ms待つ
    # 「Esc」を押すと無限ループから抜けて終了処理に移る
    key = cv2.waitKey(10)
    if key == 27:
        break
    elif key == ord('0'):       # 「0」を押すと距離が即座に出る
        dis_ans = distance(SAMPLE_LEN, FW_SAMPLE, EW_SAMPLE, fw, ew)
        print('%.2fcm\n' % dis_ans)
    elif key == ord('1'):
        if text_change == 0:     # 現在cmのテキストを頭上に表示している場合、画面上部に固定化する
            text_change = 1
        else :                  # 現在cmのテキストを画面上部に固定化している場合、頭上に表示する
            text_change = 0

# 終了処理
# カメラのリソースを開放する
cap.release()
# OpenCVのウィンドウをすべて閉じる
cv2.destroyAllWindows()
