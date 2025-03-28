#ifndef __YL37_DHT11_H
#define __YL37_DHT11_H

#include "stm32f1xx_hal.h"
#include "usart.h"

/*----------------------------------------------------------------------------------------------------------*/
//2023.10.14||Saturday||sunny

//@���ܽ���
/*  YL47ģ���Ѿ���DHT11��DR�Ͻ���һ��������������Ӱ��ʱ��ֻҪVcc�������߾�Ϊ1*/
/*  ÿ�ζ�ȡ5*8=40bit����  byte1Ϊʪ������ byte2Ϊʪ��С�� byte3Ϊ�¶����� byte4Ϊ�¶�С�� byteΪУ���*/
/*  ��Ϊ���Ƚϵͣ�ֻ��ӡ��������*/
/*  ��ӡ���1 �������������¶Ⱥ�ʪ������*/
/*  ��ӡ���2 �������쳣_��λ�쳣��DHT11��Ӧ�쳣*/
/*  ��ӡ���3 �������쳣_����У���쳣  */

//@ʹ��˵��
/*  DR_init();�˺�����Ҫ��main��whileǰ���ã����г�ʼ��*/
/*  ��Ҫ����Զ���us��ʱ���������Q_delay_us();�Ĺ�������tim.c�ж��岢��tim.h������*/
/*  ��Ҫ��ӡ��򿪴��ڲ��ض���printf  */
/*  ��main---while����е���   DHT11_Start();����ʵ�ִ��ڴ�ӡ; Ĭ��Ƶ��Լ1Hz__DHT11_Start()�е�1000ms+200ms */
/*  ��*@@@@@���޸Ĳ�������Ӧ��Ŀ�����*/

 /*@@@@@@  ���ĺ궨�����趨��� DR���Ŷ�Ӧ��IO����  ��ʹ�ܸ����Ŷ�Ӧ��ģ�� @@@@@@*/
#define DATA_PORT           GPIOC 
#define DATA_PIN            GPIO_PIN_7
#define DATA_PORT_ENABLE    __HAL_RCC_GPIOA_CLK_ENABLE();
/*----------------------------------------------------------------------------------------------------------*/

#define DR_OUT_1        do{  DR_OUTinit();  HAL_GPIO_WritePin(DATA_PORT, DATA_PIN, GPIO_PIN_SET); }while(0);      //���1   
#define DR_OUT_0        do{  DR_OUTinit();  HAL_GPIO_WritePin(DATA_PORT, DATA_PIN, GPIO_PIN_RESET); }while(0);    //���0   
#define DR_IN           do{  DR_INPUTinit();  }while(0);                                                          //����ģʽ


typedef enum  {error1 = 0u, error2,ok} response;      //error1 ��λӦ�����      error2 ��λӦ������������У�����

void DR_init(void);                                   //GPIO��ʼ��
void DR_OUTinit(void);                                //PA7��Ϊ���  
void DR_INPUTinit(void);                              //PA7��Ϊ����
void DHT11_Rst(void);                                 //��λ
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
