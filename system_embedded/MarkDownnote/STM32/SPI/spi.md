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

#SPI  
#####Motorola发明
高速，全双工，四根线
SPI线路由一个主机，多个从机组成。
###线1：SCLK
提供SCLK的为master
###线2：NSS 
NSS即片选CS信号号线，通过NSS(CS)来选择主机与那个从机通讯
所有操作都要先拉低CS电平，激活slave
操作完成后再拉高CS电平，释放slave
HAL_GPIO_writepin来写入连接芯片CS引脚的电平(即NSS片选)
+ 传输数据线要将slave的选中，给一个NSS信号，也就是将CS线拉低
+ 硬件控制：
  + 可以在MX中设为硬件控制，MX指定一个GPIO，在发送数据时会自动拉低拉高，不用自己操控，只用接上线。
+ 软件模拟：使能一个IO，用到哪个slave，就把那个slave的CS线拉低，结束后把slave的CS拉高
  + 主设备控制：主设备GPIO控制slave_cs的拉高拉低
  + 第三方控制：用其他设备控制slave_cs,保证传输数据前拉低，传完拉高即可。
+ NSS接线方式
  + 几个slave就接几根线，分开单独控制
  + 可以一根NSS线同时控制多个，拉低总线就相当于拉低若干个子设备
  + 也可以把slave的NSS线串在一起，不过这样只要有一个断点，断点后的slave都不会被操控(选中)，没法被选中接收数据。
  

###线3，4：SDO-MOSI/SDI-MISO 
两条线的数据是同步收发的，若想接收，发送空指令，若想发送，也会接收一些data

####过程：
1. 控制(NSS)CS对应的IO引脚电平高/低，选择开启/关闭从设备
   NSS选中后(等效于寻址从设备的操作)，
   + 与FLASH通讯，发送command(读取指令，擦除指令，页写指令等等，具体看通信对象)，调用transmitreceive指令 收(读) 发(写) 数据
   + 与其他设备通讯，一般直接调佣transmitreceive即可完成收发数据
####性能：
+ 常见频率：
72/4=18Mhz=55ns   一个周期= 55  = 一个下降沿或上升沿(一个周期指低电平脉冲宽度+高电平脉冲宽度) = 55ns传输一个bit
（1/72Mhz=13.8=14ns   1/18=55.5=55ns）
+ 传输方式：
  一般在72Mhz，GPIO_speed_low时，wirtepin_set为70ns，writepin_reset为50ns，所以对于高速SPI，不采用软件模拟，而使用硬件SPI
对于一些较低速的DR单总线，IIC等，可以考虑软件模拟的方式便于移植

####函数区别：
```c
+ HAL_SPI_receivetransmit=HAL_SPI_receive=HAL_SPI_transmit，

HAL_SPI_TransmitReceive	(&hspi1,	&send,	&read,	1,	0xFFFFFF);
HAL_SPI_Transmit	(&hspi1,	&send,		1,	0xFFFFFF);
HAL_SPI_Receive		(&hspi1,		&read,	1,	0xFFFFFF);
```
只不过第一个要传两个地址指针参数进去，后两个只用传一个地址指针参数进去
三者在全双工模式下 本质上一样，因为数据同步双向，传输一个Data时，transmit和receive在同时进行。

####特别注意parameter：
+ 参数SIZE，表示个数
+ 依据你定义的SPI传输通道宽度(指向缓冲区的数据指针宽度)_16bit_或者_8bit_，发送对应的数据大小
  + uint8_t *send   =1byte*size
  + uint16_t *send  =2byte*size
+ 例如定义了一个uint16_t Rxbuf[  ]； uint16_t *read;
+ 使用此函数收数据时，
  1. 用于指向接收区域Rxbuf的指针read会指向这个数组的首地址，
  2. 根据size的大小，来自增放入
     + 例如size=2，则receive两个_16bit_(根据你定义的SPI宽度)的数据放入a[0]和a[1]；因此，在official_function_manual中，SIZE的描述为amount，指传了几帧，而不是帧的大小，帧的大小，也就是SPI宽度是8还是16在初始化中设置

***
##dating...
####硬件SPI与FLASH通信
Personal function depository Q_
Personal variables and function declarations
```c
    void Delay( uint32_t nCount);                   
    
    uint8_t Send[] = {9,2,3,4,5,6};                                                              //发送区
    uint8_t*pSend=Send;
    
    uint8_t Read[32] = "0";                                                                      //接收区
    uint8_t*pRead=Read;

    uint8_t PP=0x02,RD=0x03,RDID=0x90,SE=0x20,WREN=0x06,RDSR1=0x05,ZERO=0x00,DummyByte=0xFF;     //指令
    uint32_t timeout=72000;                                                                      //等待超时1ms

    uint8_t Q_SPI_1_TR(uint8_t Data);                                     //
    void Q_NSS_PA2_level(uint8_t state);                                  //
    void Q_SPI_FLASH_busy_reset(void);                                    //
    void Q_SPI_FLASH_WREN(void);                                          //
    void Q_SPI_FLASH_busy_reset(void);                                    //
    void Q_SPI_FLASH_ReadID(void);                                        //
    void SPI_FLASH_SE(uint32_t SectorAddr);                               //
    void Q_SPI_FLASH_RD(uint32_t ReadAddr,uint16_t Length_of_data);       //
    void Q_SPI_FLASH_WR(uint32_t WriteAddr);                              //

main------
//传几次就死机
  while (1)
  {
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_8, GPIO_PIN_SET);      
    Delay(7200000);

    Q_SPI_FLASH_ReadID();                             		 //查看ID
      
    Q_SPI_FLASH_busy_reset();                         		 //等待Busy位reset
    SPI_FLASH_SE(0x001000);                         		 //写使能，发送擦除指令的地址  
      
    Q_SPI_FLASH_busy_reset();
    Q_SPI_FLASH_WR(0x001000);                      	   	 //写使能，发送页写指令的地址  
 
    Q_SPI_FLASH_busy_reset();
    uint8_t readlength=12;                          	 	 //设定要查看的数据大小
    Q_SPI_FLASH_RD(0x001000,readlength);            	 	 //发送读指令，地址
   for(int i=0;i<readlength;i++)printf("0x%02x  ",Read[i]);

    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_8, GPIO_PIN_RESET);
    Delay(7200000);

}

//    while(--readlength)
//    {   
//        uint8_t *pdata=Read;
//        printf("0x%x  ",*pdata++);
//    }


define-------------------
 void Delay(uint32_t nCount)                  	  //软件延时延时函数
{
  for(; nCount != 0; nCount--);
}


uint8_t Q_SPI_1_TR(uint8_t Data)              	 //发送数据函数，返回值为接收的数据
{					                           //parameter：需要发送到flash的数据
    uint8_t Read=0; 
    HAL_SPI_TransmitReceive( &hspi1, &Data, &Read, 1, 0xFFFF);
    return Read;
}


void Q_NSS_PA2_level(uint8_t state)                     //CS电平
{   					            //parameter：0、1
    if(state==0)
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_2, GPIO_PIN_RESET);       
    else
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_2, GPIO_PIN_SET);
}


void Q_SPI_FLASH_busy_reset(void)                      //等待busy位清除
{
  uint8_t FLASH_Status = 0;
  Q_NSS_PA2_level(0);
  Q_SPI_1_TR(RDSR1);
  do
  {
  FLASH_Status=Q_SPI_1_TR(DummyByte);        
    {
      if((timeout--) == 0) 
      {
        printf("无法传输");
        return;
      }
    } 
  }while ((FLASH_Status & 0x01) == SET); 	//SR1 寄存器最后一位为busy位
  Q_NSS_PA2_level(1);
}


void SPI_FLASH_SE(uint32_t SectorAddr)              // sector(1*16*256=4096B=4KB) erase   (contain write enable)
{
  Q_SPI_FLASH_WREN();
  Q_SPI_FLASH_busy_reset();
  Q_NSS_PA2_level(0);
  Q_SPI_1_TR(SE);
  Q_SPI_1_TR((SectorAddr & 0xFF0000) >> 16);
  Q_SPI_1_TR((SectorAddr & 0xFF00) >> 8);
  Q_SPI_1_TR( SectorAddr & 0xFF);
  Q_NSS_PA2_level(1);
  Q_SPI_FLASH_busy_reset();
}


void Q_SPI_FLASH_WREN(void)                          //write enable
{
  Q_NSS_PA2_level(0);
  Q_SPI_1_TR(WREN);
  Q_NSS_PA2_level(1);
}


void Q_SPI_FLASH_ReadID(void)                       //read ID on flash
    {
    Q_NSS_PA2_level(0);
    Q_SPI_1_TR(RDID);
    Q_SPI_1_TR(ZERO);
    Q_SPI_1_TR(ZERO);
    Q_SPI_1_TR(ZERO);
    printf("\n芯片ID:0x%x",Q_SPI_1_TR(ZERO));
    printf("%x\n",Q_SPI_1_TR(ZERO));
    Q_NSS_PA2_level(1);
    }
    

void Q_SPI_FLASH_WR(uint32_t WriteAddr)                   //write data on flash   (contain  write enable)
{					         //parameter：需要写入的flash的起始地址，需要读取的数据长度
    Q_SPI_FLASH_WREN();
    Q_NSS_PA2_level(0);
    Q_SPI_1_TR(PP);
    Q_SPI_1_TR((WriteAddr & 0xFF0000) >> 16);
    Q_SPI_1_TR((WriteAddr & 0xFF00) >> 8);
    Q_SPI_1_TR( WriteAddr & 0xFF);

    printf("发送的数据为：");
    for(int i=0;i<sizeof(Send);i++)
    {
        Q_SPI_1_TR(Send[i]);
        printf("%d  ",Send[i]);
    }
    printf("\n");
    Q_NSS_PA2_level(1);
}

void Q_SPI_FLASH_RD(uint32_t ReadAddr,uint16_t Length_of_data)        //read data on flash   
{							     //parameter：需要读取的flash的起始地址，需要读取的数据长度
  Q_NSS_PA2_level(0);
  Q_SPI_1_TR(RD);
  Q_SPI_1_TR((ReadAddr & 0xFF0000) >> 16);
  Q_SPI_1_TR((ReadAddr & 0xFF00) >> 8);
  Q_SPI_1_TR( ReadAddr & 0xFF);
  printf("收到的数据为：");
  while (Length_of_data--)
  {
    *pRead = Q_SPI_1_TR(DummyByte);
    pRead++;
  }
    Q_NSS_PA2_level(1);
}
```
####NM25Q64手册
根据NM25Q64手册，
发送指令09H，后接000000H得Manufacturer地址52H，后接000001H得Device地址16H
实际后接000000H为Manufacturer地址52H，其他值(即不为000000H的值)为Device地址16H


数据寄存器DR    接收数据寄存器RDR     发送数据寄存器TDR    xx外设控制器CR1
+ TXE  空flag(已发送)   
  + 发送缓冲区(即TDR)中的数据为空  TXE=SET   表明数据从TDR中已发送到**位移**寄存器中
+ RXNE 非空flag(已收到)   
  + 接收缓冲区(即RDR)中的数据不为空  RXNE=SET   表明RDR从**位移**寄存器中接收到数据
+ TC 发送完成flag 
  + 即TDR和**移位**寄存器中数据都空 TC=SET




***
##dating...

NOR FLASH基本驱动步骤

SPI配置
SPI工作参数配置初始化：工作模式、时钟极性、时钟相位，HAL_SPI_Init();
使能SPI时钟、初始化相关引脚：GPIO设为复用推挽输出，HAL_SPI_MspInit();
使能SPI：__HAL_SPI_ENABLE();
SPI传输数据：HAL_SPI_Transmit 发送；HAL_SPI_Receive 接收；HAL_SPI_TransmitReceive 进行发送接收；
设置SPI传输速度（可选）：操作SPI_CR1寄存器中的波特率（需要先失能SPI，设置完成后再使能）

NM25Q128驱动
初始化片选引脚和SPI接口：相关GPIO、SPI；
NM25Q128读取：0x03+24位地址+读取数据；
NM25Q128扇区擦除：0x06+等待空闲+0x20+24位地址+等待空闲；擦除大小4096字节；
NM25Q128写入：擦除扇区（可选）+0x06+0x02+24位地址+写入数据+等待空闲。
驱动核心在于写数据：需要判断是否需要擦除；写入数据是否需要换页换扇区；遵循读、改、写原则。
写数据是将磁盘中的1-->0，无法将0-->1，因此要进行擦除，使所有的位都变成1
一般对于一块新磁盘，没有写入数据前，大部分扇区读取到的数据为1，若读取数据长度为1Byte，则显示数据255/0xFF

读操作步骤 ：读命令 ，地址 ，读数据(发数据)
擦除步骤 ：写使能 ，擦除命令 ，地址 
写操作步骤： 写使能，擦除命令 ，写使能 ，写命令 ，地址， 发数据(读数据)
数据大小不同擦除和写指令不同
