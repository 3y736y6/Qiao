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
#舵机
###90°，180°，270°舵机
20ms PWM周期
0.5(最小角度)~2.5ms(最大角度) 控制周期
###360°舵机
20ms PWM周期
0ms<--1.5ms(停止位)-->2.5ms
速度与PWM宽度有关
力矩与电压电流和力臂有关

###数字舵机与普通舵机的区别(控制上)
+ 普通舵机：需要连续不断地PWM信号输出控制，直至转动至对应角度
+ 数字舵机：只需要一个脉冲信号，PWM：start ~delay(20ms)~ stop，在舵机内部的控制板上，会将一个PWM信号细分成若干个控制信号
####状态机控制舵机的转动
```c
//数字舵机
    static uint16_t cnt=10;
    cnt++;
    HAL_Delay(200);
    if(cnt==10)
    {
        HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_4);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_4, 10);
        HAL_Delay(20);
        HAL_TIM_PWM_Stop(&htim3,TIM_CHANNEL_4);
    }
    if(cnt==20)
    {
        HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_4);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_4, 15);
        HAL_Delay(20);
        HAL_TIM_PWM_Stop(&htim3,TIM_CHANNEL_4);
    }
    if(cnt==30)
    {  
        HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_4);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_4, 25);
        HAL_Delay(30);
        HAL_TIM_PWM_Stop(&htim3,TIM_CHANNEL_4);
        cnt=0;
    }
//普通舵机
    static uint16_t cnt=0;
    cnt++;
    HAL_Delay(200);
    if(cnt==10)
    {
        HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_4);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_4, 10);
        HAL_Delay(5000);
        HAL_TIM_PWM_Stop(&htim3,TIM_CHANNEL_4);
    }
    if(cnt==20)
    {
        HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_4);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_4, 15);
        HAL_Delay(5000);
        HAL_TIM_PWM_Stop(&htim3,TIM_CHANNEL_4);
    }
    if(cnt==30)
    {  
        HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_4);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_4, 25);
        HAL_Delay(5000);    
        HAL_TIM_PWM_Stop(&htim3,TIM_CHANNEL_4);
        cnt=0;
    }
```