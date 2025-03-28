
#ifndef __GY_302_BH1750_H__
#define __GY_302_BH1750_H__

#include "stm32f1xx_hal.h"
#include "stdio.h"

/*----------------------------------------------------------------------------------------------------------*/
//2023.10.14||Saturday||Sunny

//---例程信息
//例程使用的单次测量模式，基于BH1750芯片，GY-302模块
//例程使用模拟IIC通讯，通讯速率由.c文件中第一个函数决定
//模拟SDA口为开漏输出，在一对一通讯时，可以使用推挽输出，但是接多个设备时，推挽易发生短路
//设置为开漏输出时，应该外接上拉，GY302模块已实现
//ACK应答信号--用ReadPin检测SDA总线的电平即可，不用切换input
//GY302已将ADDR接GND
//例程中没有对BH1750进行掉电处理，出于低功耗考虑，在采样频率需求低时，每次采样后可以对GY302进行掉电处理
//具体实现 --> void Get_LIght_Intensity(void){}在此函数定义中加上void BH1750_Power_OFF(void)函数
//可以使用////response SDA_CheckDevice(uint8_t _Address);对通讯接口进行检查而不触发采集数据和读取数据

//---使用须知
/*@@@@@@ 修改参数以适配你的开发板 @@@@@*/
//在main中调用Get_LIght_Intensity();配合hal_delay可以实现循环采集
//在mian中的while前初始化IO引脚 --> BH1750_SDA_SCL_init();
//需使能usart并重定向printf,记得勾选库和调用stdio.h;

/*@@@@@@ 此处修改测量模式 精度计算会相应更改@@@@@*/
#define Measure_Mode                ONE_TIME_H_MODE

/*@@@@@@ 此处修改定义I2C总线连接的GPIO端口, 只需要修改下面4行代码即可任意改变SCL和SDA的引脚 @@@@@*/
#define SCL_PORT             GPIOC                             /* SDA所在PORT */
#define SDA_PORT             GPIOC                             /* SCL所在PORT */
#define SCL_PIN              GPIO_PIN_7                        /* 连接到SCL时钟线的GPIO */
#define SDA_PIN              GPIO_PIN_9                        /* 连接到SDA数据线的GPIO */
//下两行自行修改，  __HAL_RCC_GPIOA/B/C/D_CLK_ENABLE();
#define SCL_PORT_ENABLE      __HAL_RCC_GPIOC_CLK_ENABLE();     /* SDA所在PORT使能 */
#define SDA_PORT_ENABLE      __HAL_RCC_GPIOC_CLK_ENABLE();     /* SDA所在PORT使能 */
/*----------------------------------------------------------------------------------------------------------*/

//BH1750的地址 
#define BH1750_Addr                   0x46       //7bit地址  接地 0100 011    接VCC时ADDR取反

//BH1750指令码 instruct
#define POWER_OFF                     0x00
#define POWER_ON                      0x01
#define MODULE_RESET                  0x07
#define CONTINUE_H_MODE               0x10       //精度 1     lx      120ms
#define CONTINUE_H_MODE2              0x11       //精度 0.5   lx      120ms
#define CONTINUE_L_MODE               0x13       //精度 4     lx      16ms
#define ONE_TIME_H_MODE               0x20       //精度 1     lx      120ms
#define ONE_TIME_H_MODE2              0x21       //精度 0.5   lx      120ms
#define ONE_TIME_L_MODE               0x23       //精度 4     lx      16ms

//分辨率	光照强度（单位lx）=（High Byte  + Low Byte）/ 1.2 * 测量精度
#if ((Measure_Mode==CONTINUE_H_MODE2)|(Measure_Mode==ONE_TIME_H_MODE2))
#define Resolurtion		0.5
#define Wait_measure_Time    120
#elif ((Measure_Mode==CONTINUE_H_MODE)|(Measure_Mode==ONE_TIME_H_MODE))
#define Resolurtion		1
#define Wait_measure_Time    120
#elif ((Measure_Mode==CONTINUE_L_MODE)|(Measure_Mode==ONE_TIME_L_MODE))
#define Resolurtion		4
#define Wait_measure_Time    16
#endif

#define SCL_1  do{  HAL_GPIO_WritePin(SCL_PORT, SCL_PIN, GPIO_PIN_SET);}while(0);
#define SCL_0  do{  HAL_GPIO_WritePin(SCL_PORT, SCL_PIN, GPIO_PIN_RESET);}while(0);
#define SDA_1  do{  HAL_GPIO_WritePin(SDA_PORT, SDA_PIN, GPIO_PIN_SET);}while(0);
#define SDA_0  do{  HAL_GPIO_WritePin(SDA_PORT, SDA_PIN, GPIO_PIN_RESET);}while(0);

#define SDA_Readstate     HAL_GPIO_ReadPin(SDA_PORT, SDA_PIN)         /* 读SDA口线状态 */
#define BH1750_WR    0                                                /* 写控制bit */
#define BH1750_RD    1                                                /* 读控制bit */

typedef enum  {ok = 0u, error1,error2,
                        error3,error4} response;                       //error1 复位应答错误   error2 寻址+写 错误
                                                                       //error3 写入命令错误   error4 寻址+读 错误

void BH1750_SDA_SCL_init(void);                            //模拟IIC的IO初始化
void SDA_Start(void);
void BH1750_Power_ON(void);                                //上电指令
void SDA_SendByte(uint8_t _ucByte);
uint8_t  SDA_ReadByte(void);
void Send_Ack(void);                                       //SLC高脉冲(窄)时发送SDA电平状态(宽脉冲)  ACK=0  NADC=1
void Send_NAck(void);                                      //SLC高脉冲(窄)时发送SDA电平状态(宽脉冲)  ACK=0  NADC=1
response SDA_WaitAck(void);                                //等待应答
response Send_measure(uint8_t Measure_mode);               //寻址并发送测量模式
uint16_t Read_data(void);
void Get_LIght_Intensity(void);                            //读取光照强度的值
void SDA_Stop(void);
void BH1750_Power_OFF(void);                               //断电指令



////此项目未用到
////void BH1750_RESET(void);
////response SDA_CheckDevice(uint8_t _Address);

#endif




