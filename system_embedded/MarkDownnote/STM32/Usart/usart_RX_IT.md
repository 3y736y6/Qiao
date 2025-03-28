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
#Uart_IT
```c
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) 
{
    自定义语句
}
---实例
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    uint8_t Rx_Cnt=0;
    char RxBuffer[256];
    uint8_t aRxBuffer=0;
    if(huart->Instance == USART2)
    {
        RxBuffer[Rx_Cnt++] = aRxBuffer; 
        //接收到的第一个数据放入RxBffer[0]
        HAL_UART_Receive_IT(&huart2, (uint8_t *)&aRxBuffer, 1);
        //开始执行第二个字节数据接收中断

        if((RxBuffer[Rx_Cnt-1] == 0x0A)&&(RxBuffer[Rx_Cnt-2] == 0x0D)) 
        //检查当前位是否为\n且上一位是否为\r
        //即检查0x0D 0x0A -->\r\n    检查到结束标志，则该帧数据包接收完毕，重置cnt开始接收下一个数据包
        {
            HAL_UART_Transmit(&huart1, (uint8_t *)&RxBuffer, Rx_Cnt-1,0xFFFF);    
            Rx_Cnt = 0;                
        }
    }
}
//以上为每次接收一个数据，循环接收
//若知道数据长度，可以指定接收数据大小x，例如x=5
        HAL_UART_Receive_IT(&huart2, (uint8_t *)&aRxBuffer, 5);
        当接收到数据字节总数=5时，产生一次中断，
        若第一次接收3个，第二次接收4个，则前3+2个产生中断，(后两个进入下一次中断？)
```
1. 使用接收中断 HAL_UART_Receive_IT
2. 接收到消息-->中断产生-->执行回调函数
3. 进入自定义的HAL_UART_RxCpltCallback开始执行 
    + HAL_UART_RxCpltCallback 函数是在中断上下文中执行的，因此应该尽量保持它的执行时间短，避免执行耗时操作。
    + 如果你希望处理多个字符，而不仅仅是一个字符，你可以在 HAL_UART_RxCpltCallback 函数中使用循环来处理多个接收到的字符。
    + 确保接收缓冲区足够大以容纳所有接收到的字符，并进行边界检查，以防止数据溢出。
4. 需要在回调函数中再次开启中断，保证数据能够多级进行中断接收。

end
