import cv2 as cv
import numpy as np
import time 
import move_car
import move_arm
from pyzbar.pyzbar import decode
# 找到圆形物料

class Find_Circle():
    def __init__(self):
        self.maxSquare = 0
        self.maxContour = None
        self.maxCenter = None
        self.dst = None
        self.color_hsv_range= {
            # 三种颜色的阈值范围，需要根据环境光线微调。可使用hsv_look_realtime.py查看颜色范围
            'green': {
                'min': np.array([45, 20, 30]),
                'max': np.array([75, 255, 255])
            },
            'red': {
                'min1': np.array([0, 90, 30]),
                'max1': np.array([20, 255, 255]),
                'min2': np.array([160, 90, 30]),
                'max2': np.array([190, 255, 255])
            },
            'blue': {
                'min': np.array([90, 50, 30]),
                'max': np.array([130, 255, 255])
            }
        }
    
    def find_circle(self, img, color):
        # 将RGB 转为 HSV格式，使用高斯模糊增强抗噪能力
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # GBR to HSV
        hsv = cv.GaussianBlur(hsv, (5, 5), 0)   # gao si mo hu 
        # 使用二值法将 图片变为黑白  
        # 例如判断颜色为红色，则使红色变为黑色，其他颜色变为白色
        if color == "red":
            dst1 = cv.inRange(hsv, self.color_hsv_range['red']['min1'], self.color_hsv_range['red']['max1'])   
            # cv.imshow("img", dst1)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            dst2 = cv.inRange(hsv, self.color_hsv_range['red']['min2'], self.color_hsv_range['red']['max2'])     
            # cv.imshow("img", dst2)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            self.dst = cv.bitwise_or(dst1, dst2)
            # cv.imshow("img", self.dst)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
        else:
            self.dst = cv.inRange(hsv, self.color_hsv_range[color]['min'], self.color_hsv_range[color]['max'])   
        
        # 查找黑白图片里面的 圆形轮廓（因为光线噪声存在，可能会有大小不同的多个圆形）
        contours_list, _ = cv.findContours(self.dst, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)   # 返回 轮廓列表(列表里包含 轮廓点 及其坐标)及层次(_)信息 

        # 选取 最大的轮廓
        for contour in contours_list: 
            square = cv.contourArea(contour)
            if square > 2500 and square > self.maxSquare: # 圆面积大于x000 且 为最大面积
                self.maxSquare = square
                self.maxContour = contour

        # 画出 最大轮廓
        if self.maxContour is not None:
            (x, y), _ = cv.minEnclosingCircle(self.maxContour) # 最小外接圆圆心和半径
            self.maxCenter = (int(x), int(y))

            cv.circle(img, self.maxCenter, 2, (0, 255, 0), 2, 8, 0)
            cv.drawContours(img, [self.maxContour], -1, (0, 0, 255), 2)
            cv.imshow("img", img)
            cv.waitKey(0)
            cv.destroyAllWindows()
            print("S: ", self.maxSquare)
        
            return True
        else:
            return False
        
# video_path：摄像头数据传入
# 将视频流 转换为 单帧图片
def get_frame(video_path):
    cap = cv.VideoCapture(video_path)
    _ , frame =  cap.read()
    # print("image shape: ", frame.shape)
    cv.imshow("img", frame)
    print(frame)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    return frame

# 解码二维码，读取任务
def decode_QR(video_path):
    frame = get_frame(video_path)   
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    decoded_objects = decode(gray)
    mission = ''
    for obj in decoded_objects:
        print("数据:", obj.data.decode("utf-8"))
        mission = obj.data.decode("utf-8")
    return mission
        
# 寻找圆形物料 每0.3s 寻找一次 一共寻找10次(根据实际情况修改)
def find(color,video_path):
    finder = Find_Circle()
    state = False
    for i in range(10):
        if state == True:
            print("Get it! center:",finder.maxCenter)
            break
        else:
            img = get_frame(video_path)
            state = finder.find_circle(img,color)
            print("try for the",i+1,"frame" )

        time.sleep(0.3)
# 返回中心点的坐标，例如摄像头为(224，224)大小
# 返回坐标为(100，50)表示物料中心点在摄像头的左下方，由此微调机械臂的抓取位置
    return finder.maxCenter 


def main():
    QR_camera = 0
    color_camera = 0
    color_list = ["0","red","green","blue"]
    mission = decode_QR(QR_camera)  #返回值str格式：123 三个数字 分别代表不同颜色
    # 根据返回值确定抓取的颜色和顺序
    mission_1 = color_list[int(mission[0:1])] 
    mission_2 = color_list[int(mission[1:2])]
    mission_3 = color_list[int(mission[2:3])]

    center = find(mission_1,color_camera)    # 获得第1个中心点 
    ##### 抓取代码1
    center = find(mission_2,color_camera)   # 获得第2个中心点 
    ##### 抓取代码2
    center = find(mission_3,color_camera)   # 获得第3个中心点 
    ##### 抓取代码3

    #####移动到下一个位置


if __name__ == '__main__':
    main()
