import cv2
import os
import numpy as np
import time
from collections import Counter
import shutil
from enum import Enum

def get_card_map(cart_path):
    # cardsMap [cardNumber=1-y,2-y,cardImage=[...]]
    cardsMap = []
    for filename in os.listdir(cart_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img = cv2.imread(cart_path + '/' + filename)
            # resized_img = cv2.resize(img, (resize_w, resize_h), interpolation=cv2.INTER_AREA)
            sp = filename.split('.')
            cardsMap.append([sp[0] ,img])
    return cardsMap

if __name__ == "__main__":
    image = cv2.imread('./template_img/fighting.png')
    temp_image = cv2.imread('./template_img/game2.png')
    _,w,h = image.shape[::-1]
    # 0.095,0.057
    calW = int(w * 0.095)
    calH = int(h * 0.057)
    # resized_img = cv2.resize(temp_image, (calW, calH), interpolation=cv2.INTER_AREA)
    # res = cv2.matchTemplate(image, resized_img, cv2.TM_CCOEFF_NORMED)
    # threshold = 0.8
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # top_left = max_loc
    # bottom_right = (top_left[0] + calW, top_left[1] + calH)
    # cv2.rectangle(image, top_left, bottom_right, 255, 2)
    # cv2.imshow('Detected', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print(max_val)
    cards_map = [temp_image]
    for cm in cards_map:
        resized_img = cv2.resize(cm[1], (calW, calH), interpolation=cv2.INTER_AREA)
        # 创建 SIFT 或 ORB 检测器
        sift = cv2.SIFT_create()  # 或者 cv2.ORB_create() for ORB
        keypoints_image, descriptors_image = sift.detectAndCompute(image, None)
        keypoints_template, descriptors_template = sift.detectAndCompute(resized_img, None)
        # # 创建 BFMatcher 并进行匹配
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors_template, descriptors_image, k=2)
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
                
        result_image = cv2.drawMatches(resized_img, keypoints_template, image, keypoints_image, good_matches, None)
        cv2.imshow("Matches", result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # res = cv2.matchTemplate(image, resized_img, cv2.TM_CCOEFF_NORMED)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # top_left = max_loc
        # bottom_right = (top_left[0] + calW, top_left[1] + calH)
        # cv2.rectangle(image, top_left, bottom_right, 255, 2)
        # cv2.imshow('Detected', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print(cm[0],len(good_matches))
        if len(good_matches) > 40:
            print(keypoints_image[good_matches[0].trainIdx].pt)
    # loc = np.where(res >= threshold)  
    # # 在原图上绘制矩形框，标记出匹配的位置
    # pts = list(zip(*loc[::-1]))
    # for pt in pts:
    #     # current_card_list.append([cardNumber,pt])
    #     cv2.rectangle(image, pt, (pt[0] + calW, pt[1] + calH), (0, 255, 0), 2)
    #     cv2.imshow('Detected', image)  
    #     cv2.waitKey(0)
    # print(w,'end',h)
    import cv2

# 加载图像和模板
# image = cv2.imread('image.jpg', 0)
# template = cv2.imread('template.jpg', 0)

# # 创建 SIFT 或 ORB 检测器
# sift = cv2.SIFT_create()  # 或者 cv2.ORB_create() for ORB
# keypoints_image, descriptors_image = sift.detectAndCompute(image, None)
# keypoints_template, descriptors_template = sift.detectAndCompute(template, None)

# # 创建 BFMatcher 并进行匹配
# bf = cv2.BFMatcher()
# matches = bf.knnMatch(descriptors_template, descriptors_image, k=2)

# # 应用比率测试，筛选出好的匹配点
# good_matches = []
# for m, n in matches:
#     if m.distance < 0.75 * n.distance:
#         good_matches.append(m)

# # 画出匹配结果
# result_image = cv2.drawMatches(template, keypoints_template, image, keypoints_image, good_matches, None)
# cv2.imshow("Matches", result_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

