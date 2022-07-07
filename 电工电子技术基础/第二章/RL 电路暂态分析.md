---
title: RL 电路暂态分析
date: 2022-03-25 20:05
---
# RL 电路暂态分析
## 零输入响应
* 对于**电感元件**，换路后无电源激励，有指数规律：
$$
i_L(t)=I_0e^{-\frac{t}{\tau}}
$$

$$
u_L(t)=-RI_0e^{-t\frac{R}{L}}
$$
其中$\tau=\dfrac{L}{R_0}$，同一电路中任意物理量的时间常数都是它
## 零状态响应
* 换路前无，后有电源激励：
$$
i_L(t)=\dfrac{U}{R}-\dfrac{U}{R}e^{-\frac{R}{L}t}
$$

$$
u_L(t)=Ue^{-\frac{R}{L}t}
$$
## 全响应
* 稳态分量 + 暂态分量
$$
i_L(t)=\dfrac{U}{R_2}+(\dfrac{U}{R_1+R_2}-\dfrac{U}{R_2})e^{-\frac{R_2}{L}t}
$$
![IMG_0096.png](http://image.tjzfile.xyz/images/2022/03/25/IMG_0096.png)
