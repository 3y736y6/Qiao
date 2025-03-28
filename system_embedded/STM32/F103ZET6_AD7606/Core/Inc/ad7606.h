/*
  ******************************************************************************
  * File Name          : ad7606.h
  * Description        : This file provides code for the ad7606 driver.
  * Author             : jackwang by jiawang16@foxmail.com
  * Date               : 2021-01-05
  ******************************************************************************
*/
#ifndef __AD_7606_H_
#define __AD_7606_H_

#ifdef __cplusplus
 extern "C" {
#endif

/*! -------------------------------------------------------------------------- */
/*! Include headers */
#include <stdint.h>


/*! -------------------------------------------------------------------------- */
/*! Public function declarations */
void AD7606Init(void);
void AD7606Start(void);
void AD7606Stop(void);
void AD7606BusyIrqCallback(uint16_t *da7606Val,uint8_t ad7606Chl);

#ifdef __cplusplus
}
#endif

#endif
/*! end of the file */
