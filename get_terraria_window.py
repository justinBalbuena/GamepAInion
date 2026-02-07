import ctypes
import win32gui
import win32ui
import win32con
from PIL import Image

def find_terraria_window():
    terraria_hwnd = None
    terraria_title = None

    def enum_handler(hwnd, _):
        nonlocal terraria_hwnd, terraria_title
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd)
        if title.startswith("Terraria"):
            terraria_hwnd = hwnd
            terraria_title = title

    win32gui.EnumWindows(enum_handler, None)
    return terraria_hwnd, terraria_title


def capture_terraria_window(output="background_capture.png"):
    hwnd, title = find_terraria_window()

    if not hwnd:
        print("Terraria window not found.")
        return None

    print(f"Found Terraria window: {title}")

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    save_bit_map = win32ui.CreateBitmap()
    save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(save_bit_map)

    result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)

    bmpinfo = save_bit_map.GetInfo()
    bmpstr = save_bit_map.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr,
        'raw',
        'BGRX',
        0,
        1
    )

    win32gui.DeleteObject(save_bit_map.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    if result == 1:
        img.save(output)
        print(f"Captured Terraria window to {output}")
        return output

    print("PrintWindow failed.")
    return None


if __name__ == "__main__":
    capture_terraria_window()