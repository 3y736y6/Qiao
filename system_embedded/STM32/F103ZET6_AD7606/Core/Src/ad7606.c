#include "gpio.h"
#include "spi.h"
#include "tim.h"
#include "ad7606.h"

static void AD7606Reset(void)
{
    /*! ___|-----|________  >= 50ns */
//    AD7606Rst_Low();
//    AD7606Rst_High();
//    for(int i = 10; i > 0; i--){
//        __NOP();//1000/168 ns = 5.85ns
//    }
//    AD7606Rst_Low();
	
	  AD7606Rst_Low(); 
		AD7606Rst_High();//Լ0.7us
		AD7606Rst_High();
		AD7606Rst_Low();
}

void AD7606Init(void)
{
    AD7606Cs_High();
    AD7606Reset();
}

void AD7606Start(void)
{
    HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_1);
}

void AD7606Stop(void)
{
    HAL_TIM_PWM_Stop(&htim3,TIM_CHANNEL_1);
    AD7606Cs_High();
}

void AD7606BusyIrqCallback(uint16_t *ad7606Val,uint8_t ad7606Chl)
{
    AD7606Cs_Low();
    HAL_SPI_Receive(&hspi1,(uint8_t *)ad7606Val,ad7606Chl,10000);
    AD7606Cs_High();
}
