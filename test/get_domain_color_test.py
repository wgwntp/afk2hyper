import cv2
import os
import numpy as np
import time
from collections import Counter
import shutil
from enum import Enum

class CardColor(Enum):
    UNKNOWN = 0
    GREEN = 1
    BLUE = 2
    PURPLE = 3
    GOLD = 4
    
def get_dominant_color(image_path, k=1):
    # 加载图片
    image = cv2.imread(image_path)
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 
    # 定义颜色范围（这里以红色为例，但可以根据需要调整）
    # 注意：这里的范围是为了演示，实际使用时需要根据图片颜色进行调整
    # lower_red = np.array([0, 120, 70])
    # upper_red = np.array([10, 255, 255])
    # mask1 = cv2.inRange(hsv, lower_red, upper_red)
 
    # 由于我们想要找到所有颜色的分布，这里不使用颜色范围掩码
    # 而是直接计算整个HSV图像的直方图
    hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
 
    # 平滑直方图以减少噪声（可选）
    cv2.normalize(hist, hist)
 
    # 找到直方图中的最大值及其索引
    _, max_val, _, max_loc = cv2.minMaxLoc(hist)
    h, s = max_loc
 
    # 将HSV值转换回BGR（注意：这里的转换不是精确的，因为V值被忽略了）
    # 而且，由于我们使用了50和60的bin数，所以需要将索引转换回原始范围
    h_range = 180 / 50
    s_range = 256 / 60
    h_value = int(h * h_range)
    s_value = int(s * s_range)
    v_value = 255  # 我们可以随意选择一个V值，因为它在找主要颜色时通常不那么重要
 
    # 转换回BGR颜色空间（注意：这只是一个近似值）
    dominant_bgr = cv2.cvtColor(cv2.cvtColor(np.uint8([[[h_value, s_value, v_value]]]), cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2RGB)
    dominant_color = tuple(dominant_bgr[0, 0, :])
 
    # 如果需要找到前k个主要颜色，可以修改此部分代码来排序直方图并获取前k个峰值
    # 这里只返回了一个主要颜色
    return dominant_color
def get_card_color(image):
    for i in range(3):
        # path,_,_ = utils.save_window_screenshot(hwnd)
        # image = cv2.imread(path)
        img_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        width, height, s = img_rgb.shape
        print(width,height,s)
        # 左上角
        pt1 = (int(width * 0.05),int(height * 0.05))
        # 右上角
        pt2 = (int(width * 0.97),int(height * 0.04))
        # 左下角
        pt3 = (int(width * 0.05),int(height * 0.98))
        # 右下角
        pt4 = (int(width * 0.97),int(height * 0.98))
        pts = [pt1,pt2,pt3,pt4]
        colors = []
        for p in pts:
            colors.append(getPointColor(img_rgb,p[0],p[1]))
        
        for c in colors:
            if c != CardColor.UNKNOWN:
                return c
        # print(most_common_element,count)
        # if most_common_element != CardColor.UNKNOWN:
        #     return most_common_element
        
        time.sleep(1)
    return CardColor.UNKNOWN

def getPointColor(img,x,y):
    pixel_color = img[x, y]
    r = pixel_color[0]
    g = pixel_color[1]
    b = pixel_color[2]
    # print("中心像素的 RGB 值:", pixel_color)
    if 35<r<55 and 145<g<165 and 155<b<175:
        return CardColor.BLUE
    elif 60<r<80 and 145<g<165 and 110<b<140:
        return CardColor.GREEN
    elif 70<r<190 and 50<g<110 and 140<b<255:
        return CardColor.PURPLE
    elif 180<r<255 and 110<g<170 and 0<b<80:
        return CardColor.GOLD
    else :
        print("UNKNOW COLOR:",r," ",g," ",b)
        return CardColor.UNKNOWN

if __name__ == "__main__":
    path = './color_img/'
    for filename in os.listdir(path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = path + filename  # 替换为您的图片路径
            image = cv2.imread(image_path)
            dominant_color = get_card_color(image)
            print(f"FileName is :{filename},The dominant color is: {dominant_color}")