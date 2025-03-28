---
export_on_save:
  html: true
html:
  embed_local_images: false
  embed_svg: true
  offline: false
  toc: true
print_background: false
---


IIC  小数据，短距离，较慢速
多个设备公用两条线，均上拉，SDA,SCL，每个IIC设备都有一个地址，
高速IIC的传输速率400kbps = 400Khz =2.5ns，标准速率100Khz=10ns
多个IIC设备连接时，开漏输出(OD)，防干扰

OD有双态 - 1 高组态-由于SCL总线上拉-高阻态时电流没法溜走总线为1
	 - 2 漏-总线为0

同步 半双工 多主控，谁控制SCL谁就是Master，
SCL控制--SCL为1时，SDA可以切换电平，SCL为0时，SDA不可切换电平，以保持稳定供接收端接收信息
收发数据--谁控制SDA谁就在SCL=0时改变SDA状态发数据，接收端在SCL=1时检测SDA总线电平即可

全过程--空闲SCL--1,SDA--1，全过程虽然Master检测Slaver应答，但不涉及output --> input，直接readpin

start--SCL为1时，不允许SDA变化，但是start和end信号除外，
①start--SCL拉高，SDA拉高>5ns，(一般end后，也就是空闲时，都为高，可以不用进行此操作，但是有些人数据传完后不加end操作，使得总线状态仍为0)，
在SCL=1时，SDA跳为0，延时>5ns，SCL拉低，使得SDA可以进行电平转换以传输数据
②7bit寻址+read-1/write-0指令(也叫方向位)
②、、有些设备直接可以传输了，有些slave还需要一些特定的command，
例如在访问存储器时，需要master发一个地址用于寻找内存地址，
例如在访问传感器时，需要发一个上电command用于启动传感器ADC，但是command就是特定的data而已
③command/data--接收端收到8bit后，接收端发送一个应答，此时发送端检测总线是否有一个应答
④、、应答正确ACD低脉冲，应答错误NACK高脉冲
应答ACK的发送--拉低SCL使SDA可以改变，拉低SDA，接着拉高SCL，等待>5ns以检测SDA状态，拉低SCL使SDA可以改变，拉高SDA
检测到ACK后继续传输，长时间没检测到master会默认收到，也就是最后一个数据发完可以直接end操作，不过尽量避免
⑤end--SCL拉高，延时>5ns，SDA跳为1>5ns  ，转入空闲，即为结束

BH1750光敏传感器
AT24C02--EEPROM存储器

源码见GY_302_BH1750.c和.h


