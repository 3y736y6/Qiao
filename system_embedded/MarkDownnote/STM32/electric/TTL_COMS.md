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
###TTL 电平信号
+ TTL一般采用5V电源
输出 Uoh(高电平) >= 2.4V      输出Uol(低电平)   <=  0.4V
输入 Uih(高电平)  >=  2.0V      输入Uil(低电平)   <=  0.8V

###CMOS 电平信号 
电压控制器件 输入电阻极大，对于干扰信号十分敏感，因此不用的输入端不应开路，接到地或者电源上。CMOS电路的优点是噪声容限较宽，静态功耗很小。

  Uoh  ≈   VCC                Uol    ≈      GND
  Uih   ≥   0.7 VCC           Uil     ≤     0.2 VCC  

在同样5V电源电压情况下，COMS电路可以直接驱动TTL
+ 因为COMS产生的高电平电压值和低电平电压值都在TTL接收范围内
CMOS --Uoh ( 5V )    >     TTL --Uih ( 2.0V )
COMS --Uol ( 0V )     <   TTL --Uil  ( 0.8V )

+ 但TTL --( Uoh >= 2.4V ）  ，不一定大于COMS --Uih（0.7VCC=0.7*5V=3.5V）
在同样的5V电源电压情况下，TTL输出的高电平电压值不一定能被COMS接收检测并转化为逻辑1


