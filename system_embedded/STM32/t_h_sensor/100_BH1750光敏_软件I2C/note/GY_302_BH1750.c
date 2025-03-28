//###阅读对应.h文件

#include "GY_302_BH1750.h"

static  GPIO_InitTypeDef GPIO_InitStruct = {0};

static void i2c_Delay(void)                 //总线频率最大500khz
{
    for (	uint8_t i = 0; i < 10; i++);    //修改i以获得不同时钟频率
}

/*　
    通过逻辑分析仪测试
    在工作条件为---CPU主频72MHz ，MDK编译环境1级优化下：
    循环次数为10时，SCL频率 = 205KHz 
    循环次数为7时，SCL频率 = 347KHz， SCL高电平时间1.5us，SCL低电平时间2.87us 
    循环次数为5时，SCL频率 = 421KHz， SCL高电平时间1.25us，SCL低电平时间2.375us 
*/

void SDA_Start(void)              /* 当SCL高电平时，SDA出现一个下跳沿表示I2C总线启动信号 */
{
	SDA_1;
	SCL_1;
	i2c_Delay();
	SDA_0;
	i2c_Delay();
	SCL_0;
	i2c_Delay();
}


void SDA_Stop(void)              /* 当SCL高电平时，SDA出现一个上跳沿表示I2C总线停止信号 */
{
	SDA_0;
	SCL_1;
	i2c_Delay();
	SDA_1;
}


response SDA_WaitAck(void)       //SLC高脉冲(窄)时读取SDA电平状态(宽脉冲)  ACK=0  NADC=1
{

    SDA_1;                       /* CPU释放SDA总线 */
    i2c_Delay();
    SCL_1;                       /* CPU驱动SCL = 1, 此时器件会返回ACK应答 */
    i2c_Delay();
    if (SDA_Readstate)           /* CPU读取SDA口线状态 ACK=0*/
    { 
        SCL_0;
        i2c_Delay();
        return error1;          /* 返回应答错误 */
    }
    else
    {
        SCL_0;
        i2c_Delay();
        return ok;
    }
}


void Send_Ack(void)              //SLC高脉冲(窄)时发送SDA电平状态(宽脉冲)  ACK=0  NADC=1
{
    SDA_0;                       /* CPU驱动SDA = 0 */
    i2c_Delay();
    SCL_1;                       /* CPU产生1个时钟 */
    i2c_Delay();
    SCL_0;
    i2c_Delay();
    SDA_1;                       /* CPU释放SDA总线 */
}

void Send_NAck(void)             //SLC高脉冲(窄)时发送SDA电平状态(宽脉冲)  ACK=0  NADC=1
{
    SDA_1;                       /* CPU驱动SDA = 1 */
    i2c_Delay();
    SCL_1;                       /* CPU产生1个时钟 */
    i2c_Delay();
    SCL_0;
    i2c_Delay();
}



void SDA_SendByte(uint8_t byte)  //SCL为高脉冲时，读取   要求读取时SDA信号稳定 即SDA的脉冲(高1或低0)宽度要大于SDA
{
    uint8_t i;
    for (i = 0; i < 8; i++)
    {
        if(byte & 0x80)         //MSB发送
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
            SDA_1;              // 释放总线
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

void BH1750_Power_ON(void)                            //BH1750s上电
{
    Send_measure(POWER_ON);
}


void BH1750_Power_OFF(void)                           //BH1750s断电
{
    Send_measure(POWER_OFF);
}



                                                     //访问设备并开始采样 成功ok失败error1
response Send_measure(uint8_t command)               //BH1750写一个字节  
{
    SDA_Start();
    SDA_SendByte(BH1750_Addr|BH1750_WR);             //发送写地址
    if(SDA_WaitAck()==error1)
        return error2;                               //写入寻址错误
    SDA_SendByte(command);                           //发送控制命令
    if(SDA_WaitAck()==error1)
        return error3;                               //写入命令错误
    SDA_Stop();
    return ok;
}

                                                     //开始读取 成功ok失败error2
uint16_t Read_data(void)
{
    uint16_t receive_data=0; 
    SDA_Start();

    SDA_SendByte(BH1750_Addr|BH1750_RD);              //发送读地址
    if(SDA_WaitAck()==error1)
        return error4;                                //读取寻址错误
    receive_data=SDA_ReadByte();                      //读取高八位
    Send_Ack();
    receive_data=receive_data<<8|SDA_ReadByte();      //读取低八位
   // Send_NAck();
    SDA_Stop(); 
    return receive_data;                              //返回读取到的数据
}


                                                      //获取光照强度
void Get_LIght_Intensity(void)
{   
    uint16_t databuf=0,state=0;
    BH1750_Power_ON();  
    state=Send_measure(Measure_Mode);                                             //开始测量
    switch(state)
    {        
        case error2 :printf("error2 --> address+write error");break;              //寻址写入错误
        case error3 :printf("error3 --> write_command error");break;              //写入命令错误
    }
    HAL_Delay(Wait_measure_Time);                                                 //等待测量完毕
    
    databuf=Read_data();                                                          //读取数据
    if(databuf!=error4)
        printf( "%f    lx\n",(float)(databuf/1.2f*Resolurtion));                  //读取正常返回数值
    else 
        printf ("error4 --> address+read error");
}

void BH1750_SDA_SCL_init(void)                                                    //软件模拟IIC,IO设置
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


////未用到此功能

////void BH1750_RESET(void)                              //BH1750复位   仅在上电时有效
////{
////	Send_measure(MODULE_RESET);
////}


////response SDA_CheckDevice(uint8_t _Address)
////{
////    uint8_t checkAck;
////    SDA_Start();                                    /* 发送启动信号 */
////    SDA_SendByte(_Address | BH1750_WR);             /* 发送设备地址+读写控制bit（0 = w， 1 = r) bit7 先传 */
////    return SDA_WaitAck();
////}



