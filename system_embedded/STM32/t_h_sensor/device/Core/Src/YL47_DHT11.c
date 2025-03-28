
/*  ʹ��ǰ�Ķ���Ӧ��  YL47_DHT11.h  */


#include "YL47_DHT11.h"
#include "tim.h"                                    //us��ʱ����ͷ�ļ�

uint8_t temperature;                                //�¶�
uint8_t humidity;                                   //ʪ��
uint8_t temp;
uint8_t humi; 
uint8_t rx_buf[5];


static GPIO_InitTypeDef GPIO_DATA = {0};

void DR_init(void)                                  //GPIO��ʼ��
{
    HAL_GPIO_WritePin(DATA_PORT,GPIO_PIN_7,GPIO_PIN_SET);
    DATA_PORT_ENABLE;
    GPIO_DATA.Pin = DATA_PIN;
    GPIO_DATA.Pull = GPIO_NOPULL;
    GPIO_DATA.Mode = GPIO_MODE_OUTPUT_PP;

    GPIO_DATA.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(DATA_PORT, &GPIO_DATA);
}

void DR_OUTinit(void)                               //PA7��Ϊ���  
{
    GPIO_DATA.Mode = GPIO_MODE_OUTPUT_PP;
    HAL_GPIO_Init(DATA_PORT, &GPIO_DATA);
}

void DR_INPUTinit(void)                             //PA7��Ϊ����
{
    GPIO_DATA.Mode = GPIO_MODE_INPUT;
    HAL_GPIO_Init(DATA_PORT, &GPIO_DATA);
}


void DHT11_Rst(void)                                //��λ
{
    DR_OUT_0;
    Q_delay_us(25000);                              //��������18ms
    DR_OUT_1;       
    Q_delay_us(30);                                 //��������20~40us
}


response DHT11_Check(void)
{   
    uint8_t retry=0;
    DR_IN;

    while (HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN)&&retry<90)//DHT11������ 80us
    {
        retry++;
        Q_delay_us(1);
    };
    if(retry>=90)
        return error1;                              //error1 ��λӦ�����
    
    retry=0;
    while (!HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN)&&retry<90)//DHT11���ͺ���ٴ����� 80us
    {
        retry++;
        Q_delay_us(1);
    };
    if(retry>=90)
        return error1;                              //error1 ��λӦ�����
    return ok;
}


uint8_t DHT11_Read_Bit(void)
{
    uint8_t retry=0;
    while(HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN)&&retry<100)//�ȴ���͵�ƽ
    {
        retry++;
        Q_delay_us(1);
    }
    retry=0;
    while(!HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN)&&retry<100)//�ȴ���ߵ�ƽ
    {
        retry++;
        Q_delay_us(1);
    }
    Q_delay_us(40);                                         //�ȴ�40us,���������27us��ʾ0,������70us��ʾ1
    if(HAL_GPIO_ReadPin(DATA_PORT, DATA_PIN))               //ȡ�м�ֵ40us���жϼ���
        return 1;                                           //error1 ��λӦ�����
    else
        return 0;
}

uint8_t DHT11_Read_Byte(void)                               //��ȡ1byte������
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

response DHT11_Read_Data(uint8_t *temp,uint8_t *humi,uint8_t *tem,uint8_t *hum)    //��ȡ1byte������
{
    uint8_t buf[5];
    uint8_t i;
    DHT11_Rst();
    if(DHT11_Check()==ok)
    {
        for(i=0;i<5;i++)                                                            //��ȡ40λ�ֽ�
        {
            buf[i]=DHT11_Read_Byte();
        }
        if((buf[0]+buf[1]+buf[2]+buf[3])==buf[4])                                   //У��
        {
            *humi=buf[0];
            *hum=buf[1];
            *temp=buf[2];
            *tem=buf[3];
            return ok;
        }
        else return error2;                                                       //error2 ����У�����
    }
    else return error1;                                                           //error1 ��λӦ�����
}


void DHT11_Start(void)                                                         //��ʼ��������ȡ
{
   uint8_t result=0;
   result= DHT11_Read_Data(&temperature,&humidity,&temp,&humi);

   if( result==ok)                                                            //���ݶ�ȡ����У��ɹ�
   {
        rx_buf[0]=temperature;
        rx_buf[1]=humidity;
//        printf("temperature=%d,humidity=%d\r\n",rx_buf[0],rx_buf[1]);
//                  //  HAL_GPIO_TogglePin(DATA_PORT,GPIO_PIN_8);               //����Ӵ������Ϊ������ʾ
        HAL_Delay(200);
   }
//   
//   if( result==error1)                                                        //���ݶ�ȡʧ��
//   {
////        printf("reset or response error1\n");
//        HAL_Delay(200);
//   }

//   if( result==error2)                                                        //���ݶ�ȡ�ɹ���У��ʧ��
//   {
////       printf("data check error2\n");
//       HAL_Delay(200);
//   }

////    HAL_Delay(1000);
}






