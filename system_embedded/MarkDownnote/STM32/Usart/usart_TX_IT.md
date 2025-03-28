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
#Usart
```C
HAL_UART_Transmit_IT(UART_HandleTypeDef *huart, const uint8_t *pData, uint16_t Size)
```

####parameter
1. huart：指向UART句柄结构体的指针，用于指定要使用的UART外设。
2. pData：指向要发送数据缓冲区的指针，可以是uint8_t类型或uint16_t类型的数据。
3. Size：要发送的数据大小，以数据元素（uint8_t或uint16_t）的数量表示。
####return
HAL_StatusTypeDef类型的返回值，表示函数的执行状态。可能的返回值包括：
* HAL_OK：发送操作已成功启动。
* HAL_BUSY：当前有正在进行的发送操作。
* HAL_ERROR：传入的参数不合法。
####function:以中断模式发送数据。
+ 函数会检查UART的状态，如果当前有正在进行的发送操作，则返回忙碌状态。
+ 然后，它会检查传入的数据缓冲区指针和数据大小是否合法，如果不合法，则返回错误状态。
+ 如果参数合法，函数会设置UART句柄结构体中的成员变量，并根据UART的FIFO模式和数据长度选择相应的中断服务程序的函数指针，并使能相应的中断。
  + 根据UART的FIFO模式和数据长度，函数选择相应的中断服务程序的函数指针，并使能相应的中断。如果FIFO模式使能，函数将使能TX FIFO阈值中断；如果FIFO模式未使能，函数将使能发送数据寄存器空中断。
  
##源码
```c
HAL_StatusTypeDef HAL_UART_Transmit_IT(UART_HandleTypeDef *huart, const uint8_t *pData, uint16_t Size)
{
  /* Check that a Tx process is not already ongoing */
  if (huart->gState == HAL_UART_STATE_READY)  //  检查是否ready(空闲)，不是则返回HAL_BUSY
  {
    if ((pData == NULL) || (Size == 0U))      //检查传入指针是否为NUll或缓存空间大小是否为0
    {
      return HAL_ERROR;
    }

    /* In case of 9bits/No Parity transfer在9bit无奇偶校验情况下 , pData buffer provided as input parameter
       should be aligned on a u16 frontier  (pData buffer)作为传入参数，应该在u16边界对齐, as data to be filled into TDR will be handled through a u16 cast.因为被填充到TDR的数据要通过u16的cast(投射，铸造--发送器)处理*/
    
    if ((huart->Init.WordLength == UART_WORDLENGTH_9B) && (huart->Init.Parity == UART_PARITY_NONE))
    {
      if ((((uint32_t)pData) & 1U) != 0U)     //检查数据缓冲区pData是否按照u16的边界对齐
      {
        return  HAL_ERROR;
      }
    }

    huart->pTxBuffPtr  = pData;
    huart->TxXferSize  = Size;
    huart->TxXferCount = Size;
    huart->TxISR       = NULL;

    huart->ErrorCode = HAL_UART_ERROR_NONE;
    huart->gState = HAL_UART_STATE_BUSY_TX;

    /* Configure Tx interrupt processing */
    if (huart->FifoMode == UART_FIFOMODE_ENABLE)
    {
      /* Set the Tx ISR function pointer according to the data word length */
      if ((huart->Init.WordLength == UART_WORDLENGTH_9B) && (huart->Init.Parity == UART_PARITY_NONE))
      {
        huart->TxISR = UART_TxISR_16BIT_FIFOEN;
      }
      else
      {
        huart->TxISR = UART_TxISR_8BIT_FIFOEN;
      }

      /* Enable the TX FIFO threshold interrupt */
      ATOMIC_SET_BIT(huart->Instance->CR3, USART_CR3_TXFTIE);
    }
    else
    {
      /* Set the Tx ISR function pointer according to the data word length */
      if ((huart->Init.WordLength == UART_WORDLENGTH_9B) && (huart->Init.Parity == UART_PARITY_NONE))
      {
        huart->TxISR = UART_TxISR_16BIT;
      }
      else
      {
        huart->TxISR = UART_TxISR_8BIT;
      }

      /* Enable the Transmit Data Register Empty interrupt */
      ATOMIC_SET_BIT(huart->Instance->CR1, USART_CR1_TXEIE_TXFNFIE);
    }

    return HAL_OK;
  }
  else
  {
    return HAL_BUSY;
  }
}

```

