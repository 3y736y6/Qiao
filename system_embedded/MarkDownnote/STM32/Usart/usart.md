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
```c
/*****************  发送字符串 **********************/
void Usart_SendString(uint8_t *pData)
{
	unsigned int k=0;
  do 
  {
    HAL_UART_Transmit(&UartHandle,(uint8_t *)(pData + k) ,1,1000);
    k++;
  } while(*(str + k)!='\0');//k传下来后值增加1，也就是上一个字符传完后，判断下一个字符是否为'\0'
}
//重定向，记得魔棒使用MicroLib，应用stdio.h
int fputc(int ch, FILE *f)
{
	HAL_UART_Transmit(&UartHandle, (uint8_t *)&ch, 1, 1000);	
	return (ch);
}

int fgetc(FILE *f)
{		
	int ch;
	HAL_UART_Receive(&UartHandle, (uint8_t *)&ch, 1, 1000);	
	return (ch);
}
```
```
uint8_t data[128]={"AT+MQTTPUB=0\,\"tophone\"\,\"{\\\"Temp\\\":20\\\,\\\"Hum\\\":10\\\,\\\"Light\\\":99}\"\,0\,0\r\n"};
printf("AT+MQTTPUB=0\,\"tophone\"\,\"{\\\"Temp\\\":%d\\\,\\\"Hum\\\":%d\\\,\\\"Light\\\":%d}\"\,0\,0\r\n",temp,hum,light);
注意字符的转义
低放低，高放高  -->ARM小端
串口助手，勾选发送新行  \r\n  会使得发的数据比原本的数据大(一个字符？)
```