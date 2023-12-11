# 実行注意止めれません
# from pynput import mouse
# import cv2
# import numpy as np
# import win32gui
# import win32con
# import win32ui
# import win32api
# import ctypes
# import threading

# # ぼかしの関数


# def mosaic():
#     # ぼかしのカーネルサイズ
#     blur_kernel_size = (101, 101)

#     # キャプチャする領域のサイズ（画面全体）
#     screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) * 2
#     screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) * 2

#     # ウィンドウスクリーンのキャプチャ
#     hwnd = win32gui.GetDesktopWindow()
#     hwnd_dc = win32gui.GetWindowDC(hwnd)
#     mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
#     save_dc = mfc_dc.CreateCompatibleDC()
#     save_bitmap = win32ui.CreateBitmap()
#     save_bitmap.CreateCompatibleBitmap(mfc_dc, screen_width, screen_height)
#     save_dc.SelectObject(save_bitmap)
#     save_dc.BitBlt((0, 0), (screen_width, screen_height),
#                    mfc_dc, (0, 0), win32con.SRCCOPY)

#     # ビットマップから画像データを取得
#     bmp_info = save_bitmap.GetInfo()
#     bmp_data = save_bitmap.GetBitmapBits(True)
#     image_np = np.frombuffer(bmp_data, dtype=np.uint8).reshape(
#         screen_height, screen_width, 4)

#     # 画面全体にぼかしをかける
#     blurred_image = cv2.GaussianBlur(image_np, blur_kernel_size, 0)

#     # モザイクをかけた画像をデスクトップに戻す
#     img_data = blurred_image.tobytes()

#     # BITMAPINFOHEADER構造体の作成
#     class BITMAPINFOHEADER(ctypes.Structure):
#         _fields_ = [
#             ("biSize", ctypes.c_uint32),
#             ("biWidth", ctypes.c_long),
#             ("biHeight", ctypes.c_long),
#             ("biPlanes", ctypes.c_short),
#             ("biBitCount", ctypes.c_short),
#             ("biCompression", ctypes.c_uint32),
#             ("biSizeImage", ctypes.c_uint32),
#             ("biXPelsPerMeter", ctypes.c_long),
#             ("biYPelsPerMeter", ctypes.c_long),
#             ("biClrUsed", ctypes.c_uint32),
#             ("biClrImportant", ctypes.c_uint32),
#         ]

#     bmi_header = BITMAPINFOHEADER()
#     bmi_header.biSize = ctypes.sizeof(BITMAPINFOHEADER)
#     bmi_header.biWidth = screen_width
#     bmi_header.biHeight = -screen_height
#     bmi_header.biPlanes = 1
#     bmi_header.biBitCount = 32
#     bmi_header.biCompression = win32con.BI_RGB

#     # BITMAPINFO構造体の作成
#     class BITMAPINFO(ctypes.Structure):
#         _fields_ = [("bmiHeader", BITMAPINFOHEADER),
#                     ("bmiColors", ctypes.c_ulong * 3)]

#     bmi = BITMAPINFO()
#     bmi.bmiHeader = bmi_header

#     hdc = win32gui.GetDC(0)
#     # ぼかしを表示する範囲
#     ctypes.windll.gdi32.SetDIBitsToDevice(
#         hdc, 0, 0, screen_width, screen_height,
#         0, 0, 0, screen_height, img_data, ctypes.byref(
#             bmi), win32con.DIB_RGB_COLORS
#     )
#     win32gui.ReleaseDC(0, hdc)

#     # GUIリソースの解放
#     win32gui.ReleaseDC(hwnd, hwnd_dc)
#     win32gui.DeleteObject(save_bitmap.GetHandle())

# # マウスイベントハンドラ


# def on_move(x, y):
#     threading.Thread(target=mosaic).start()


# # マウスの監視を開始
# with mouse.Listener(on_move=on_move) as listener:
#     listener.join()


# import
import cv2
import numpy as np
import win32gui
import win32con
import win32ui
import win32api
import ctypes

# ぼかしの関数


def mosaic():
    # ぼかしのカーネルサイズ
    blur_kernel_size = (101, 101)

    # キャプチャする領域のサイズ（画面全体）
    # 私のPCでは大きさが小さかったので全体的に2倍にしてます
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) * 2
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) * 2

    # ウィンドウスクリーンのキャプチャ
    # ウィンドウハンドルの取得
    hwnd = win32gui.GetDesktopWindow()
    # デバイスコンテキストを取得
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    # Bitmapの作成
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bitmap = win32ui.CreateBitmap()
    # サイズの指定
    save_bitmap.CreateCompatibleBitmap(mfc_dc, screen_width, screen_height)
    save_dc.SelectObject(save_bitmap)
    # デスクトップの画面自体をコピー
    save_dc.BitBlt((0, 0), (screen_width, screen_height),
                   mfc_dc, (0, 0), win32con.SRCCOPY)

    # ビットマップから画像データを取得
    bmp_info = save_bitmap.GetInfo()
    bmp_data = save_bitmap.GetBitmapBits(True)
    image_np = np.frombuffer(bmp_data, dtype=np.uint8).reshape(
        screen_height, screen_width, 4)

    # 画面全体にぼかしをかける
    blurred_image = cv2.GaussianBlur(image_np, blur_kernel_size, 0)

    # モザイクをかけた画像をデスクトップに戻す
    img_data = blurred_image.tobytes()

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
    # ぼかしを表示する範囲
    ctypes.windll.gdi32.SetDIBitsToDevice(
        hdc, 0, 0, screen_width, screen_height,
        0, 0, 0, screen_height, img_data, ctypes.byref(
            bmi), win32con.DIB_RGB_COLORS
    )
    win32gui.ReleaseDC(0, hdc)

    # ウィンドウを閉じる
    # cv2.destroyAllWindows()

    # GUIリソースの解放
    win32gui.ReleaseDC(hwnd, hwnd_dc)
    win32gui.DeleteObject(save_bitmap.GetHandle())