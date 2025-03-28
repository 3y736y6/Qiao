#ifndef __YL37_DHT11_H
#define __YL37_DHT11_H

#include "stm32f1xx_hal.h"
#include "usart.h"

/*----------------------------------------------------------------------------------------------------------*/
//2023.10.14||Saturday||sunny

//@功能介绍
/*  YL47模块已经将DHT11的DR上接了一个上拉，无其他影响时，只要Vcc接上总线就为1*/
/*  每次读取5*8=40bit数据  byte1为湿度整数 byte2为湿度小数 byte3为温度整数 byte4为温度小数 byte为校验和*/
/*  因为精度较低，只打印整数部分*/
/*  打印结果1 ：运行正常，温度和湿度整数*/
/*  打印结果2 ：运行异常_复位异常或DHT11相应异常*/
/*  打印结果3 ：运行异常_数据校验异常  */

//@使用说明
/*  DR_init();此函数需要在main中while前调用，进行初始化*/
/*  需要添加自定义us延时函数以完成Q_delay_us();的工作，在tim.c中定义并在tim.h中声明*/
/*  需要打印需打开串口并重定义printf  */
/*  在main---while语句中调用   DHT11_Start();即可实现串口打印; 默认频率约1Hz__DHT11_Start()中的1000ms+200ms */
/*  在*@@@@@处修改参数以适应你的开发板*/

 /*@@@@@@  更改宏定义以设定你的 DR引脚对应的IO引脚  及使能该引脚对应的模块 @@@@@@*/
#define DATA_PORT           GPIOC 
#define DATA_PIN            GPIO_PIN_7
#define DATA_PORT_ENABLE    __HAL_RCC_GPIOA_CLK_ENABLE();
/*----------------------------------------------------------------------------------------------------------*/

#define DR_OUT_1        do{  DR_OUTinit();  HAL_GPIO_WritePin(DATA_PORT, DATA_PIN, GPIO_PIN_SET); }while(0);      //输出1   
#define DR_OUT_0        do{  DR_OUTinit();  HAL_GPIO_WritePin(DATA_PORT, DATA_PIN, GPIO_PIN_RESET); }while(0);    //输出0   
#define DR_IN           do{  DR_INPUTinit();  }while(0);                                                          //输入模式


typedef enum  {error1 = 0u, error2,ok} response;      //error1 复位应答错误      error2 复位应答正常，数据校验错误

void DR_init(void);                                   //GPIO初始化
void DR_OUTinit(void);                                //PA7改为输出  
void DR_INPUTinit(void);                              //PA7改为输入
void DHT11_Rst(void);                                 //复位
response DHT11_Check(void);
uint8_t DHT11_Read_Bit(void);
uint8_t DHT11_Read_Byte(void);
response DHT11_Read_Data(uint8_t *temp,uint8_t *humi,uint8_t *tem,uint8_t *hum);
void DHT11_Start(void);


extern uint8_t temperature;         
extern uint8_t humidity; 
extern uint8_t temp;         
extern uint8_t humi; 
extern uint8_t rx_buf[5];



#endif
