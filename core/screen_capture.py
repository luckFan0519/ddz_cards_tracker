import win32gui
import win32ui
import win32con
from PIL import Image
import ctypes

class ScreenCapture:
    """
    窗口截图类, 截取图片
    """

    def __init__(self, window_title: str = None):
        ctypes.windll.user32.SetProcessDPIAware() # 这一行代码是用来确保你的应用程序在高DPI（每英寸点数）显示器上正确显示的
        self.window_title = window_title

    def capture_window(self):      # 截图
        hwnd = win32gui.FindWindow(None, self.window_title)
        if not hwnd:
            print(f"没找到窗口: {self.window_title}")
            return None

        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        hdesktop = win32gui.GetDesktopWindow()
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)
        mem_dc = img_dc.CreateCompatibleDC()

        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(img_dc, w, h)
        mem_dc.SelectObject(bmp)

        mem_dc.BitBlt(
            (0, 0), (w, h),
            img_dc, (left, top),
            win32con.SRCCOPY
        )

        bmpinfo = bmp.GetInfo()
        bmpstr = bmp.GetBitmapBits(True)

        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # 释放资源
        mem_dc.DeleteDC()  # 删除内存设备上下文
        img_dc.DeleteDC()  # 删除图像设备上下文
        win32gui.ReleaseDC(hdesktop, desktop_dc)  # 释放桌面设备上下文
        win32gui.DeleteObject(bmp.GetHandle())  # 删除位图对象

        return img

#
#
#
#
# if __name__ == "__main__":
#     screen = ScreenCapture("JJ斗地主")
#     img = screen.capture_window()
#     img.show()
#     img.save("screenshot.png")