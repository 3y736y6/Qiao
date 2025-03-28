//###�Ķ���Ӧ.h�ļ�

#include "GY_302_BH1750.h"

static  GPIO_InitTypeDef GPIO_InitStruct = {0};

static void i2c_Delay(void)                 //����Ƶ�����500khz
{
    for (	uint8_t i = 0; i < 10; i++);    //�޸�i�Ի�ò�ͬʱ��Ƶ��
}

/*��
    ͨ���߼������ǲ���
    �ڹ�������Ϊ---CPU��Ƶ72MHz ��MDK���뻷��1���Ż��£�
    ѭ������Ϊ10ʱ��SCLƵ�� = 205KHz 
    ѭ������Ϊ7ʱ��SCLƵ�� = 347KHz�� SCL�ߵ�ƽʱ��1.5us��SCL�͵�ƽʱ��2.87us 
    ѭ������Ϊ5ʱ��SCLƵ�� = 421KHz�� SCL�ߵ�ƽʱ��1.25us��SCL�͵�ƽʱ��2.375us 
*/

void SDA_Start(void)              /* ��SCL�ߵ�ƽʱ��SDA����һ�������ر�ʾI2C���������ź� */
{
	SDA_1;
	SCL_1;
	i2c_Delay();
	SDA_0;
	i2c_Delay();
	SCL_0;
	i2c_Delay();
}


void SDA_Stop(void)              /* ��SCL�ߵ�ƽʱ��SDA����һ�������ر�ʾI2C����ֹͣ�ź� */
{
	SDA_0;
	SCL_1;
	i2c_Delay();
	SDA_1;
}


response SDA_WaitAck(void)       //SLC������(խ)ʱ��ȡSDA��ƽ״̬(������)  ACK=0  NADC=1
{

    SDA_1;                       /* CPU�ͷ�SDA���� */
    i2c_Delay();
    SCL_1;                       /* CPU����SCL = 1, ��ʱ�����᷵��ACKӦ�� */
    i2c_Delay();
    if (SDA_Readstate)           /* CPU��ȡSDA����״̬ ACK=0*/
    { 
        SCL_0;
        i2c_Delay();
        return error1;          /* ����Ӧ����� */
    }
    else
    {
        SCL_0;
        i2c_Delay();
        return ok;
    }
}


void Send_Ack(void)              //SLC������(խ)ʱ����SDA��ƽ״̬(������)  ACK=0  NADC=1
{
    SDA_0;                       /* CPU����SDA = 0 */
    i2c_Delay();
    SCL_1;                       /* CPU����1��ʱ�� */
    i2c_Delay();
    SCL_0;
    i2c_Delay();
    SDA_1;                       /* CPU�ͷ�SDA���� */
}

void Send_NAck(void)             //SLC������(խ)ʱ����SDA��ƽ״̬(������)  ACK=0  NADC=1
{
    SDA_1;                       /* CPU����SDA = 1 */
    i2c_Delay();
    SCL_1;                       /* CPU����1��ʱ�� */
    i2c_Delay();
    SCL_0;
    i2c_Delay();
}



void SDA_SendByte(uint8_t byte)  //SCLΪ������ʱ����ȡ   Ҫ���ȡʱSDA�ź��ȶ� ��SDA������(��1���0)���Ҫ����SDA
{
    uint8_t i;
    for (i = 0; i < 8; i++)
    {
        if(byte & 0x80)         //MSB����
        {
            SDA_1;
        }
        else
        {
            SDA_0;
        }
        i2c_Delay();
        SCL_1;
        i2c_Delay();
        SCL_0;
        if (i == 7)
            SDA_1;              // �ͷ�����
        byte <<= 1;
        i2c_Delay();
    }
}


uint8_t SDA_ReadByte(void)
{
    uint8_t i;
    uint8_t value;
    value = 0;
    for (i = 0; i < 8; i++)
    {
        value <<= 1;
        SCL_1;
        i2c_Delay();
        if (SDA_Readstate)
        {
            value++;
        }
        SCL_0;
        i2c_Delay();
    }
    return value;
}

void BH1750_Power_ON(void)                            //BH1750s�ϵ�
{
    Send_measure(POWER_ON);
}


void BH1750_Power_OFF(void)                           //BH1750s�ϵ�
{
    Send_measure(POWER_OFF);
}



                                                     //�����豸����ʼ���� �ɹ�okʧ��error1
response Send_measure(uint8_t command)               //BH1750дһ���ֽ�  
{
    SDA_Start();
    SDA_SendByte(BH1750_Addr|BH1750_WR);             //����д��ַ
    if(SDA_WaitAck()==error1)
        return error2;                               //д��Ѱַ����
    SDA_SendByte(command);                           //���Ϳ�������
    if(SDA_WaitAck()==error1)
        return error3;                               //д���������
    SDA_Stop();
    return ok;
}

                                                     //��ʼ��ȡ �ɹ�okʧ��error2
uint16_t Read_data(void)
{
    uint16_t receive_data=0; 
    SDA_Start();

    SDA_SendByte(BH1750_Addr|BH1750_RD);              //���Ͷ���ַ
    if(SDA_WaitAck()==error1)
        return error4;                                //��ȡѰַ����
    receive_data=SDA_ReadByte();                      //��ȡ�߰�λ
    Send_Ack();
    receive_data=receive_data<<8|SDA_ReadByte();      //��ȡ�Ͱ�λ
   // Send_NAck();
    SDA_Stop(); 
    return receive_data;                              //���ض�ȡ��������
}


                                                      //��ȡ����ǿ��
void Get_LIght_Intensity(void)
{   
    uint16_t databuf=0,state=0;
    BH1750_Power_ON();  
    state=Send_measure(Measure_Mode);                                             //��ʼ����
    switch(state)
    {        
        case error2 :printf("error2 --> address+write error");break;              //Ѱַд�����
        case error3 :printf("error3 --> write_command error");break;              //д���������
    }
    HAL_Delay(Wait_measure_Time);                                                 //�ȴ��������
    
    databuf=Read_data();                                                          //��ȡ����
    if(databuf!=error4)
        printf( "%f    lx\n",(float)(databuf/1.2f*Resolurtion));                  //��ȡ����������ֵ
    else 
        printf ("error4 --> address+read error");
}

void BH1750_SDA_SCL_init(void)                                                    //���ģ��IIC,IO����
{

  SCL_PORT_ENABLE;
  SDA_PORT_ENABLE;

  HAL_GPIO_WritePin(SCL_PORT, SCL_PIN|SDA_PIN, GPIO_PIN_SET);

  GPIO_InitStruct.Pin = SCL_PIN;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(SCL_PORT, &GPIO_InitStruct);
    
    
  GPIO_InitStruct.Pin = SDA_PIN;
  HAL_GPIO_Init(SDA_PORT, &GPIO_InitStruct);
  SDA_Stop();
}


////δ�õ��˹���

////void BH1750_RESET(void)                              //BH1750��λ   �����ϵ�ʱ��Ч
////{
////	Send_measure(MODULE_RESET);
////}


////response SDA_CheckDevice(uint8_t _Address)
////{
////    uint8_t checkAck;
////    SDA_Start();                                    /* ���������ź� */
////    SDA_SendByte(_Address | BH1750_WR);             /* �����豸��ַ+��д����bit��0 = w�� 1 = r) bit7 �ȴ� */
////    return SDA_WaitAck();
////}



