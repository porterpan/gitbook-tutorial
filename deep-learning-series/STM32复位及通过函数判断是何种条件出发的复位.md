---
title: STM32复位及通过函数判断是何种条件出发的复位
date: 2018-11-11 17:07:55
categories:     
    skill    
tags: [C语言,嵌入式]
---

# 摘要

STM32F10xxx支持三种复位形式，分别为系统复位、上电复位和备份区域复位。本文将通过实际的代码来解释各种情况下，软、硬件导致芯片复位的判别和怎样采取措施。

<!-- more -->

## 一、系统复位

#### 系统复位将复位所有寄存器至它们的复位状态。 当发生以下任一事件时，产生一个系统复位：

* 1. NRST引脚上的低电平(外部复位) 2. 窗口看门狗计数终止(WWDG复位)
* 3. 独立看门狗计数终止(IWDG复位)
* 4. 软件复位(SW复位)
* 5. 低功耗管理复位 可通过查看RCC_CSR控制状态寄存器中的复位状态标志位识别复位事件来源。
软件复位通过将Cortex™-M3中断应用和复位控制寄存器中的SYSRESETREQ位置’1’，可实现软件复位。请参考Cortex™-M3技术参考手册获得进一步信息。

### 1.1 低功耗管理复位在以下两种情况下可产生低功耗管理复位：

* 1. 在进入待机模式时产生低功耗管理复位： 通过将用户选择字节中的nRST_STDBY位置’1’将使能该复位。这时，即使执行了进入待机模式的过程，系统将被复位而不是进入待机模式。
* 2. 在进入停止模式时产生低功耗管理复位： 通过将用户选择字节中的nRST_STOP位置’1’将使能该复位。这时，即使执行了进入停机模式的过程，系统将被复位而不是进入停机模式。 
关于用户选择字节的进一步信息，请参考STM32F10xxx闪存编程手册。

## 电源复位

#### 电源复位当以下事件中之一发生时，产生电源复位：

* 1. 上电/掉电复位(POR/PDR复位)
* 2. 从待机模式中返回 图4) 电源复位将复位除了备份区域外的所有寄存器。
(见图中复位源将最终作用于RESET引脚，并在复位过程中保持低电平。复位入口矢量被固定在地址0x0000_0004。

芯片内部的复位信号会在NRST引脚上输出，脉冲发生器保证每一个(外部或内部)复位源都能有至少20μs的脉冲延时；当NRST引脚被拉低产生外部复位时，它将产生复位脉冲。

![iqofJS.png](https://s1.ax1x.com/2018/11/11/iqofJS.png)

## 三、备份域复位

> 备份区域拥有两个专门的复位，它们只影响备份区域(见图4)。 当以下事件中之一发生时，产生备份区域复位。

* 1. 软件复位，备份区域复位可由设置备份域控制寄存器 (RCC_BDCR)(见6.3.9节)中的BDRST位产生。
* 2. 在VDD和VBAT两者掉电的前提下，VDD或VBAT上电将引发备份区域复位。

## 四、复位的标志位

[![iqohRg.md.png](https://s1.ax1x.com/2018/11/11/iqohRg.md.png)](https://imgchr.com/i/iqohRg)

## 五、复位标志位检索/判断什么原因导致的复位

标志位判断的代码由官方库中给定代码如下：

> FlagStatus RCC_GetFlagStatus(uint8_t RCC_FLAG)；//FlagStatus 分为SET和RESET两种；

```C

/**
  * @brief  Checks whether the specified RCC flag is set or not.
  * @param  RCC_FLAG: specifies the flag to check.
  *   
  *   For @b STM32_Connectivity_line_devices, this parameter can be one of the
  *   following values:
  *     @arg RCC_FLAG_HSIRDY: HSI oscillator clock ready
  *     @arg RCC_FLAG_HSERDY: HSE oscillator clock ready
  *     @arg RCC_FLAG_PLLRDY: PLL clock ready
  *     @arg RCC_FLAG_PLL2RDY: PLL2 clock ready      
  *     @arg RCC_FLAG_PLL3RDY: PLL3 clock ready                           
  *     @arg RCC_FLAG_LSERDY: LSE oscillator clock ready
  *     @arg RCC_FLAG_LSIRDY: LSI oscillator clock ready
  *     @arg RCC_FLAG_PINRST: Pin reset
  *     @arg RCC_FLAG_PORRST: POR/PDR reset
  *     @arg RCC_FLAG_SFTRST: Software reset
  *     @arg RCC_FLAG_IWDGRST: Independent Watchdog reset
  *     @arg RCC_FLAG_WWDGRST: Window Watchdog reset
  *     @arg RCC_FLAG_LPWRRST: Low Power reset
  * 
  *   For @b other_STM32_devices, this parameter can be one of the following values:        
  *     @arg RCC_FLAG_HSIRDY: HSI oscillator clock ready
  *     @arg RCC_FLAG_HSERDY: HSE oscillator clock ready
  *     @arg RCC_FLAG_PLLRDY: PLL clock ready
  *     @arg RCC_FLAG_LSERDY: LSE oscillator clock ready
  *     @arg RCC_FLAG_LSIRDY: LSI oscillator clock ready
  *     @arg RCC_FLAG_PINRST: Pin reset
  *     @arg RCC_FLAG_PORRST: POR/PDR reset
  *     @arg RCC_FLAG_SFTRST: Software reset
  *     @arg RCC_FLAG_IWDGRST: Independent Watchdog reset
  *     @arg RCC_FLAG_WWDGRST: Window Watchdog reset
  *     @arg RCC_FLAG_LPWRRST: Low Power reset
  *   
  * @retval The new state of RCC_FLAG (SET or RESET).
  */
FlagStatus RCC_GetFlagStatus(uint8_t RCC_FLAG)
{
  uint32_t tmp = 0;
  uint32_t statusreg = 0;
  FlagStatus bitstatus = RESET;
  /* Check the parameters */
  assert_param(IS_RCC_FLAG(RCC_FLAG));

  /* Get the RCC register index */
  tmp = RCC_FLAG >> 5;
  if (tmp == 1)               /* The flag to check is in CR register */
  {
    statusreg = RCC->CR;
  }
  else if (tmp == 2)          /* The flag to check is in BDCR register */
  {
    statusreg = RCC->BDCR;
  }
  else                       /* The flag to check is in CSR register */
  {
    statusreg = RCC->CSR;
  }

  /* Get the flag position */
  tmp = RCC_FLAG & FLAG_Mask;
  if ((statusreg & ((uint32_t)1 << tmp)) != (uint32_t)RESET)
  {
    bitstatus = SET;
  }
  else
  {
    bitstatus = RESET;
  }

  /* Return the flag status */
  return bitstatus;
}

```

当然判断完后，我们需要将复位类型的标志置位以防后期出现重复多次判断

> void RCC_ClearFlag(void)；//清除复位执行函数

代码原型如下:

```C
/**
  * @brief  Clears the RCC reset flags.
  * @note   The reset flags are: RCC_FLAG_PINRST, RCC_FLAG_PORRST, RCC_FLAG_SFTRST,
  *   RCC_FLAG_IWDGRST, RCC_FLAG_WWDGRST, RCC_FLAG_LPWRRST
  * @param  None
  * @retval None
  */
void RCC_ClearFlag(void)
{
  /* Set RMVF bit to clear the reset flags */
  RCC->CSR |= CSR_RMVF_Set;
}

``` 

* 在使用时，只需要执行如下语句即可：

```C
if(RCC_GetFlagStatus(RCC_FLAG_PORRST) != RESET)
        {
           //这是上电复位
        }
        else if (RCC_GetFlagStatus(RCC_FLAG_PINRST) != RESET)
        {
           //这是外部RST管脚复位
        }
        else if (RCC_GetFlagStatus(RCC_FLAG_SFTRST)!= RESET)
        {
           //这是外部RST管脚复位
        }        
        RCC_ClearFlag();//清除RCC中复位标志
```

## 六、STM32软件复位方法

在Cortex-M3权威指南中有这么一句话这里有一个要注意的问题：从SYSRESETREQ 被置为有效，到复位发生器执行复位命令，往往会有一个延时。在此延时期间，处理器仍然可以响应中断请求。但我们的本意往往是要让此次执行到此为止，不要再做任何其它事情了。所以，最好在发出复位请求前，先把FAULTMASK 置位。所以最好在将FAULTMASK 置位才万无一失。

```C
void mcuRestart(void)
{
　　__set_FAULTMASK(1); //关闭所有中断
　　NVIC_SystemReset(); //复位
｝
```