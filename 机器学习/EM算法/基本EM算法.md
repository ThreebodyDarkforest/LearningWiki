# 基本 EM 算法

## 写在前面

EM 算法作为一种运行在概率模型上的算法，虽然算法过程比较简单，但是其数学本质却不那么容易理解。此外，这一算法由于在求解含有隐变量的概率模型的参数问题上表现良好，得到了广泛的应用。

总的来说，EM 算法是一个用于求解极大似然估计的迭代算法，可以描述为一个寻找概率模型的对数似然函数的最大下界的过程。它通过不断构造并求解一个特殊的 $Q$ 函数的极大值点，来近似地以 $Q$ 的极大值点作为对数似然函数的极大值点，进而找到最优参数。

看起来简单，不过这个算法似乎[水挺深](https://www.zhihu.com/question/40797593)的，慢慢学习吧。

## 隐变量与极大似然估计

EM 算法面对的问题与[极大似然估计](概率论与数理统计/第七章/极大似然估计)是相当类似的，让我们先来回顾一下极大似然估计。

对于随机变量 $Y$ 的一组观测值 $y = (y_1, y_2,\cdots, y_n)$，已知 $Y$ 满足某种**未知参数**的先验概率分布 $P(Y|\theta)$，我们希望通过 $y$ 求出该分布的参数 $\hat\theta$ 。

> 注：极大似然估计是经典概率论的重要方法，它假设观测值从一个确定参数但现在未知的概率分布中观测得到，并试图通过这些观测值反向求解这一**确定但未知**的参数  $\hat\theta$。

解决这一问题的手段是最大化（对数）似然函数

$$
L(\theta) = \sum_{j = 1}^n \log P(y_j|\theta)
$$
要求

$$
\arg\max_\theta L(\theta)
$$

一般来说接下来对各个参数求偏导就完事了，但是当概率分布中存在**隐变量**时，这个问题没有解析解。

> 注：
> （1）所谓隐变量，就是虽然由概率分布 $P(Y|\theta)$ 生成但是**不可观测**的随机变量。严格地说，若隐变量为 $Z$，概率分布应写为 $\sum_{Z}P(Y,Z|\theta)$，其中 $Y$ 的值可观测，但 $Z$ 不可观测。
> （2）当然，只有当 $Z$ 会对可观测变量 $Y$ 产生影响时我们才会去考虑它，$Z$ 才会成为隐变量。
> （3）‼️注意，观测数据 $y$ 称为**不完全数据**，而 $y, z$ 的并才称为**完全数据**，严格的概率分布函数应该建立在完全数据上（大写为随机变量，小写为样本值）。

EM 算法就能通过迭代解决含有隐变量的参数估计问题。

## 问题求解

EM 算法与其它迭代算法的基本思想一致，就是通过迭代不断接近最优解。这就需要保证算法具有三个性质

- 算法每轮迭代给出的都是可行解
- 算法每轮迭代给出的解都比上一轮更优
- 算法能够在运行足够时间后收敛

第一点是显然的，因为该问题并没有什么约束条件，$\theta$ 只要在其定义域上即可。

而第二点的论证则并不显然，我们先描述含有隐变量的对数似然函数

$$
\begin{aligned}
L(\theta) 
&= \sum_{j = 1}^n\log \sum_ZP(y_j,Z|\theta)\\
&= \sum_{j = 1}^n\log\left(\sum_Z P(y_j|Z,\theta)P(Z|\theta)\right)
\end{aligned}
$$

> 注：
> （1）注意这个地方两个求和号不同的意义。最外层的求和号原本是累乘，表示所有 $y_j$ 同时发生的概率（乘法原理），内层求和号则是根据加法原理得出的（不同的隐变量取值对应到同一个 $y_j$）。
> （2）第三点就不写了，可以参考[这篇文章](https://blog.csdn.net/weixin_44936889/article/details/104038703)，机器学习方法这本书上也有，大概就是通过 $Jenson$ 不等式放缩来证明。

为了满足第二点，我们要求

$$
L(\theta^{(i + 1)}) - L(\theta^{(i)}) > 0
$$
现假设已知 $L(\theta^{(i)})$，则本轮迭代所求 $\theta$ 必须满足 $L(\theta) > L(\theta^{(i)})$

$$
L(\theta) - L(\theta^{(i)}) = \sum_{j = 1}^n\left\{\log\left(\sum_Z P(y_j|Z,\theta)P(Z|\theta)\right) - \log P(y_j|\theta^{(i)})\right\} > 0
$$

利用 $Jensen$ 不等式可得

$$
\begin{aligned}
L(\theta) - L(\theta^{(i)})
&= \sum_{j = 1}^n\left\{\log\left(\sum_Z P(Z|y_j,\theta^{(i)})\dfrac{P(y_j|Z,\theta)P(Z|\theta)}{P(Z|y_j,\theta^{(i)})}\right) - \log P(y_j|\theta^{(i)})\right\}\\
&\ge \sum_{j = 1}^n\left\{\sum_Z P(Z|y_j,\theta^{(i)})\log\left(\dfrac{P(y_j|Z,\theta)P(Z|\theta)}{P(Z|y_j,\theta^{(i)})}\right) - \log P(y_j|\theta^{(i)})\right\}\\
& = \sum_{j = 1}^n\left\{\sum_Z P(Z|y_j,\theta^{(i)})\log\left(\dfrac{P(y_j|Z,\theta)P(Z|\theta)}{P(Z|y_j,\theta^{(i)})P(y_j|\theta^{(i)})}\right)\right\}
\end{aligned}
$$

> 注：$\sum_{Z}P(Z|y_j,\theta^{(i)}) = 1$

运用这个不等式，我们规避了包含和的对数难以求解的问题，并获得了 $L(\theta)$ 的一个下界 $B(\theta, \theta^{(i)})$

$$
L(\theta) \ge B(\theta,\theta^{(i)}) = L(\theta^{(i)}) + \sum_{j = 1}^n\left\{\sum_Z P(Z|y_j,\theta^{(i)})\log\left(\dfrac{P(y_j|Z,\theta)P(Z|\theta)}{P(Z|y_j,\theta^{(i)})P(y_j|\theta^{(i)})}\right)\right\}
$$

通过最大化这个下界，同样可以达到最大化 $L(\theta)$ 的效果，于是我们进一步研究该下界。

首先有

$$
B(\theta^{(i)},\theta^{(i)}) = L(\theta^{(i)})
$$
这意味着 $B$ 与 $L$ 恰好在 $\theta^{(i)}$ 处相切，而在其他地方有 $B(\theta, \theta^{(i)}) < L(\theta^{(i)})$。

> 注：大概是这么个意思，网上找的图，里面 $l$ 与上文的 $B$ 相同含义。
> ![OIP-C.EhIgkAp3ZYmP6tA1vdZGkgHaEG.jpg](http://image.tjzfile.xyz/images/2023/02/04/OIP-C.EhIgkAp3ZYmP6tA1vdZGkgHaEG.jpg)

接下来考虑最大化 $B(\theta,\theta^{(i)})$

$$
\arg\max_\theta B(\theta,\theta^{(i)})
$$
将其中的与 $\theta$ 无关的量去掉之后得到

$$
\arg\max_{\theta} \sum_{j = 1}^n\left(\sum_Z P(Z|y_j,\theta)\log P(y_j, Z|\theta)\right)
$$

接下来令

$$
\begin{aligned}
Q(\theta, \theta^{(i)}) 
&= \sum_{j = 1}^n\left(\sum_Z P(Z|y_j,\theta)\log P(y_j, Z|\theta)\right)\\
&= E_Z[\log P(Y,Z|\theta)|Y,\theta^{(i)}]
\end{aligned}
$$
则最大化 $B(\theta,\theta^{(i)})$ 的问题等价于

$$
\theta^{(i + 1)} = \arg\max_\theta Q(\theta, \theta^{(i)})
$$

也就是说要迭代求解任意含隐变量的极大似然估计问题，只需要在每轮迭代中，求解问题的 $Q$ 函数并最大化该函数即可。该算法之所以叫 EM 算法，是因为在每轮迭代中有两步

- E 步：求出 $Q$ 函数，即对数似然函数的期望（expectation）

$$
Q(\theta, \theta^{(i)}) = E_Z[\log P(Y,Z|\theta)|Y,\theta^{(i)}]
$$

- M 步：求出 $Q$ 函数的极值，即最大化 $Q$ 函数（maximization）

$$
\theta^{(i + 1)} = \arg\max_\theta Q(\theta, \theta^{(i)})
$$

每轮迭代都会使得下界 $B$ 得到增长，EM 算法就是通过不断使得下界极大化进而逼近求解对数似然函数的。

因此，只要我们能够合理地定义概率模型 $P(Y,Z|\theta)$ 并已知一系列观测值 $y_1,y_2,\cdots,y_n$，我们就能使用 EM 算法求解该模型的近似最优参数。

> 注：
> （1）EM 算法是初值敏感的。
> （2）停机条件是更新的幅度小于给定阈值。