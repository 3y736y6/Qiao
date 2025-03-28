import serial  
import csv
# 配置串行端口参数  
SERIAL_PORT = '/dev/ttyS0'  # 替换为你的RS485设备对应的串口  
BAUD_RATE = 9600            # 波特率，根据你的设备设置  
TIMEOUT = None              # 设置为None表示没有超时，即read()会阻塞直到有数据可读  
  
# 打开串行端口  
ser = serial.Serial(  
    port=SERIAL_PORT,  
    baudrate=BAUD_RATE,  
    timeout=TIMEOUT,  
    parity=serial.PARITY_NONE,  
    stopbits=serial.STOPBITS_ONE,  
    bytesize=serial.EIGHTBITS  
)  


def read_from_serial():  
    data_list = []
    count = 0
    try:  
        while True:  
            # 读取一行数据，这里假设数据是以换行符'\n'结尾的  
            if ( count % 2000 == 0 ) & ( count != 0 ):
                with open('MacTemp_devTemp_Humi.csv', mode='a', newline='', encoding='utf-8') as file:  
                    writer = csv.writer(file)  
                    
                    # 追加新行到CSV文件  
                    for row in data_list:  
                        writer.writerow(row) 
                
            line = ser.readline().decode('utf-8').rstrip()  
            if line:  
                data_list.append(line)
                count = count + 1
            


    except KeyboardInterrupt:  
        print("Program interrupted. Closing serial port.")  
    except serial.SerialException as e:  
        print(f"Serial error: {e}")  
    finally:  
        ser.close()  
  
if __name__ == "__main__":  
    read_from_serial()