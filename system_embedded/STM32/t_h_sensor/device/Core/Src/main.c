/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

#include "YL47_DHT11.h"

#include "GY_302_BH1750.h"




#include "usart.h"
#include <string.h>



void Usart_SendString(uint8_t *str);

      
      void Usart_SendString(uint8_t *str);
      void Init_esp8266_01s(void);

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

      
        
        static uint8_t temp=0;
        static uint8_t hum=0;
        
        char RxBuffer[256];
        uint8_t aRxBuffer=0;
        uint8_t Rx_Cnt = 0;
    static    uint8_t phone_state=0;
    static    uint8_t curtain_state=0;


/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

    
  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_TIM3_Init();
  MX_TIM2_Init();
  MX_USART1_UART_Init();
  MX_USART2_UART_Init();
  /* USER CODE BEGIN 2 */
    HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_4);
    DR_init();
    BH1750_SDA_SCL_init();

    HAL_UART_Receive_IT(&huart2, (uint8_t *)&aRxBuffer, 1);  
    Init_esp8266_01s();

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

    DHT11_Start();
    Get_LIght_Intensity();
    temp=rx_buf[0];
    hum=rx_buf[1];

      
    printf("AT+MQTTPUB=0\,\"tophone\"\,\"{\\\"Temp\\\":%d\\\,\\\"Hum\\\":%d\\\,\\\"Light\\\":%d}\"\,0\,0\r\n",temp,hum,light);

    HAL_GPIO_TogglePin(GPIOA,GPIO_PIN_8);
      
    HAL_Delay(4000);
      






  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */


void Usart_SendString(uint8_t *str)
{
	unsigned int k=0;
  	do 
  	{
        HAL_UART_Transmit(&huart1,(uint8_t *)(str + k) ,1,1000);
        k++;
  	} while(*(str + k)!='\0');
    

}
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    
    if(huart->Instance == USART2)
    {
        RxBuffer[Rx_Cnt++] = aRxBuffer; 

        HAL_UART_Receive_IT(&huart2, (uint8_t *)&aRxBuffer, 1);
        
        if((RxBuffer[Rx_Cnt-1] == 0x0A)&&(RxBuffer[Rx_Cnt-2] == 0x0D)) 
        {
            if(RxBuffer[Rx_Cnt-4]=='1')
            {
                phone_state=1;
                if(phone_state!=curtain_state)   
                {
                    curtain_state=1;
                     HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_4);
                     __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_4,7);
                     HAL_Delay(7500);
                     HAL_TIM_PWM_Stop(&htim3, TIM_CHANNEL_4);
                }
            }
                
            if(RxBuffer[Rx_Cnt-4]=='0')
            {
                phone_state=0;
                if(phone_state!=curtain_state)
                {
                    curtain_state=0;
                    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_4);
                    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_4, 25);
                    HAL_Delay(6700);
                    HAL_TIM_PWM_Stop(&htim3, TIM_CHANNEL_4);
                }
            }
            
         //   HAL_UART_Transmit(&huart1, (uint8_t *)&RxBuffer, Rx_Cnt-1,0xFFFF);
            
            Rx_Cnt = 0;                
            memset(RxBuffer,0x00,sizeof(RxBuffer));
        }
    }
}








                
                



    void Init_esp8266_01s(void)
       {

      
uint8_t a[64]={"AT\r\n"};

uint8_t b[64]={"AT+RST\r\n"};

uint8_t c[64]={"AT+CWMODE=1\r\n"};

uint8_t d[64]={"AT+CWJAP=\"3y736y6\",\"zijipojie8\"\r\n"};

uint8_t e[64]={"AT+MQTTUSERCFG=0,1,\"ESP01s\",\"\",\"\",0,0,\"\"\r\n"};

uint8_t f[64]={"AT+MQTTCONN=0,\"broker.emqx.io\",1883,1\r\n"};

uint8_t g[64]={"AT+MQTTSUB=0,\"tocurtain\",1\r\n"};


        do{
            
        printf("%s",a);      //��ѯ to esp8266

        HAL_Delay(1000);

        printf("%s",b);

        HAL_Delay(3000);

        printf("%s",c);

        HAL_Delay(2000);

        printf("%s",d);
        HAL_Delay(3000);

        printf("%s",e);
        HAL_Delay(2000);

        printf("%s",f);
        HAL_Delay(5000);

        printf("%s",g);
        HAL_Delay(3000);
        
        
              
    }while(0);

}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
