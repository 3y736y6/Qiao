
/*  使用前阅读对应的  YL47_DHT11.h  */


#include "YL47_DHT11.h"
#include "tim.h"                                    //us延时函数头文件

uint8_t temperature;                                //温度
uint8_t humidity;                                   //湿度
uint8_t temp;
uint8_t humi; 
uint8_t rx_buf[5];


static GPIO_InitTypeDef GPIO_DATA = {0};

void DR_init(void)                                  //GPIO初始化
{
    HAL_GPIO_WritePin(DATA_PORT,GPIO_PIN_7,GPIO_PIN_SET);
    DATA_PORT_ENABLE;
    GPIO_DATA.Pin = DATA_PIN;
    GPIO_DATA.Pull = GPIO_NOPULL;
    GPIO_DATA.Mode = GPIO_MODE_OUTPUT_PP;

    GPIO_DATA.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(DATA_PORT, &GPIO_DATA);
}

void DR_OUTinit(void)                               //PA7改为输出  
{
    GPIO_DATA.Mode = GPIO_MODE_OUTPUT_PP;
    HAL_GPIO_Init(DATA_PORT, &GPIO_DATA);
}

void DR_INPUTinit(void)                             //PA7改为输入
{
    GPIO_DATA.Mode = GPIO_MODE_INPUT;
    HAL_GPIO_Init(DATA_PORT, &GPIO_DATA);
}


void DHT11_Rst(void)                                //复位
{
    DR_OUT_0;
    Q_delay_us(25000);                              //拉低至少18ms
    DR_OUT_1;       
    Q_delay_us(30);                                 //主机拉高20~40us
}


response DHT11_Check(void)
{   
    uint8_t retry=0;
    DR_IN;

    while (HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN)&&retry<90)//DHT11会拉低 80us
    {
        retry++;
        Q_delay_us(1);
    };
    if(retry>=90)
        return error1;                              //error1 复位应答错误
    
    retry=0;
    while (!HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN)&&retry<90)//DHT11拉低后会再次拉高 80us
    {
        retry++;
        Q_delay_us(1);
    };
    if(retry>=90)
        return error1;                              //error1 复位应答错误
    return ok;
}


uint8_t DHT11_Read_Bit(void)
{
    uint8_t retry=0;
    while(HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN)&&retry<100)//等待变低电平
    {
        retry++;
        Q_delay_us(1);
    }
    retry=0;
    while(!HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN)&&retry<100)//等待变高电平
    {
        retry++;
        Q_delay_us(1);
    }
    Q_delay_us(40);                                         //等待40us,输出高脉冲27us表示0,高脉冲70us表示1
    if(HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN))               //取中间值40us做判断即可
        return 1;                                           //error1 复位应答错误
    else
        return 0;
}

uint8_t DHT11_Read_Byte(void)                               //读取1byte并返回
{        
    uint8_t i,dat;
    dat=0;
    for (i=0;i<8;i++) 
    {
        dat<<=1; 
        dat|=DHT11_Read_Bit();
    } 
    return dat;
}

response DHT11_Read_Data(uint8_t *temp,uint8_t *humi,uint8_t *tem,uint8_t *hum)    //读取1byte并返回
{
    uint8_t buf[5];
    uint8_t i;
    DHT11_Rst();
    if(DHT11_Check()==ok)
    {
        for(i=0;i<5;i++)                                                            //读取40位字节
        {
            buf[i]=DHT11_Read_Byte();
        }
        if((buf[0]+buf[1]+buf[2]+buf[3])==buf[4])                                   //校验
        {
            *humi=buf[0];
            *hum=buf[1];
            *temp=buf[2];
            *tem=buf[3];
            return ok;
        }
        else return error2;                                                       //error2 数据校验错误
    }
    else return error1;                                                           //error1 复位应答错误
}


void DHT11_Start(void)                                                         //开始测量并读取
{
   uint8_t result=0;
   result= DHT11_Read_Data(&temperature,&humidity,&temp,&humi);

   if( result==ok)                                                            //数据读取并且校验成功
   {
        rx_buf[0]=temperature;
        rx_buf[1]=humidity;
//        printf("temperature=%d,humidity=%d\r\n",rx_buf[0],rx_buf[1]);
//                  //  HAL_GPIO_TogglePin(DATA_PORT,GPIO_PIN_8);               //可添加此语句作为运行显示
        HAL_Delay(200);
   }
//   
//   if( result==error1)                                                        //数据读取失败
//   {
////        printf("reset or response error1\n");
//        HAL_Delay(200);
//   }

//   if( result==error2)                                                        //数据读取成功，校验失败
//   {
////       printf("data check error2\n");
//       HAL_Delay(200);
//   }

////    HAL_Delay(1000);
}






