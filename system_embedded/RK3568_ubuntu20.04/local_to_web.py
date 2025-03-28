import numpy as np
from datetime import datetime  
import requests  
import json  
import csv  
def data_generator(ID_vibration_index):

    machine_Temp = 0
    device_Temp = 0
    device_Humidity = 0

    # 指定要读取的CSV文件名  
    filename = 'MacTemp_devTemp_Humi.csv'  
    
    # 指定要读取的行号（从1开始计数）  
    target_row_number = ID_vibration_index 
    
    # 打开文件进行读操作  
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:  
        # 创建一个csv reader对象  
        csvreader = csv.reader(csvfile)  
        
        # 初始化一个计数器  
        current_row_number = 1  
        
        # 遍历csv reader对象，读取每一行  
        for row in csvreader:  
            # 检查当前行号是否为目标行号  
            if current_row_number == target_row_number:  
                # 打印目标行  
                machine_Temp = row[0] 
                device_Temp = row[1]
                device_Humidity = row[2]
                # 如果只需要这一行，可以在这里退出循环  
                break  
            # 增加计数器  
            current_row_number += 1

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
    json_data = json.dumps(data_generator(6000))

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
