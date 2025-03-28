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
#TIM
####GPIO的频率
在CPU_72Mhz ,gpio_low_speed情况下， gpio_write_pin_reset = 50ns,gpio_write_pin_set = 70ns
GPIO_low_middle_high_Speed --> 10Mhz，20Mhz，50Mhz

####CPU运行
F1系列无FPU，无法实现硬件运算浮点数，只能靠cpu进行少量的浮点运算。

####TIM_us延时  
delay_us(1)；          大约1.3us
delay_us(2);	大约2.3us
delay_us(3);	大约3.3us     即函数语句本身需要执行300ns


```c
方法二
    htim2.Init.Prescaler         = 72-1;        //每次1us
    htim2.Init.Period            = 0;          
    htim2.Init.CounterMode       = TIM_COUNTERMODE_UP;   

void us_timer_delay(uint16_t t)
{
    uint16_t counter = 0;
    __HAL_TIM_SET_AUTORELOAD(&htim2, t);	      //设定计数值Period	
    __HAL_TIM_SET_COUNTER(&htim2, counter);     //计数器复位
    HAL_TIM_Base_Start(&htim2);                 //定时器开始计数
    while(counter != t)
    {
        counter = __HAL_TIM_GET_COUNTER(&htim2);
    }
    HAL_TIM_Base_Stop(&htim2);
}
方法一：
    htim2.Init.Prescaler = 71;
    htim2.Init.Period = 65535;
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;

void Q_delay_us(uint32_t nus)
{
 
    uint16_t  differ = 0xffff-nus-5;   //离计数值上限Period远一点，避免错误
    __HAL_TIM_SetCounter(&htim2,differ);              //设初值=上限-nus-5
    HAL_TIM_Base_Start(&htim2);
    while( differ<0xffff-5)
    {
        differ = __HAL_TIM_GetCounter(&htim2);   //设上限为65535-5，从 65532-nus-5 开始向上计数 
    };
    HAL_TIM_Base_Stop(&htim2);
}

```