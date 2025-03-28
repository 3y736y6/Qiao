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
###dating...
SOF start of frame	 帧
Arbitration Field 	 仲裁场
ID identifier  	 11bit
IDE identifier extension  	18bit
RTR Remote transmission request [data 0 >>remote 1]
SRR  substitute remote request  	替代位
Control Field 
r，r0，r1 reserve bit 		保留位，规定显性
DLC data length code
Data Field	，0-8byte  MSB传输
CRC Check field
DEL Delimiter 界定符，分隔符,规定[1]
ACK Acknowledge character 确认符
EOF end of frame 
ITM intermission 间歇符

Bit Stuffing 位填充	
填充的范围从SOF到CRC，只要总线上出现了5个连续相同的位，在下一位插入一个与其相反的位，假设插入一个隐形，会与后4位组成5个，产生一个新的插入，显现同理。
如果在SOF到CRC段发现有6个连续相同的位，即没有出现正确插入，则总线发送的数据有问题。
（1）发送方的工作
在发送数据帧和遥控帧时，SOF～CRC 段间的数据，相同电平如果持续5 位，在下一个位（第6 个位）则要插入1 位与前5 位反型的电平。
（2）接收方的工作
在接收数据帧和遥控帧时，SOF～CRC 段间的数据，相同电平如果持续5 位，需要删除下一个位（第6 个位）再接收。如果这个第6 个位的电平与前5 位相同，将被视为错误并发送错误帧。

Error Frame
1.Error Flag Active 6个0+8个1
2.Error Flag Active 6个1+8个1
用于通知其他节点发生错误
错误帧发送完成后，总线空闲时自动重发出错的数据帧。


standard frame：
start---SOF[0] 
[12bit]Arbitration Field---ID[0:10] +  RTR[data 0]
Control Field---IDE[ standard 0 ] +  r0[1]  + DLC[0:3]
Data Field---[min 0:7---max 0:63]
CRC Check field---CRC value[0:14]  + DEL[1]
ACK Field---发送设备发送1，接收设备接收[right 0/error 1]  + DEL[1]
EOF---[7个1]
IMT---[3个1]
连续11个[1]表示总线空闲
当发送数据时出现连续的11个1时，会Bit stuffing，因此不会在发送数据时出现总线空闲

extension frame：

[32bit]Arbitration Field---ID[0:10]  + SRR[1]  + IDE[ extension 1 ]  + ID[11:28]  + RTR[data 0]
Control Field--- r1[0] +  r2[0]  + DLC[0:3]

Init
使能CAN总线HAL_CAN_Start
中断的激活 HAL_CAN_ActivateNotification(&hcan1, CAN_IT_RX_FIFO0_MSG_PENDING);(选择CANx，选择RX/TX，选择FIFO0/1)
回调函数的配置(可不配置)

TX
TXdata buffer的配置
发送帧 的结构的配置

RX
RXdata buffer的配置
筛选器的配置 HAL_CAN_ConfigFilter(&hcan1, &can_Filter)	
自定义结构体参数（HAL中已给出此结构体定义）CAN_FilterTypeDef   can_Filter = {0};



HAL_CAN_Start			//开启CAN通讯
HAL_CAN_Stop			//关闭CAN通讯
HAL_CAN_RequestSleep		//尝试进入休眠模式
HAL_CAN_WakeUp			//从休眠模式中唤醒
HAL_CAN_IsSleepActive		//检查是否成功进入休眠模式
HAL_CAN_AddTxMessage		//向 Tx 邮箱中增加一个消息,并且激活对应的传输请求
HAL_CAN_AbortTxRequest		//请求中断传输
HAL_CAN_IsTxMessagePending	//检查是否有传输请求在指定的 Tx 邮箱上等待
HAL_CAN_GetRxMessage		//从Rx FIFO 收取一个 CAN 帧


Timer Triggered Communication Mode:否使用时间触发功能 (ENABLE/DISABLE)，时间触发功能在某些CAN 标准中会使用到。
Automatic Bus-Off Management:用于设置是否使用自动离线管理功能 (ENABLE/DISABLE)，使用自动离线管理可以在出错时离线后适时自动恢复，不需要软件干预。
Automatic Wake-Up Mode:用于设置是否使用自动唤醒功能 (ENABLE/DISABLE)，使能自动唤醒功能后它会在监测到总线活动后自动唤醒。
Automatic Retransmission:用于设置是否使用自动重传功能 (ENABLE/DISABLE)，使用自动重传功能时，会一直发送报文直到成功为止。
Receive Fifo Locked Mode:用于设置是否使用锁定接收 FIFO(ENABLE/DISABLE)，锁定接收 FIFO 后，若FIFO 溢出时会丢弃新数据，否则在 FIFO 溢出时以新数据覆盖旧数据。
Transmit Fifo Priority:用于设置发送报文的优先级判定方法 (ENABLE/DISABLE)，使能时，以报文存入发送邮箱的先后顺序来发送，否则按照报文 ID 的优先级来发送。配置完这些结构体成员后，我们调用库函数 HAL_CAN_Init 即可把这些参数写入到 CAN 控制寄存器中，实现 CAN 的初始化

CAN通过控制器将二进制数据转换成差分信号
由CAN_H和CAN_L两根线接通网络





