import cv2
import numpy as np

# 用于快速测量 摄像头输入的不同颜色的阈值 对find_circle_0.py中的颜色阈值进行微调

# 打开摄像头
Pic_Capture = cv2.VideoCapture(0)
# 设置视频帧的宽度、高度和缓冲区大小
Pic_Capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
Pic_Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
# 通常不需要设置缓冲区大小，除非有特定需求
# Pic_Capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# 初始化HSV阈值
hsv_low = np.array([0, 0, 0])
hsv_high = np.array([180, 255, 255])

# 定义滑动条回调函数
def h_low(value):
    hsv_low[0] = value
def h_high(value):
    hsv_high[0] = value
def s_low(value):
    hsv_low[1] = value
def s_high(value):
    hsv_high[1] = value
def v_low(value):
    hsv_low[2] = value
def v_high(value):
    hsv_high[2] = value

# 创建窗口和滑动条
cv2.namedWindow('Set', cv2.WINDOW_FREERATIO)
cv2.createTrackbar('H low', 'Set', 0, 180, h_low)
cv2.createTrackbar('H high', 'Set', 180, 180, h_high)
cv2.createTrackbar('S low', 'Set', 0, 255, s_low)
cv2.createTrackbar('S high', 'Set', 255, 255, s_high)
cv2.createTrackbar('V low', 'Set', 0, 255, v_low)
cv2.createTrackbar('V high', 'Set', 255, 255, v_high)

# 循环读取视频帧
while True:
    ret, image = Pic_Capture.read()
    if not ret:
        break
    
    # 转换到HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 高斯模糊
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
    # 应用阈值
    mask = cv2.inRange(hsv, hsv_low, hsv_high)
    
    # 显示原始图像和过滤后的图像
    cv2.imshow('Original', image)
    cv2.imshow('Filtered', mask)
    
    # 检查按键事件q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭所有窗口
Pic_Capture.release()
cv2.destroyAllWindows()