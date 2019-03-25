---
title: STM32串口通信配置（USART1+USART2+USART3+UART4）
date: 2018-11-11 17:22:27
categories:     
    skill   
tags: [C语言,嵌入式]
---

# 摘要：

本文是通过分享几个通用的串口函数，实现对STM32芯片的多个串口操作和多种收发数据方式，实现串口通信的功能，本文的各个驱动代码经测试都可以直接使用，本人写的这部分代码开源 (。*^_^*。)

<!-- more -->

## 一、串口一的配置

* （初始化+中断配置+中断接收函数）

```C
/*===============================================================================
Copyright:
Version:
Author:    
Date: 2017/11/3
Description:
    配置独立看门狗初始化函数，在主函数中运行IWDG_ReloadCounter进行喂狗主函数必须在4s内进行一次喂狗不然系统会复位；
    函数功能是将接收固定长度的字符串，并将接收后的字符串通过串口发送出去
revise Description:
===============================================================================*/
#include "stm32f10x_usart.h"
#include "stm32f10x.h"
#include "stm32f10x_iwdg.h"

u8 USART1_RX_BUF[21]; 
u8 USART1_RX_CNT=0;

void IWDG_Configuration(void); 

void Usart1_Init(u32 bound)
{
    //GPIO端口设置
    GPIO_InitTypeDef GPIO_InitStructure;
    USART_InitTypeDef USART_InitStructure;
    NVIC_InitTypeDef NVIC_InitStructure;
     
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1|RCC_APB2Periph_GPIOA|RCC_APB2Periph_GPIOC, ENABLE);//使能USART1,GPIOA,C时钟
      
    //USART1_TX   GPIOA.9
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9; //PA.9
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;    //复用推挽输出
    GPIO_Init(GPIOA, &GPIO_InitStructure);//初始化GPIOA.9

    //USART1_RX      GPIOA.10初始化
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;//PA10
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;//浮空输入
    GPIO_Init(GPIOA, &GPIO_InitStructure);//初始化GPIOA.10  

    //Usart1 NVIC 配置
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);    //设置NVIC中断分组2:2位抢占优先级，2位响应优先级   0-3;
    
    NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=3 ;//抢占优先级3
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 3;        //子优先级3
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;            //IRQ通道使能
    NVIC_Init(&NVIC_InitStructure);    //根据指定的参数初始化VIC寄存器
  
   //USART 初始化设置

    USART_InitStructure.USART_BaudRate = bound;//串口波特率
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;//字长为8位数据格式
    USART_InitStructure.USART_StopBits = USART_StopBits_1;//一个停止位
    USART_InitStructure.USART_Parity = USART_Parity_No;//无奇偶校验位
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
    USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;    //收发模式

    USART_Init(USART1, &USART_InitStructure); //初始化串口1
    USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);//开启串口接受中断
    USART_Cmd(USART1, ENABLE);                    //使能串口1 
}
/**
* USART1发送len个字节.
* buf:发送区首地址
* len:发送的字节数(为了和本代码的接收匹配,这里建议不要超过64个字节)
**/
void USART1_Send_Data(u8 *buf,u16 len)
{
    u16 t;
    GPIO_SetBits(GPIOC,GPIO_Pin_9);
//  RS485_TX_EN=1;            //设置为发送模式
    for(t=0;t<len;t++)        //循环发送数据
    {           
        while(USART_GetFlagStatus(USART1,USART_FLAG_TC)==RESET); //循环发送,直到发送完毕   
        USART_SendData(USART1,buf[t]); 
    }     
    while(USART_GetFlagStatus(USART1, USART_FLAG_TC) == RESET);        
    GPIO_ResetBits(GPIOC,GPIO_Pin_9);
//    RS485_TX_EN=0;                //设置为接收模式    
}
void main(void)
{
    Usart1_Init(9600);//串口1波特率设置为9600
    IWDG_Configuration();
    while(1)
    {
        IWDG_ReloadCounter();//4s内必须喂狗不然复位
        if(USART1_RX_CNT==21)//数据接收完成
        {
            USART1_RX_CNT=0;//指针复位
            //将接收到的数据发送出去
            USART1_Send_Data(USART1_RX_BUF,21);//通过串口1将接收到的固定长度字符发送出去            
        }
    }
    
}
/**
* 接收指定长度的字符串
* 比如接收固定大小为21个字节的字符串
**/
void USART1_IRQHandler(void)                    //串口1中断服务程序
{
    u8 Res;
    if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET) 
        {
            Res =USART_ReceiveData(USART1);    //读取接收到的数据     
            if(USART1_RX_CNT<21)//对于接收指定长度的字符串
            {
                USART1_RX_BUF[USART1_RX_CNT]=Res;        //记录接收到的值    
                USART1_RX_CNT++;                                        //接收数据增加1 
            }             
     }
         //溢出-如果发生溢出需要先读SR,再读DR寄存器则可清除不断入中断的问题
    if(USART_GetFlagStatus(USART1,USART_FLAG_ORE) == SET)
    {
        USART_ReceiveData(USART1);
        USART_ClearFlag(USART1,USART_FLAG_ORE);
    }
     USART_ClearFlag(UART1,USART_IT_RXNE); //一定要清除接收中断
}
/*===============================================================================
Copyright:
Version:
Author:    
Date: 2017/11/3
Description:配置独立看门狗初始化函数，在主函数中运行IWDG_ReloadCounter进行喂狗
    主函数必须在4s内进行一次喂狗不然系统会复位
revise Description:
===============================================================================*/
void IWDG_Configuration(void) 
{
     /* 写入0x5555,用于允许狗狗寄存器写入功能 */
    IWDG_WriteAccessCmd(IWDG_WriteAccess_Enable); 
     /* 狗狗时钟分频,40K/256=156HZ(6.4ms)*/  
    IWDG_SetPrescaler(IWDG_Prescaler_256);    /* 喂狗时间 5s/6.4MS=781 .注意不能大于0xfff*/  
    IWDG_SetReload(781);//781（5s时间）
    IWDG_SetReload(3125);//781（20s时间）
    IWDG_Enable();//启用定时器
    IWDG_ReloadCounter();
}
```

## 二、串口二的配置

* （初始化+中断配置+中断接收函数）

```C
/*===============================================================================
Copyright:
Version:
Author:    
Date: 2017/11/3
Description:
    函数功能是将接收固定长度的字符串，并将接收后的字符串通过串口发送出去
revise Description:
===============================================================================*/
#include "stm32f10x_usart.h"
#include "stm32f10x.h"
#include "stm32f10x_iwdg.h"


u8 USART2_RX_BUF[250]; 
u8 USART2_RX_CNT=0;
u16 USART2_RX_STA=0;       //接收状态标记    

void Usart2_Init(u32 bound)
{  
    GPIO_InitTypeDef GPIO_InitStructure;
    USART_InitTypeDef USART_InitStructure;
    NVIC_InitTypeDef NVIC_InitStructure;
    //|RCC_APB2Periph_AFIO
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);//使能GPIOA时钟
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2,ENABLE);//使能USART2时钟

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;    //PA2
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;    //复用推挽
    GPIO_Init(GPIOA, &GPIO_InitStructure);

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3;//PA3
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING; //浮空输入
    GPIO_Init(GPIOA, &GPIO_InitStructure);  

    RCC_APB1PeriphResetCmd(RCC_APB1Periph_USART2,ENABLE);//复位串口2
    RCC_APB1PeriphResetCmd(RCC_APB1Periph_USART2,DISABLE);//停止复位

    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);    //设置NVIC中断分组2:2位抢占优先级，2位响应优先级   0-3;
    NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn; //使能串口2中断
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 3; //先占优先级2级
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 3; //从优先级2级
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; //使能外部中断通道
    NVIC_Init(&NVIC_InitStructure); //根据NVIC_InitStruct中指定的参数初始化外设NVIC寄存器

    USART_InitStructure.USART_BaudRate = bound;//波特率设置
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;//8位数据长度
    USART_InitStructure.USART_StopBits = USART_StopBits_1;//一个停止位
    USART_InitStructure.USART_Parity = USART_Parity_No;///奇偶校验位
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
    USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;//收发模式

    USART_Init(USART2, &USART_InitStructure); ; //初始化串口
    USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);//开启中断
    USART_Cmd(USART2, ENABLE);                    //使能串口 

}
/**
* USART2发送len个字节.
* buf:发送区首地址
* len:发送的字节数(为了和本代码的接收匹配,这里建议不要超过64个字节)
**/
void USART2_Send_Data(u8 *buf,u16 len)
{
    u16 t;
      for(t=0;t<len;t++)        //循环发送数据
    {           
        while(USART_GetFlagStatus(USART2, USART_FLAG_TC) == RESET);      
        USART_SendData(USART2,buf[t]);
    }     
    while(USART_GetFlagStatus(USART2, USART_FLAG_TC) == RESET);          
}
/**
* 这也是一个接收函数，可以用，也可以用下面main函数的方法调用
* USART2查询接收到的数据
* buf:接收缓存首地址
* len:读到的数据长度
**/
void USART2_Receive_Data(u8 *buf)
{
    u8 rxlen=USART2_RX_CNT;
    u8 i=0;
    delay_ms(10);        //等待10ms,连续超过10ms没有接收到一个数据,则认为接收结束
    while(rxlen!=USART2_RX_CNT)
    {
        rxlen=USART2_RX_CNT;
        delay_ms(10);
    }
        for(i=0;i<(USART2_RX_CNT);i++)
        {
            buf[i] = USART2_RX_BUF[i];    
            USART2_RX_BUF[i] = 0;
        }        
        USART2_RX_CNT=0;        //清零
    
}

void main(void)
{
    Usart2_Init(9600);//串口1波特率设置为9600
    while(1)
    {
        if(USART2_RX_STA)//数据接收完成
        {
            USART2_RX_STA=0;            
            //将接收到的数据发送出去
            USART2_Send_Data(USART2_RX_BUF,USART2_RX_CNT);//通过串口1将接收到的固定长度字符发送出去    
            USART2_RX_CNT=0;//指针复位
        }
    }    
}


void USART2_IRQHandler(void)
{
    u8 res;        
     if(USART_GetITStatus(USART2, USART_IT_RXNE) != RESET) //接收到数据
    {          
        res =USART_ReceiveData(USART2);     //读取接收到的数据        
        if(USART2_RX_STA==0)
        {
            USART2_RX_BUF[USART2_RX_CNT] = res;        //记录接收到的值    
            //当数据结尾收到0xA0和0xA1代表数据接收完成，是一串完整的数据
            if(USART2_RX_BUF[USART2_RX_CNT-1]==0xA0&&USART2_RX_BUF[USART2_RX_CNT]==0xA1)
                USART2_RX_STA=1;//表示接收数据结束
            USART2_RX_CNT++;                        //接收数据增加1 
        }
        } 
    }  
    //溢出-如果发生溢出需要先读SR,再读DR寄存器则可清除不断入中断的问题
    if(USART_GetFlagStatus(USART2,USART_FLAG_ORE) == SET)
    {
        USART_ReceiveData(USART2);
        USART_ClearFlag(USART2,USART_FLAG_ORE);
    }
     USART_ClearFlag(UART2,USART_IT_RXNE); //一定要清除接收中断    
}
```

##  三、串口三的配置

* （初始化+中断配置+中断接收函数）

```C
/*===============================================================================
Copyright:
Version:
Author:    
Date: 2017/11/3
Description:
    函数功能是将接收固定长度的字符串，并将接收后的字符串通过串口发送出去
    通过滴答定时器方式获取数据
revise Description:
===============================================================================*/
#include "stm32f10x_usart.h"
#include "stm32f10x.h"

#define USART3_TIMEOUT_Setting 800  //(ms)

u8 USART3_RX_BUF[250]; 
u16 USART3_RX_CNT=0;
u16 USART3_RX_TIMEOUT=0;       //接收状态标记    

void Timer1CountInitial(void);

void USART3_Init(u32 baud)   
{  
    USART_InitTypeDef USART_InitStructure;  
    NVIC_InitTypeDef NVIC_InitStructure;   
    GPIO_InitTypeDef GPIO_InitStructure;    //声明一个结构体变量，用来初始化GPIO  
    //使能串口的RCC时钟  
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB , ENABLE); //使能UART3所在GPIOB的时钟  
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART3, ENABLE);  

    //串口使用的GPIO口配置  
    // Configure USART3 Rx (PB.11) as input floating    
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_11;  
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;  
    GPIO_Init(GPIOB, &GPIO_InitStructure);  

    // Configure USART3 Tx (PB.10) as alternate function push-pull  
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;  
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;  
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;  
    GPIO_Init(GPIOB, &GPIO_InitStructure);  

    //配置串口  
    USART_InitStructure.USART_BaudRate = baud;  
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;  
    USART_InitStructure.USART_StopBits = USART_StopBits_1;  
    USART_InitStructure.USART_Parity = USART_Parity_No;  
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;  
    USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;  


    // Configure USART3   
    USART_Init(USART3, &USART_InitStructure);//配置串口3 
    // Enable USART3 Receive interrupts 使能串口接收中断  
    USART_ITConfig(USART3, USART_IT_RXNE, ENABLE);  
    // Enable the USART3   
    USART_Cmd(USART3, ENABLE);//使能串口3  

    //串口中断配置  
    //Configure the NVIC Preemption Priority Bits     
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);  

    // Enable the USART3 Interrupt   
    NVIC_InitStructure.NVIC_IRQChannel = USART3_IRQn;   
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=3 ;//抢占优先级3
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 2;        //子优先级3
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;  
    NVIC_Init(&NVIC_InitStructure);       
      
} 

void USART3_Sned_Char(u8 temp)        
{  
    USART_SendData(USART3,(u8)temp);      
    while(USART_GetFlagStatus(USART3,USART_FLAG_TXE)==RESET);  
      
}

void USART3_Sned_Char_Buff(u8 buf[],u32 len)  
{  
    u32 i;  
    for(i=0;i<len;i++)  
    USART3_Sned_Char(buf[i]);  
          
}

void main(void)
{
    Timer1CountInitial();
    Usart3_Init(9600);//串口1波特率设置为9600
    while(1)
    {
        if(USART3_RX_TIMEOUT==USART3_TIMEOUT_Setting)
        {            
            USART3_RX_TIMEOUT=0;
            USART3_Sned_Char_Buff(USART3_RX_BUF,USART3_RX_CNT);//将接收到的数据发送出去
            USART3_RX_CNT=0;
        }
        
    }    
}
void USART3_IRQHandler(void)                    //串口3中断服务程序
{
    u8 Res;
    if(USART_GetITStatus(USART3, USART_IT_RXNE) != RESET)  
    {    
        USART3_RX_TIMEOUT=0;
        USART3_RX_BUF[USART3_RX_CNT++] = USART_ReceiveData(USART3);    //读取接收到的数据        
    }
    //溢出-如果发生溢出需要先读SR,再读DR寄存器则可清除不断入中断的问题
    if(USART_GetFlagStatus(USART3,USART_FLAG_ORE) == SET)
    {
        USART_ReceiveData(USART3);
        USART_ClearFlag(USART3,USART_FLAG_ORE);
    }
    USART_ClearITPendingBit(USART3, USART_IT_RXNE);

}

//放到主函数的初始化中初始化
void Timer1CountInitial(void)
{
    //定时=36000/72000x2=0.001s=1ms;
        TIM_TimeBaseInitTypeDef    TIM_TimeBaseStructure;
        ///////////////////////////////////////////////////////////////
        RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM1, ENABLE);
        
        TIM_TimeBaseStructure.TIM_Period = 100-1;//自动重装值（此时改为10ms）
        TIM_TimeBaseStructure.TIM_Prescaler = 7200-1;//时钟预分频
        TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;//向上计数
        TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1;        //时钟分频1
        TIM_TimeBaseStructure.TIM_RepetitionCounter = 0;            
        TIM_TimeBaseInit(TIM1,&TIM_TimeBaseStructure);
        
        TIM_ClearFlag(TIM1,TIM_FLAG_Update);
        TIM_ITConfig(TIM1,TIM_IT_Update,ENABLE);  
        TIM_Cmd(TIM1, ENABLE);
}
void TIM1_UP_IRQHandler(void)
{        
    //TIM_TimeBaseStructure.TIM_Period = 100-1;//自动重装值（此时改为10ms）
    if (TIM_GetITStatus(TIM1, TIM_IT_Update) != RESET)
    {  
        if(USART3_RX_TIMEOUT<USART3_TIMEOUT_Setting)
                USART3_RX_TIMEOUT++;        
    }
    TIM_ClearITPendingBit(TIM1,TIM_IT_Update);
}
```

## 四、串口四的配置

* （初始化+中断配置+中断接收函数）

>  注意串口四的中断优先级没有贴出来，和前面的三个一样的配置，为了不占用过多的篇幅就不贴中断优先级配置了

```C
/*===============================================================================
Copyright:
Version:
Author:    
Date: 2017/11/3
Description:
    函数功能是将接收固定长度的字符串，并将接收后的字符串通过串口发送出去
    通过滴答定时器方式获取数据
revise Description:
===============================================================================*/
#include "stm32f10x_usart.h"
#include "stm32f10x.h"

#define USART4_TIMEOUT_Setting 800  //(ms)

u8 USART4_RX_BUF[250]; 
u16 USART4_RX_CNT=0;
u16 USART2_RX_STA=0;       //接收状态标记

void Systick_delay_init(u8 SYSCLK);
u8 virtual_delay(u32 num,u8 unit);

//通用异步收发器UART4
void UART4_Init(u32 bound)
{
    USART_InitTypeDef USART_InitStructure;
    GPIO_InitTypeDef GPIO_InitStructure;

    //used for USART3 full remap
    //GPIO_PinRemapConfig(GPIO_FullRemap_USART3, ENABLE);
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB | RCC_APB2Periph_GPIOC | RCC_APB2Periph_AFIO, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_UART4, ENABLE);//for UART4

    //Configure RS485_TX_EN PIN
    GPIO_InitStructure.GPIO_Pin = RS485_TX_EN_PIN;                 //PC9端口配置
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;          //推挽输出
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(RS485_TX_EN_PORT, &GPIO_InitStructure);

    RS485_TX_EN=0;            //设置485默认为接收模式

    /* Configure USART Tx as alternate function push-pull */
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_Init(GPIOC, &GPIO_InitStructure);

    /* Configure USART Rx as input floating */
    GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_11;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
    GPIO_Init(GPIOC, &GPIO_InitStructure);


    USART_InitStructure.USART_BaudRate = bound;
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;
    USART_InitStructure.USART_StopBits = USART_StopBits_1;
    USART_InitStructure.USART_Parity = USART_Parity_No ;
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
    USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;

    USART_Init(UART4, &USART_InitStructure);
    //USART_Init(USART3, &USART_InitStructure);
    /* Enable the USART */
    USART_Cmd(UART4, ENABLE);
    USART_ITConfig(UART4, USART_IT_RXNE, ENABLE);//开启串口接受中断
    USART_ClearFlag(UART4,USART_FLAG_TC);    
}
//USART1查询接收到的数据
//buf:接收缓存首地址
//len:读到的数据长度
void UART4_Receive_Data(u8 *buf)
{
    u8 rxlen=21;
    u8 i=0;
    delay_ms(10);        //等待10ms,连续超过10ms没有接收到一个数据,则认为接收结束
    
    RS485_RX_FLAG = 0;
    if((UART4_RX_BUF[0]==0x01)&&(UART4_RX_BUF[1]==0x03))
    {
        for(i=0;i<rxlen;i++)
        {
            buf[i]=UART4_RX_BUF[i];    
            UART4_RX_BUF[i] = 0;
        }    
        RS485_RX_FLAG = 1;
    }
        UART4_RX_CNT=0;        //清零
}


//USART1发送len个字节.
//buf:发送区首地址
//len:发送的字节数(为了和本代码的接收匹配,这里建议不要超过64个字节)
void UART4_Send_Data(u8 *buf,u16 len)
{
    u16 t;
    RS485_TX_EN=1;            //设置为发送模式
    for(t=0;t<len;t++)        //循环发送数据
    {           
        while(USART_GetFlagStatus(UART4,USART_FLAG_TC)==RESET); //循环发送,直到发送完毕   
        USART_SendData(UART4,buf[t]); 
    }     
    while(USART_GetFlagStatus(UART4, USART_FLAG_TC) == RESET);        
    RS485_TX_EN=0;                //设置为接收模式    
}

void main(void)
{
    Systick_delay_init(72);
    Usart4_Init(9600);//串口1波特率设置为9600
    while(1)
    {
        if(USART2_RX_STA)
        {
            if(virtual_delay(USART4_TIMEOUT_Setting,MS))//超过800ms空闲则可以读取数据
            {
                UART4_Send_Data(UART4_RX_BUF,UART4_RX_CNT);
                USART2_RX_STA=0;
                UART4_RX_CNT=0;                
            }
            
        }
        
    }    
}
void UART4_IRQHandler(void)                    //UART4 Receive Interrupt 
{
    u8 Res;
    
    if(USART_GetITStatus(UART4, USART_IT_RXNE) != RESET)  //接收中断(接收到的数据必须是0x0d 0x0a结尾)
    {    
        Res =USART_ReceiveData(UART4);//(USART1->DR);    //读取接收到的数据    
        UART4_RX_BUF[UART4_RX_CNT&0XFF]=Res;        //回传的数据存入数组,0X3F限制为64个数值
            UART4_RX_CNT++;
        USART2_RX_STA=1;    
    }
    
    if( USART_GetITStatus(UART4, USART_IT_TC) == SET )
    {
        USART_ClearFlag(UART4, USART_FLAG_TC);
    }    
    //溢出-如果发生溢出需要先读SR,再读DR寄存器则可清除不断入中断的问题
    if(USART_GetFlagStatus(UART4,USART_FLAG_ORE) == SET)
    {
        USART_ReceiveData(UART4);
        USART_ClearFlag(UART4,USART_FLAG_ORE);
    }
//    USART_ITConfig(UART4, USART_IT_RXNE, DISABLE);//临时关闭接收中断
    USART_ClearFlag(UART4,USART_IT_RXNE); //一定要清除接收中断
    
} 

//初始化延迟函数
//SYSTICK的时钟固定为HCLK时钟的1/8
//SYSCLK:系统时钟
void Systick_delay_init(u8 SYSCLK)
{
    SysTick->CTRL&=0xfffffffb;//bit2清空,选择外部时钟  HCLK/8
//    SysTick_CLKSourceConfig(SysTick_CLKSource_HCLK_Div8);    //选择外部时钟  HCLK/8
    fac_us=SYSCLK/8;            
    fac_ms=(u16)fac_us*1000;
}
/*===============================================================================
Author:peter pan
Date: 
Description: 查询式分时或叫做轮询式（近似延时）。本函数是用于执行高效率场合的查询延时，但是一个for or while 循环中只能用一次。
revise Description:  
@ num :    //分时查询的周期计数值    
@ unit :    //分时查询的周期单位 
    @@ParaValue ： 
        MS    //周期单位为MS毫秒级
        US    //周期单位为US微秒级
@ virtual_delay_status :    //静态变量
    @@ParaValue ： 
        SET    //SYSTICK正在占用中，请勿用
        RESET  //SYSTICK空闲，可以使用
@ReValue :
    with zero mean Time non-arrive ,one representative Time arrived ,you can do task;
##example             if(virtual_delay(1000,MS)) LedFlash();    //1000ms LED闪烁一下
===============================================================================*/
u8 virtual_delay(u32 num,u8 unit)
{
    u32 temp;           
    if(virtual_delay_status==RESET)    //  SYSTICK空闲，可以使用
      {
          if(unit==MS)
          {
                SysTick->LOAD=(u32)num*Delay_SYSCLK*125;//时间加载(SysTick->LOAD为24bit)
                SysTick->VAL =0x00;           //清空计数器
                SysTick->CTRL=0x01 ;          //开始倒数  
          }else if(unit==US) 
          {
                SysTick->LOAD=num*Delay_SYSCLK/8; //时间加载               
                SysTick->VAL=0x00;        //清空计数器
                SysTick->CTRL=0x01 ;      //开始倒数     
          }
          virtual_delay_status=SET;
          return 0;
        }
    else 
        {        //virtual_delay_status==SET SYSTICK被占用
        
            temp=SysTick->CTRL;
            if(!(temp&0x01&&!(temp&(1<<16))))//等待时间到达   
            {
                SysTick->CTRL=0x00;       //关闭计数器
                SysTick->VAL =0X00;       //清空计数器    
                virtual_delay_status=RESET;    
                return 1;
            }else return 0;
        }
}
```

附上[本人这篇博客地址](本文地址：https://www.cnblogs.com/pertor/p/9488446.html)
