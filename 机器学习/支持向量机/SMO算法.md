# 序列最小最优化算法

## SVM 的算法实现问题

现在，我们已经对 SVM 进行了深入的数学分析，解决了从问题定义到求解方法的一系列问题。但是就其算法实现而言，使用数学方法求解（凸优化方法解线性方程组）在大规模数据上非常慢，于是我们转而试图得到一种迭代方法来近似地得到最优解而非直接求出精确解，这就是序列最小最优化（SMO）方法的基本思想。

## SMO算法

SMO 算法面对一个凸二次规划问题

$$
\begin{aligned}
&\min_{\pmb \alpha}\dfrac{1}{2}\sum_{i = 1}^n\sum_{j = 1}^n\alpha_i\alpha_jy_iy_jK(\pmb x_i, \pmb x_j) - \sum_{i = 1}^n\alpha_i\\
st.&\sum_{i = 1}^n\alpha_iy_i = 0\\
&0\le \alpha_i \le C
\end{aligned}
$$

其中共有 $n$ 个样本点 $(\pmb x_i, y_i)$，对应地有 $n$ 个拉格朗日乘子 $\alpha_i$。

### 问题转化与求解

SMO 算法基于一条基本定理：

> 问题的最优解的充分必要条件是其满足KKT条件，故当所有样本点都满足 KKT 条件时，当前解为最优解。

也就是说，只要我们通过某种手段不断调整分类超平面，使得当前解逐渐完全满足 KKT 条件即可。SMO 算法就是这样一种迭代算法，它在每轮迭代中选取两个特定的 $\alpha_1, \alpha_2$ 作为变量，并**固定其它** $\pmb\alpha$，选取标准如下

* $\alpha_1$ 为所有样本点中违反 KKT 条件的那个点对应的拉格朗日乘子。
* $\alpha_2$ 为在 $\alpha_1$ 已确定的情况下自身能够发生最大变化的拉格朗日乘子。

然后，用这两个变量构造一个子问题

$$
\begin{aligned}
    \min_{\alpha_1, \alpha_2} W(\alpha_1,\alpha_2) = &\dfrac{1}{2}K_{11}\alpha_1^2 + \dfrac{1}{2}K_{22}\alpha_2^2 + y_1y_2K_{12}\alpha_1\alpha_2 -\\ 
    &(\alpha_1 + \alpha_2) + y_1\alpha_1\sum_{i = 3}^ny_i\alpha_iK_{i1} + y_2\alpha_2\sum_{i = 3}^ny_i\alpha_iK_{i2}\\
    st.&~\alpha_1y_1 + \alpha_2y_2 = -\sum_{i = 3}^n \alpha_iy_2 = \varsigma\\
    &0\le \alpha_i \le C,~ i = 1,2
\end{aligned}
$$

其中 $K_{ij} = K(\pmb x_i, \pmb x_j)$ ，$\varsigma$ 是常数。那么显然由于

$$
\alpha_1 = y_1(\varsigma - \alpha_2y_2)
$$

该问题实质上是单变量最优化问题，即可直接使用解析法求解。此外，由于该问题只含两个变量，故可在二维平面上进行讨论。

* 由 $0\le \alpha_i \le C, i = 1, 2$ 可知该问题的可行域在一个 $[0, C]\times [0, C]$ 的方框内。
* 由 $\alpha_1y_2 + \alpha_2y_2 = \varsigma$ 可知该问题的可行域进一步缩小到 $[0, C]\times [0, C]$ 中的一条直线段。

进一步地，我们希望求出 $W(\alpha_1, \alpha_2)$ 在此二约束下的最优解，那么不妨先求出无约束情况下的最优解，再通过考察 $W(\alpha_1, \alpha_2)$ 的和约束本身性质来确定最优解。

显然，**无约束最优解**是易求的，首先作变量代换，求 $\alpha_2^{new,unc}$

$$
\begin{aligned}
W(\alpha_2) = &\dfrac{1}{2}K_{11}(\varsigma - \alpha_2y_2)^2 + \dfrac{1}{2}K_{22}\alpha_2^2 + y_2K_{12}(\varsigma - \alpha_2y_2)\alpha_2 - \\
&(\varsigma - \alpha_2y_2)y_1 - \alpha_2 + (\varsigma - \alpha_2y_2)\sum_{i = 3}^ny_i\alpha_iK_{i1} + y_2\alpha_2\sum_{i = 3}^ny_i\alpha_iK_{i2}
\end{aligned}
$$

令 $\dfrac{dW}{d\alpha_2}$ = 0，并由初始可行解 $\alpha_1^{old}, \alpha_2^{old}$ 计算常数 $\varsigma = \alpha_1^{old}y_1 + \alpha_2^{old}y_2$，可得

$$
\alpha_2^{new, unc} = \alpha_2^{old} + \dfrac{y_2(E_1 - E_2)}{\eta}
$$

其中

$$
g(\pmb x) = \sum_{i = 1}^n\alpha_iy_iK(\pmb x_i, \pmb x) + b
$$

$$
E_i = g(x_i) - y_i
$$

$$
\eta = K_{11} + K_{22} - 2K_{12}
$$

那么

$$
\alpha_1^{new,unc} =  \alpha_1^{old} +  y_1y_2(\alpha_1^{old} - \alpha_1^{new,unc})
$$

> 注：
> （1）$\alpha_2^{new,unc}$ 是无约束最优化问题的最优解。
> （2）$E_i$ 表示第 $i$ 个样本点的分类结果的误差。
> （3）由于每次迭代中使用此法解析求解对于任意可行解 $\alpha_1^{old}, \alpha_2^{old}$，都能得到局部最优解（同时显然是可行解）$\alpha_1^{new},\alpha_2^{new}$，因此只要保证 $\pmb \alpha$ 的初始值为可行解，那么之后的每轮迭代得到的都是可行解。
> （4）注意由于当前迭代时 $\pmb \alpha^{old}$ 为常数，那么 $g(\pmb x_i), E_i, i = 1,2,\cdots,n$ 以及 $K_{ij}$ 都是常数，

接下来再来考虑约束的问题，设约束条件下最优解为 $\alpha_1^{new}, \alpha_2^{new}$，约束造成的影响如下

$$
L\le \alpha_i^{new} \le H, i = 1, 2
$$

我们只考虑 $\alpha_2^{new}$ 的情况，只要它满足约束，那么 $\alpha_1^{new}$ 显然满足。

* 若 $y_1 \neq y_2$，则可行域直线单调递增，因此有（令 $\alpha_1 = 0, C$ 可求）

$$
L = \max(0, \alpha_1^{old} - \alpha_2^{old}), H = \min(C, C + \alpha_1^{old} - \alpha_2^{old})
$$

* 若 $y_1 = y_2$，则可行域单调递减，因此有

$$
L = \max(0, \alpha_1^{old} + \alpha_2^{old} - C), H = \min(C, \alpha_1^{old} + \alpha_2^{old})
$$

不难发现 $W(\alpha_2)$ 在 $0\le \alpha_2\le C$ 单调，这就保证了上式的正确性。

求出 $\alpha_2^{new}$ 后，再用跟上面同样的方法即可求出 $\alpha_1^{new}$

$$
\alpha_1^{new} =  \alpha_1^{old} +  y_1y_2(\alpha_1^{old} - \alpha_1^{new})
$$

要更新分类超平面，除了 $\pmb\alpha$ 还需要更新阈值 $b$，同时重新计算所有 $E_i$（其中含有 $b$）

$$
b_1^{new} = -E_1 - y_1K_{11}(\alpha_1^{new} - \alpha_1^{old}) - y_2K_{21}(\alpha_2^{new} - \alpha_2^{old}) + b^{old}
$$

$$
b_2^{new} = -E_2 - y_1K_{12}(\alpha_1^{new} - \alpha_1^{old}) - y_2K_{22}(\alpha_2^{new} - \alpha_2^{old}) + b^{old}
$$

* 若 $0 < \alpha_i < C, i = 1,2$，那么 $b^{new} = b_1^{new} = b_2^{new}$。
* 若 $\alpha_1^{new}, \alpha_2^{new}$ 是 $0$ 或 $C$，那么 $\min(b_1^{new}, b_2^{new})\le b^{new} \le \max(b_1^{new}, b_2^{new})$。

$$
E_i^{new} = \sum_{j\in S}y_j\alpha_jK(\pmb x_i, \pmb x_j) + b^{new} - y_i
$$

其中 $S$ 是当前所有支持向量对应的下标集合。

### 变量选取

在上面的论述中，我们提到了两个可行解 $\alpha_1^{old}, \alpha_2^{old}$，它们是从 $n$ 个拉格朗日乘子中按一定标准选择的，目的是使得目标函数变小得尽可能大。

具体地说，$\alpha_1^{old}$ 从所有样本点中选取（当前迭代）违反 KKT 条件最严重的一个，即进行检验

$$
\alpha_i = 0 \Leftrightarrow  y_ig(\pmb x_i)\ge 1\\
0\le \alpha_i \le C \Leftrightarrow y_ig(\pmb x_i) = 1\\
\alpha_i = C \Leftrightarrow y_ig(\pmb x_i) \le 1
$$

并选取违反上述条件最严重的一个样本点对应的拉格朗日乘子作为 $\alpha_1^{old}$。

当确定 $\alpha_1^{old}$ 之后，$\alpha_2^{old}$ 便可通过约束条件确定，即使得 $|\alpha_2^{new} - \alpha_2^{old}|$ 尽可能大。由于

$$
\alpha_2^{new} = \alpha_2^{old} + \dfrac{y_2(E_1 - E_2)}{\eta}
$$

其中 $y_2, \eta, E_1$ 都是常数（当选定 $\alpha_1^{old}$ 时），那么要使 $|\alpha_2^{new} - \alpha_2^{old}|$ 尽可能大，只需使 $|E_1 - E_2|$ 尽可能大，这样就能确定 $\alpha_2^{old}$ 了。

> 注：
> （1）注意区分 $\pmb\alpha^{old}$ 和 $\pmb\alpha^{new}$，前者是当前迭代的已知输入，后者是当前迭代的输出。
> （2）KKT 条件的检验是在人为选取的精度 $\varepsilon$ 下进行的。

### 停机条件

为了使迭代结束，必须设置停机（边界）条件，显然我们最初的目的（使得所有样本点满足 KKT 条件）就是该条件。

$$
\sum_{i = 1}^n \alpha_iy_i = 0,~ 0 \le \alpha_i \le C,~ i = 1,2,\cdots,N
$$

$$
    y_ig(\pmb x_i) = \left\{
    \begin{aligned}
        &\ge 1, &\{\pmb x_i| \alpha_i = 0\}\\
        &= 1, &\{\pmb x_i|0 <\alpha_i < C\}\\
        &\le 1, &\{\pmb x_i|\alpha_i = C\}
    \end{aligned}
    \right.
$$

> 注：该检验是在人为选取的精度 $\varepsilon$ 下进行的。