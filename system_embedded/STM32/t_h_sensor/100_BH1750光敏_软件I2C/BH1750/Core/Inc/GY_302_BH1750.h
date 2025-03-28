
#ifndef __GY_302_BH1750_H__
#define __GY_302_BH1750_H__

#include "stm32f1xx_hal.h"
#include "stdio.h"

/*----------------------------------------------------------------------------------------------------------*/
//2023.10.14||Saturday||Sunny

//---������Ϣ
//����ʹ�õĵ��β���ģʽ������BH1750оƬ��GY-302ģ��
//����ʹ��ģ��IICͨѶ��ͨѶ������.c�ļ��е�һ����������
//ģ��SDA��Ϊ��©�������һ��һͨѶʱ������ʹ��������������ǽӶ���豸ʱ�������׷�����·
//����Ϊ��©���ʱ��Ӧ�����������GY302ģ����ʵ��
//ACKӦ���ź�--��ReadPin���SDA���ߵĵ�ƽ���ɣ������л�input
//GY302�ѽ�ADDR��GND
//������û�ж�BH1750���е��紦�����ڵ͹��Ŀ��ǣ��ڲ���Ƶ�������ʱ��ÿ�β�������Զ�GY302���е��紦��
//����ʵ�� --> void Get_LIght_Intensity(void){}�ڴ˺��������м���void BH1750_Power_OFF(void)����
//����ʹ��////response SDA_CheckDevice(uint8_t _Address);��ͨѶ�ӿڽ��м����������ɼ����ݺͶ�ȡ����

//---ʹ����֪
/*@@@@@@ �޸Ĳ�����������Ŀ����� @@@@@*/
//��main�е���Get_LIght_Intensity();���hal_delay����ʵ��ѭ���ɼ�
//��mian�е�whileǰ��ʼ��IO���� --> BH1750_SDA_SCL_init();
//��ʹ��usart���ض���printf,�ǵù�ѡ��͵���stdio.h;

/*@@@@@@ �˴��޸Ĳ���ģʽ ���ȼ������Ӧ����@@@@@*/
#define Measure_Mode                ONE_TIME_H_MODE

/*@@@@@@ �˴��޸Ķ���I2C�������ӵ�GPIO�˿�, ֻ��Ҫ�޸�����4�д��뼴������ı�SCL��SDA������ @@@@@*/
#define SCL_PORT             GPIOC                             /* SDA����PORT */
#define SDA_PORT             GPIOC                             /* SCL����PORT */
#define SCL_PIN              GPIO_PIN_7                        /* ���ӵ�SCLʱ���ߵ�GPIO */
#define SDA_PIN              GPIO_PIN_9                        /* ���ӵ�SDA�����ߵ�GPIO */
//�����������޸ģ�  __HAL_RCC_GPIOA/B/C/D_CLK_ENABLE();
#define SCL_PORT_ENABLE      __HAL_RCC_GPIOC_CLK_ENABLE();     /* SDA����PORTʹ�� */
#define SDA_PORT_ENABLE      __HAL_RCC_GPIOC_CLK_ENABLE();     /* SDA����PORTʹ�� */
/*----------------------------------------------------------------------------------------------------------*/

//BH1750�ĵ�ַ 
#define BH1750_Addr                   0x46       //7bit��ַ  �ӵ� 0100 011    ��VCCʱADDRȡ��

//BH1750ָ���� instruct
#define POWER_OFF                     0x00
#define POWER_ON                      0x01
#define MODULE_RESET                  0x07
#define CONTINUE_H_MODE               0x10       //���� 1     lx      120ms
#define CONTINUE_H_MODE2              0x11       //���� 0.5   lx      120ms
#define CONTINUE_L_MODE               0x13       //���� 4     lx      16ms
#define ONE_TIME_H_MODE               0x20       //���� 1     lx      120ms
#define ONE_TIME_H_MODE2              0x21       //���� 0.5   lx      120ms
#define ONE_TIME_L_MODE               0x23       //���� 4     lx      16ms

//�ֱ���	����ǿ�ȣ���λlx��=��High Byte  + Low Byte��/ 1.2 * ��������
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

#define SDA_Readstate     HAL_GPIO_ReadPin(SDA_PORT, SDA_PIN)         /* ��SDA����״̬ */
#define BH1750_WR    0                                                /* д����bit */
#define BH1750_RD    1                                                /* ������bit */

typedef enum  {ok = 0u, error1,error2,
                        error3,error4} response;                       //error1 ��λӦ�����   error2 Ѱַ+д ����
                                                                       //error3 д���������   error4 Ѱַ+�� ����

void BH1750_SDA_SCL_init(void);                            //ģ��IIC��IO��ʼ��
void SDA_Start(void);
void BH1750_Power_ON(void);                                //�ϵ�ָ��
void SDA_SendByte(uint8_t _ucByte);
uint8_t  SDA_ReadByte(void);
void Send_Ack(void);                                       //SLC������(խ)ʱ����SDA��ƽ״̬(������)  ACK=0  NADC=1
void Send_NAck(void);                                      //SLC������(խ)ʱ����SDA��ƽ״̬(������)  ACK=0  NADC=1
response SDA_WaitAck(void);                                //�ȴ�Ӧ��
response Send_measure(uint8_t Measure_mode);               //Ѱַ�����Ͳ���ģʽ
uint16_t Read_data(void);
void Get_LIght_Intensity(void);                            //��ȡ����ǿ�ȵ�ֵ
void SDA_Stop(void);
void BH1750_Power_OFF(void);                               //�ϵ�ָ��



////����Ŀδ�õ�
////void BH1750_RESET(void);
////response SDA_CheckDevice(uint8_t _Address);

#endif




