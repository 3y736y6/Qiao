/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
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

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define LED1_Pin GPIO_PIN_5
#define LED1_GPIO_Port GPIOE
#define AD7606_RD_Pin GPIO_PIN_5
#define AD7606_RD_GPIO_Port GPIOA
#define AD7606_DB7_Pin GPIO_PIN_6
#define AD7606_DB7_GPIO_Port GPIOA
#define AD7606_OS1_Pin GPIO_PIN_12
#define AD7606_OS1_GPIO_Port GPIOG
#define AD7606_CS_Pin GPIO_PIN_13
#define AD7606_CS_GPIO_Port GPIOG
#define AD7606_RANGE_Pin GPIO_PIN_14
#define AD7606_RANGE_GPIO_Port GPIOG
#define AD7606_BUSY_Pin GPIO_PIN_15
#define AD7606_BUSY_GPIO_Port GPIOG
#define AD7606_BUSY_EXTI_IRQn EXTI15_10_IRQn
#define AD7606_OS0_Pin GPIO_PIN_3
#define AD7606_OS0_GPIO_Port GPIOB
#define AD7606_CVAB_Pin GPIO_PIN_4
#define AD7606_CVAB_GPIO_Port GPIOB
#define LED0_Pin GPIO_PIN_5
#define LED0_GPIO_Port GPIOB
#define AD7606_OS2_Pin GPIO_PIN_6
#define AD7606_OS2_GPIO_Port GPIOB
#define AD7606_RST_Pin GPIO_PIN_7
#define AD7606_RST_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
