import cv2
import unittest
import utils
import cus_enum as ce


class MatchOneTemplateCase:
    def __init__(self,image_paths,temp_path,ratio_w,ratio_h,except_x,except_y):
        self.image_paths = image_paths
        self.temp_path = temp_path
        self.ratio_w = ratio_w
        self.ratio_h = ratio_h
        self.except_x = except_x
        self.except_y = except_y
        
class GetPageTypeCase:
    def __init__(self,image_paths,except_page_type):
        self.image_paths = image_paths
        self.expcept_page_type = except_page_type
        
        
# 100 * 75 ratio
ratio_w = 0.086
ratio_h = 0.035       
match_one_templates_casese = [
    MatchOneTemplateCase(
        ["./test/image/test_confirm_image.png"],
        "confirm.png",
        ratio_w,
        ratio_h,
        except_x = 910,
        except_y = 1381,
    ),
    MatchOneTemplateCase(
        ["./test/image/test_ready_for_fighting_page.png"],
        "back.png",
        ratio_w,
        ratio_h,
        except_x = 108,
        except_y = 1930,
    ),
]

get_page_type_casese = [
    GetPageTypeCase(
        ["./test/image/test_confirm_image.png"],
        except_page_type = ce.PageType.CONFIMR_PAGE,
    ),
    GetPageTypeCase(
        ["./test/image/test_no_hero_page.png"],
        except_page_type = ce.PageType.NO_HERO_PAGE,
    ),
    GetPageTypeCase(
        ["./test/image/test_map_page.png"],
        except_page_type = ce.PageType.MAP_PAGE,
    ),
]
class TestMatchOneTemplate(unittest.TestCase):
    def assertIntAlmostEqual(self, first, second, tolerance=10):
        """
        自定义断言方法，用于检查两个整数是否在指定的误差范围内。
        
        :param first: 第一个整数
        :param second: 第二个整数
        :param tolerance: 允许的误差范围（默认为10）
        """
        self.assertTrue(abs(first - second) <= tolerance,
                        f"{first} is not within {tolerance} of {second}")
    def test_match_template(self):

        for case in match_one_templates_casese:
            for image_path in case.image_paths:
                image = cv2.imread(image_path)
                # 获取图片的宽高（注意：OpenCV返回的是（高度，宽度），与Pillow不同）
                height, width = image.shape[:2]
                image_info = (image_path,width,height,0,0)
                # 调用被测试的方法
                x, y = utils.matchTemplate(image_info, case.temp_path, case.ratio_w, case.ratio_h)
                if case.except_x == 0 and case.except_y == 0:
                    print(x,y)
                    # 读取原图和模板图进行对比
                    map_image = cv2.imread(image_path)
                    # 绘制矩形框（如果找到匹配项）
                    if x != 0 and y != 0:
                        tempW, tempH = utils.reCalTemplateSize(width, height, ratio_w, ratio_h)
                        start_point = (x - int(tempW / 2), y - int(tempH / 2))
                        end_point = (x + int(tempW / 2), y + int(tempH / 2))  # 调整高度以匹配模板比例
                        cv2.rectangle(map_image, start_point, end_point, (0, 255, 0), 2)
                        print(x,y)
                    # 显示结果
                    cv2.imshow('Detected Result', map_image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                self.assertIntAlmostEqual(x,case.except_x)
                self.assertIntAlmostEqual(y,case.except_y)
                
    def test_get_page_type(self):
          for case in get_page_type_casese:
              for image_path in case.image_paths:
                image = cv2.imread(image_path)
                # 获取图片的宽高（注意：OpenCV返回的是（高度，宽度），与Pillow不同）
                height, width = image.shape[:2]
                image_info = (image_path,width,height,0,0)
                page_type,_ = utils.get_current_page_type_by_image_path(image_info)
                self.assertEqual(page_type,case.expcept_page_type)
                
if __name__ == '__main__':
    unittest.main()