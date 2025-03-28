import random
import numpy as np
from datetime import datetime  
import requests  
import json  

def data_generator(ID_vibration_index):

    # 机器温度  和  设备温度/湿度
    machine_Temp = random.uniform(50.0,55.0)
    device_Temp = random.uniform(30,33)
    device_Humidity = random.uniform(20,23)

    # 振动
    vibration_numpy = np.loadtxt('./test.dat',dtype=np.float32)  # 长度为7000的数组
    vibration = vibration_numpy.tolist()  

    # 时间  
    current_datetime = datetime.now()  
    formatted_datetime = current_datetime.strftime("%Y.%m.%d_%H.%M.%S") # 格式化

    data = {  
        "device_NO": 1,              # 固定
        "frequency_sample": 1000,    # 固定
        "sample_points":1645,        # 固定

        "temp_machine": machine_Temp,  
        "humidity_device": device_Humidity,  
        "temp_device" : device_Temp,

        "vibration": vibration[ID_vibration_index],  

        "date" : formatted_datetime
    }  
    return data

def post_signal():

    # Flask应用的URL  
    url = 'https://madebyhuman.top/postsignal'  
    # url = '127.0.0.1:9988/postsignal'  
    # 将数据转换为JSON格式  
    json_data = json.dumps(data_generator(1000))

    # 发送POST请求  
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})  

    # 检查响应状态码  
    if response.status_code == 200:  
        # 请求成功，打印响应内容  
        print("Request successful")  
        print(response.json())  
    else:  
        # 请求失败，打印错误信息  
        print("Request failed")  
        print("Status code:", response.status_code)  
        print("Response:", response.text)

def main():
    post_signal()

if __name__ == '__main__':
    main()
