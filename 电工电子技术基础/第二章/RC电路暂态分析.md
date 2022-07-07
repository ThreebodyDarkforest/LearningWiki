---
title: RC电路暂态分析
date: 2022-03-18 19:32
---
# RC 电路暂态分析
[TOC]
## 写在前面
* **电容上**电压随时间按**指数规律**变化
* 变化的**起点是初始值**，变化的**终点是稳态值**
* 变化**速度取决于时间常数**
· 实际上，当 $t=5\tau$ 时，过渡过程基本结束
## 零输入响应
* 换路后的电路中无电源激励
$$
RC\dfrac{du_C}{dt}+u_C=0
$$
解得
$$
u_C (t)=Ue^{-\frac{t}{RC}}
$$
时间常数 $\tau=RC$，**越大过渡时间越慢**
其中单位 $R(\Omega),C(F),\tau(s)$
其他量
$$
u_R=-u_c=-Ue^{-\frac{t}{RC}}
$$

$$
i_C=\dfrac{u_C}{R}=\dfrac{U}{R}e^{-\frac{t}{RC}}
$$
### 波形图
![IMG_0079.png](http://image.tjzfile.xyz/images/2022/03/24/IMG_0079.png)
![IMG_0080.png](http://image.tjzfile.xyz/images/2022/03/24/IMG_0080.png)
## 零状态响应
* 换路前电容上电压为零
$$
RC\dfrac{du_C}{dt}+u_C=U
$$
解得
$$
u_C(t)=U-Ue^{-\frac{t}{RC}}
$$
其中 $U$ 称为**稳态分量（不随时间变）**，$Ue^{-\frac{t}{RC}}$ 称为**暂态分量**
同样的有 $\tau=RC$
其他量
$$
u_R=U-u_C=Ue^{-\frac{t}{RC}}
$$

$$
i=\dfrac{u_R}{R}=\dfrac{U}{R}e^{-\frac{t}{RC}}
$$
### 波形图
![IMG_0082.png](http://image.tjzfile.xyz/images/2022/03/24/IMG_0082.png)
## 全响应
* 换路前电压不为零，换路后有电源激励
$$
RC\dfrac{du_C}{dt}+u_C=U
$$
解得
$$
u_C(t)=U+(U_0-U)e^{-\frac{t}{RC}}
$$
即**零输入和零状态的并**，符号意义跟上文一致
同样的 $\tau=RC$
### 波形图
![IMG_0083.png](http://image.tjzfile.xyz/images/2022/03/24/IMG_0083.png)