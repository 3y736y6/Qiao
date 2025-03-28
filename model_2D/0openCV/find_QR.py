import cv2
from pyzbar.pyzbar import decode

# 扫二维码并
cap = cv2.VideoCapture(0)
_ , frame =  cap.read()

print("image shape: ", frame.shape)
cv2.imshow("img", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 将图像从BGR转换为灰度（可选，但通常有助于提高解码性能）
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# 使用pyzbar解码QRCode
decoded_objects = decode(gray)
mission = ''

# 打印解码结果
for obj in decoded_objects:
    print("类型:", obj.type)
    print("数据:", obj.data.decode("utf-8"))    
    print("str --> int",int(obj.data.decode("utf-8")))
    mission = obj.data.decode("utf-8")
    print(mission)
print(mission)

color_list = ["0","red","green","blue"]

mission_1 = int(mission[0:1])
mission_2 = int(mission[1:2])
mission_3 = int(mission[2:3])

print(color_list)
print(color_list[int(mission[0:1])])
print(color_list[int(mission[1:2])])
print(color_list[int(mission[2:3])])

print(mission,'->',mission_1,"->",mission_2,"->",mission_3)
