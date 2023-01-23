# 核方法与非线性支持向量机

## 非线性支持向量机

对于某些非线性可分的问题，它也有可能仍然是可以进行（近似）二分类的，只不过分类不是用直线或超平面，而是用超曲面。比如下图使用圆锥曲线来进行分类的情形。

![QQ20230119104628.png](http://image.tjzfile.xyz/images/2023/01/19/QQ20230119104628.png)

这类问题直接用 SVM 是做不出来的，无论是软间隔还是硬间隔 SVM 都只能解决线性问题。但是，如果我们通过一个非线性变换将原始向量空间映射到另一个高维空间，这些向量就有可能在这个高维空间中线性可分，这个问题就能通过 SVM 解决，这就是核方法的基本思想。

* 找到一个映射 $\pmb x\rightarrow \phi(\pmb x)$，使得原问题变为线性问题。
* 用 SVM 解决该线性问题，进而解决原问题。

> 注：其中 $\pmb x\in R^n$ 在输入空间中，而 $\phi(\pmb x)$ 在一个被称为希尔伯特空间 $\mathcal H$ 的高维空间中，它甚至可以是无穷维的。这个映射实质上将输入空间中的超曲面模型映射到了希尔伯特空间中的超平面模型。
> 关于希尔伯特空间，可以参考[这篇文章](
https://www.zhihu.com/question/332144499/answer/731866608)和[维基百科](https://zh.wikipedia.org/wiki/%E5%B8%8C%E5%B0%94%E4%BC%AF%E7%89%B9%E7%A9%BA%E9%97%B4)，这是泛函分析的内容。

## 核方法

前文提到了输入空间到希尔伯特空间的非线性变换 $\phi(\pmb x)$，但是 $\phi(\pmb x)$ 往往是难以得出的。不过，通过一些泛函分析手段，我们会发现在 $\mathcal H$ 上的内积容易求出，即 $\phi(\pmb x)\cdot \phi(\pmb z), x,z\in \mathcal{H}$。通过观察 SVM 的分类超平面（在间隔最大化的求解过程中定义）

$$
\pmb\omega\pmb x + b = \sum_{i = 1}^n\alpha_i^*y_i(\pmb x_i\cdot\pmb x) + b = 0
$$

和 SVM 面对的凸优化问题

$$
\begin{aligned}
    &\min_{\pmb\alpha}\dfrac{1}{2}\sum_{i = 1}^n\sum_{j = 1}^n\alpha_i\alpha_jy_iy_j\pmb x_i^T\pmb x_j + \sum_{i = 1}^n\alpha_i\\
    st.&\  0 \le \alpha_i \le C\\
    & \sum_{i = 1}^n\alpha_iy_i = 0\\
\end{aligned}
$$

不难发现它们都只出现了输入空间中的内积，那么要将该问题映射到 $\mathcal H$，只需要将 $\pmb x_i\cdot \pmb x_j$ 映射到 $\phi(\pmb x_i)\cdot\phi(\pmb x_j)$ 即可，因此我们实际上只需要隐式地考虑 $\phi(\pmb x)$ 即可，并不用了解它具体的表达式。在此基础上，我们把 $K(\pmb x,\pmb z) = \phi(\pmb x)\cdot\phi(\pmb z)$ 定义为**核函数**

> 设 $\mathcal X$ 是输入空间（欧氏空间 $R^n$ 的子集或离散集合），又设 $\mathcal{H}$ 为特征空间（希尔伯特空间），如果存在一个 $\mathcal X\rightarrow\mathcal H$ 的映射
> $$
> \phi(\pmb x): \mathcal X\rightarrow \mathcal H
> $$
> 使得对所有 $\pmb x,\pmb z\in \mathcal X$ 函数 $K(\pmb x, \pmb z)$ 满足条件
> $$
> K(x,z) = \phi(\pmb x)\cdot\phi(\pmb z)
> $$
> 则称 $K(\pmb x, \pmb z)$ 为核函数，$\phi(\pmb x)$ 为映射函数。

于是原问题映射到特征空间后变为

$$
\begin{aligned}
    &\min_{\pmb\alpha}\dfrac{1}{2}\sum_{i = 1}^n\sum_{j = 1}^n\alpha_i\alpha_jy_iy_j\pmb K(\pmb x_i,\pmb x_j) + \sum_{i = 1}^n\alpha_i\\
    st.&\  0 \le \alpha_i \le C\\
    & \sum_{i = 1}^n\alpha_iy_i = 0\\
\end{aligned}
$$

分类超平面变为

$$
\sum_{i = 1}^n\alpha_i^*y_iK(\pmb x_i, \pmb x) + b = 0
$$

这相当于在特征空间 $H$ 中隐式地（不必知道 $\phi(\pmb x)$ 的具体表达式）学习一个非线性模型，在 $\mathcal H$ 中应用 SVM 学得的线性模型实际上对应于输入空间中的一个非线性模型。