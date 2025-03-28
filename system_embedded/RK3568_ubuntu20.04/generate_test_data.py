import csv  
import random

datalist = []

for i in range(7000):
    machine_Temp = random.uniform(50.0,55.0)
    device_Temp = random.randint(32,35)
    device_Humidity = random.randint(22,25)
    datalist.append([machine_Temp,device_Temp,device_Humidity])


# 指定输出的CSV文件名  
filename = "MacTemp_devTemp_Humi.csv"  
  
# 打开文件进行写操作  
with open(filename, 'w', newline='') as csvfile:  
    # 创建一个csv writer对象  
    csvwriter = csv.writer(csvfile)  
      
    # 写入数据  
    for row in datalist:  
        csvwriter.writerow(row)  
  
print(f"CSV文件 '{filename}' 已生成并写入数据.")


  
# # 指定要读取的CSV文件名  
# filename = 'MacTemp_devTemp_Humi.csv'  
  
# # 打开文件进行读操作  
# with open(filename, 'r', newline='') as csvfile:  
#     # 创建一个csv reader对象  
#     csvreader = csv.reader(csvfile)  
      
#     # 逐行读取数据  
#     for row in csvreader:  
#         print(type(row))