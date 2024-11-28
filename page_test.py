import utils
import os
import config
def show_screen_ocr(hwnd):
    path,_,_,_,_ = utils.window_screenshot(hwnd)
    ocr_result = config.READER.readtext(path)
    os.remove(path)
    for r in ocr_result:
        print(r[0])
        print(r[1])