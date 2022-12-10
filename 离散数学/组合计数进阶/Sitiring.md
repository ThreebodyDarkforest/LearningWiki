# 斯特林数

## 写在前面

斯特林数与 Catalan 数类似，都是从大量具有共性的计数问题中提炼出来的一个数学分布规律。我们将看到，它与阶乘幂有紧密的联系。

第一类斯特林数和第二类斯特林数都在考虑这样一个问题：将一个集合按某些规则划分为一些子集，而由于划分规则本身的联系，两类斯特林数有着有趣的联系。

## 第一类斯特林数

* 第一类斯特林数与如下问题的方法数相同：把一个集合 $S$ 中的所有元素划分成 $k$ 个不同的轮换，第一类斯特林数表示如下

$$
\left[
\begin{matrix}
    n\\k
\end{matrix}
\right]
$$

> 注：轮换指的是一个组循环同构的循环位移，比如 $(1, 2, 3), (2, 3, 1)$ 是同一个轮换，而 $(1, 2, 3), (3, 2, 1)$ 则不是同一个轮换。

第一类斯特林数不存在通项公式，只有递推关系式

$$
\left[
\begin{matrix}
    n\\k
\end{matrix}
\right] = (n - 1)
\left[
\begin{matrix}
    n - 1\\k
\end{matrix}
\right] +
\left[
\begin{matrix}
    n - 1\\k - 1
\end{matrix}
\right]
$$

这个关系是显然的，如果我们考虑第 $n$ 个元素的放置方法，那么会有两种方案：

1. 要么新开一个轮换，这个轮换只有 $n$ 这个元素
2. 要么加入已有的 $n - 1$ 个轮换中

递归边界为

$$
\left[
\begin{matrix}
    n\\1
\end{matrix}
\right] = (n - 1)!
$$

$$
\left[
\begin{matrix}
    n\\0
\end{matrix}
\right] = 1, 
\left[
\begin{matrix}
    0\\0
\end{matrix}
\right] = 1
$$

第一条边界不是那么好理解，这涉及到含 $n$ 个元素的单个轮换的所有可能的形状总数，不难发现固定任一元素后，其余元素的每一个排列都是一个轮换（固定位置的元素不可能在少于 $n$ 次位移时与原排列在这位置上的元素相同）。

## 第二类斯特林数

第二类斯特林数与第一类斯特林数非常类似，只有选取子集的规则不同。

* 第二类斯特林数与如下问题的方法数相同：把一个集合 $S$ 中的所有元素划分成 $k$ 个不同的子集，第二类斯特林数表示如下

$$
\left\{
\begin{matrix}
    n\\1
\end{matrix}
\right\}
$$

第二类斯特林数存在通项公式，因为子集是容易计数的。

$$
\left\{
\begin{matrix}
    n\\k
\end{matrix}
\right\} = \dfrac{1}{k!}\sum_{t = 0}^k(-1)^t\binom{k}{t}(k - t)^n
$$

第二类斯特林数可以这样计算：考虑 $n$ 个互异的球和 $k$ 个**互异**的盒子，求每个盒子非空的不同的分球方法数，假设为 $T$，那么 $T / k!$ 即为答案（原问题不要求互异，但是通过假设一个新的问题，原问题变得好求）。

由**容斥原理**，假设 $A_i$ 表示第 $i$ 个盒子为空的情况，那么

$$
\begin{aligned}
    T = |\Omega| - |\bigcup A_i| &= |\Omega| - \sum|A_i| + \sum|A_i \cap A_j|\cdots + (-1)^k|\bigcap A_i|\\ 
    &= \sum_{t = 0}^k(-1)^t\binom{k}{t}(k - t)^n 
\end{aligned}
$$

除了这种使用容斥原理的直接计数方法，我们还可以递归地求解这个问题，思路跟第一类斯特林数是十分相似的，同样地，我们来考虑第 $n$ 个放入盒子中的球，这个球有两种可能的放法：

1. 放入一个新的盒子中
2. 在 $k$ 个已经有球的盒子中选一个放入

$$
\left\{
\begin{matrix}
    n\\k
\end{matrix}
\right\} = k - 1
\left\{
\begin{matrix}
    n - 1\\k
\end{matrix}
\right\} + 
\left\{
\begin{matrix}
    n - 1\\k - 1
\end{matrix}
\right\}
$$

边界条件也是类似的考虑

$$
\left\{
\begin{matrix}
    n\\1
\end{matrix}
\right\} = 1
$$

$$
\left\{
\begin{matrix}
    n\\0
\end{matrix}
\right\} = 0,
\left\{
\begin{matrix}
    0\\0
\end{matrix}
\right\} = 1
$$

## 阶乘幂与普通幂

阶乘幂是一类特殊的多项式，分为上阶乘幂和下阶乘幂

* 下阶乘幂

$$
x^{\underline n} = x(x - 1)\cdots(x - n + 1)
$$

* 上阶乘幂

$$
x^{\overline{n}} = x(x + 1)\cdots(x + n - 1)
$$

不难发现，实际上 $x^{\underline n}, x^{\overline{n}}$ 都是最高次数为 $n$ 的多项式。

一般更为常用的是下阶乘幂，主要是因为它与一些离散数学性质有关，下面我们会看到它与离散积分和离散微分的关系。

### 上阶乘幂与普通幂

$$
x^{\overline{n}} = \sum_k
\left[
\begin{matrix}
    n\\k
\end{matrix}
\right]x^k
$$

$$
x^n = \sum_k
\left\{
\begin{matrix}
    n\\k
\end{matrix}
\right\}(-1)^{n - k}x^{\overline{k}}
$$

> 注：这些性质多半是通过观察得到的（直接展开阶乘幂），而证明直接暴力归纳即可。

### 下阶乘幂与普通幂

$$
x^{\underline n } = \sum_k
\left[
\begin{matrix}
    n\\k
\end{matrix}
\right](-1)^{n - k}x^k
$$

$$
x^n = \sum_k
\left\{
\begin{matrix}
    n\\k
\end{matrix}
\right\}x^\underline{k}
$$

### 下阶乘幂与上阶乘幂

$$
x^\overline{k} = (-1)^k(-x)^{\underline{k}}
$$

这个结论可以通过一个相当浅显的推导得出

$$
\begin{aligned}
    x^\overline{k} &= x(x + 1)\cdots(x + k - 1)\\
    &= (-1)^k(-x)(-x - 1)(-x - 2)\cdots(-x - k + 1)\\
    &= (-1)^k(-x)^{\underline{k}}
\end{aligned}
$$里三积分

> 注：这个性质精巧地对应着上阶乘幂和下阶乘幂的某种对称性质，你可以在前两条性质发现它。

### 乘幂求和

在具体数学对离散导数和离散积分进行了定义：

* 离散微分

$$
g(x) = \Delta f(x) = f(x + 1) - f(x)
$$

* 离散积分

$$
\sum_a^bg(x)\delta x = \left.f(x)\right|_a^b = f(b) - f(a)
$$

下阶乘幂有一个神奇的性质，这个性质决定了它在离散数学中的重要性

$$
\Delta(x^\underline{m}) = mx^{\underline{m - 1}}
$$

$$
\sum_{0\le k < n}k^{\underline{m}} = \left.\dfrac{k^{\underline{m + 1}}}{m + 1}\right|_0^n = \dfrac{n^{\underline{m + 1}}}{m + 1}
$$

可以看到，它们与实函数的导数和积分公式形式一致，正是得益于这一点，下阶乘幂有广泛的应用。

> 注：这两个关系神奇就神奇在给出了一种对幂级数求和的方法。

一个常见的例子是求一个长度为 $n$ 的正整数数列的任意幂次和，也就是我们从小学求到大学的这么一个东西

$$
1^2 + 2^2 + \cdots + n^2
$$

这个就是二次幂和。我们曾经使用了不计其数的方法来求解这个问题，现在这里又有了一个新的方法。思路应当是显然的，就是将所有的普通幂转换成下阶乘幂，再利用上面提到的离散积分和离散微分的性质来做（因为有个求和号嘛）。

> 注：这个解法的主要难点在于斯特林数的求解。