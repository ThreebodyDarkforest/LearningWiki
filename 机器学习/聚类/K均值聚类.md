# K 均值聚类

## 写在前面

聚类是一种无监督学习方法，而 K 均值聚类是最简单常用的聚类方法，多用于数据预处理和特征工程。聚类算法通常试图将数据集中的样本点分为 $m$ 簇，使得这 $m$ 簇样本点之间的距离尽可能大，而单个簇内的样本点之间的距离尽可能小。注意，$m$ 多数情况下为人为确定的超参数，有时距离也会换成相似度（如余弦相似度）。

## 样本相似度度量

聚类的核心是样本距离或相似度，有多种相似度和距离的定义。因为相似度直接影响聚类的结果，所以其选择是聚类的根本问题。

聚类的输入与其它机器学习方法的输入一样，都是由 $m$ 个属性组成 $R^m$ 输入空间 $\mathcal{X}$ 中的 $n$ 个样本点。这样一来，只要能把属性值量化，那么就可以在空间中度量样本点之间的距离，不妨设 $x_{ij}$ 表示第 $j$ 个样本的第 $i$ 个属性值（假设数据集为一组列向量）。

### 属性类型

* 连续属性：在定义域上有无穷多个取值。
* 离散属性：在定义域上有有限个取值。
* 有序属性：属性值存在大小关系。
* 无序属性：属性值不存在大小关系。

### 闵可夫斯基距离

设有两样本 $x_i,x_j\in \mathcal{X}$（两列向量），样本 $x_i$ 和 $x_j$ 之间的闵可夫斯基距离定义为

$$
d_{ij} = ({\sum_{k = 1}^m|x_{ki} - x_{kj}|^p})^{\frac{1}{p}}
$$

其中 $p$ 的取值可选，当

* $p = 1$ 时，该距离称为曼哈顿距离，可理解为平行坐标轴的折线距离
$$
d_{ij} = \sum_{k = 1}^m|x_{ki} - x_{kj}|
$$
* $p = 2$ 时，称为欧式距离，即最常用的距离。
* $p = \infty$ 时，称为切比雪夫距离
$$
d_{ij} = \max_{k}|x_{ki} - x_{kj}|
$$

> 注：
> （1）闵可夫斯基距离常用于属性值有序的情况。

### 马哈拉诺比斯距离

给定样本集合 $X = [x_{ij}]_{m\times n}$，其协方差矩阵记为 $S$，那么 $x_i$ 和 $x_j$ （列向量）之间的马哈拉诺比斯距离为

$$
d_{ij} = [(x_i - x_j)^TS^{-1}(x_i - x_j)]^{\frac{1}{2}}
$$

> 注：
> （1）马哈拉诺比斯距离计算的结果与特征的尺度无关。
> （2）马哈拉诺比斯距离考虑各个特征之间的相关性（协方差）。
> （3）马哈拉诺比斯距离常用于属性值有序的情况。

### 相关系数

$$
r_{ij} = \dfrac{\sum_{k = 1}^m(\pmb x_{ki} - \overline{\pmb x}_i)(\pmb {x}_{kj} - \overline{\pmb x}_{j})}{\left[\sum_{k = 1}^m(\pmb x_{ki} - \overline{\pmb x_i})^2\sum_{k = 1}^m(\pmb x_{kj} - \overline{\pmb x}_{j})\right]^{\frac{1}{2}}}
$$

> 注
> （1）相关系数的绝对值越接近 $1$ 表明样本越相似，越接近 $0$ 表明越不相似。
> （2）一般来说，距离越小越相关，相似度越大越相关。

### 余弦相似度

$$
s_{ij} = \dfrac{\sum_{k = 1}^mx_{ki}x_{kj}}{\left(\sum_{k = 1}^mx_{ki}^2\sum_{k = 1}^mx_{kj}^2\right)^{\frac{1}{2}}}
$$

> 注：余弦相似度的值越接近 $1$ 表明样本越相似，越接近 $0$ 表明越不相似。

### VDM

属性 $k$ 上两个离散值 $a, b$ 之间的 VDM 距离为

$$
VDM_p(a, b) = \sum_{i = 1}^d\left|\dfrac{m_{u, a, i}}{m_{u, a}} - \dfrac{m_{u, b, i}}{m_{u, b}}\right|^p
$$

其中 $m_{u, a}$ 表示在属性 $u$ 上取值 $a$ 的样本数，$m_{u, a, i}$ 表示在第 $i$ 个簇中在属性 $u$ 上取值 $a$ 的样本数，$d$ 为样本簇数，$p$ 是人为确定的参数。

> 注：VDM 距离可以处理无序离散属性。

### 混合属性

将闵可夫斯基距离和 VDM 相结合，可以同时处理无序属性和有序属性

$$
MinkovDM_p(\pmb x_i, \pmb x_j) = \left(\sum_{k = 1}^{m_c}|\pmb x_{ki} - \pmb x_{kj}|^p + \sum_{k = m_c + 1}^m VDM_p(\pmb x_{ki}, \pmb x_{kj})\right)^{\frac{1}{p}}
$$

其中 $m_c$ 为有序属性的个数。

## 簇的性质

一个簇是聚类得到的一个样本子集。下面用 $G$ 表示簇，用 $\pmb x_i, \pmb x_j$ 表示簇中样本，用 $n_G$ 表示簇中样本个数，用 $d_{ij}$ 表示样本 $\pmb x_i, \pmb x_j$ 间的距离。

### 簇的均值

簇的均值 $\overline{\pmb x}_G$，又称为簇心

$$
\overline{\pmb x}_G = \dfrac{1}{n_G}\sum_{i = 1}^{n_G}\pmb x_i
$$

其中 $n_G$ 为簇 $G$ 包含的样本个数。

### 簇的直径

簇的直径 $D_G$ 是簇中任意两个样本之间的最大距离

$$
D_G = \max_{\pmb x_i, \pmb x_j\in G} d_{ij}
$$

### 簇的样本散布矩阵

簇 $G$ 的样本散布矩阵 $A_G$ 为

$$
A_G = \sum_{i = 1}^{n_G}(\pmb x_i - \overline{\pmb x}_G)(\pmb x_i - \overline{\pmb x}_G)^T
$$

样本协方差矩阵 $S_G$ 为

$$
S_G = \dfrac{1}{n_G - 1}A_G = \dfrac{1}{n_G - 1}\sum_{i = 1}^{n_G}(\pmb x_i - \overline{\pmb x}_G)(\pmb x_i - \overline{\pmb x}_G)^T
$$

### 簇间距离

簇间距离有几种不同的定义方法。

#### 最短距离或单连接

簇 $G_p$ 的样本与 $G_q$ 中样本之间的最短距离

$$
D_{pq} = d_{min}(G_p, G_q) = \min\{d_{ij}|\pmb x_i\in G_p. \pmb x_j\in G_q\}
$$

#### 最长距离或完全连接

簇 $G_p$ 的样本与 $G_q$ 的样本之间的最长距离

$$
D_{pq} = d_{max}(G_p, G_q) = \max\{d_{ij}|\pmb x_i\in G_p. \pmb x_j\in G_q\}
$$

#### 中心距离

簇 $G_p$ 与 $G_q$ 的中心 $\overline{\pmb x}_p, \overline{\pmb x}_q$ 之间的距离

$$
D_{pq} = d_{cen}(G_p, G_q) = d_{\overline{\pmb x}_p, \overline{\pmb x}_q}
$$

#### 平均距离

簇 $G_p$ 与 $G_q$ 任意两个样本之间距离的平均值

$$
D_{pq} = \text{avg}(G_p, G_q) = \dfrac{1}{n_qn_p}\sum_{\pmb x_i\in G_p}\sum_{\pmb x_i\in G_q} d_{ij}
$$

### 簇内距离

簇内距离有几种，定义如下

#### 平均距离

$$
\text{avg}(G_p) = \dfrac{1}{|G_p|(|G_p - 1|)}\sum_{1\le i\le j\le |G_p|}d_{ij}
$$

#### 最远距离

$$
d_{max}(G_p) = \max_{1\le i\le j\le |G_p|}d_{ij}
$$

#### 最近距离

$$
d_{min}(G_p) = \max_{1\le i\le j\le |G_p|}d_{ij}
$$

> 注：
> （1）注意区分簇间距离和簇内距离。簇间距离是单一指标但有多种可选方案，比如用簇间最短距离和簇中心距离来度量簇间距离是不同的方案。但是簇内距离的几个指标是分立的指标。

## 性能度量

性能度量分为外部指标和内部指标两种，其中

* 外部指标依赖于外部给定的样本真实类别标签，需要类似有监督学习的 $(\pmb x_i, y_i)$ 的特征向量-标记对。
* 内部指标只根据聚类结果进行度量，不依赖外部信息。

### 外部指标

对数据集 $D = \{\pmb x_1,\pmb x_2,\cdots,\pmb x_m\}$，设聚类结果 $G = \{G_1, G_2,\cdots, G_d\}$，外部类别标记 $G^* = \{G_1^*, G_2^*, \cdots, G_s^*\}$，并设 $\pmb\lambda = \{\lambda_1, \lambda_2, \cdots,\lambda_m\}, \pmb\lambda^* = \{\lambda_1^*, \lambda_2^*, \cdots,\lambda_m^*\}$ 表示与 $G, G^*$ 对应的簇标记向量。

接下来定义一些评价参数

$$
a = |SS|, SS = \{(\pmb x_i, \pmb x_j)|\lambda_i = \lambda_j, \lambda_i^* = \lambda_j^*, i < j\}\\
b = |SD|, SD = \{(\pmb x_i, \pmb x_j)|\lambda_i = \lambda_j, \lambda_i^* \neq \lambda_j^*, i < j\}\\
c = |DS|, DS = \{(\pmb x_i, \pmb x_j)|\lambda_i \neq \lambda_j, \lambda_i^* = \lambda_j^*, i < j\}\\
d = |DD|, DD = \{(\pmb x_i, \pmb x_j)|\lambda_i \neq \lambda_j, \lambda_i^* \neq \lambda_j^*, i < j\}\\
$$

且 $a + b + c + d = \dfrac{m(m - 1)}{2}$

那么接下来就可以定义这些外部指标了

* Jaccard 系数
$$
JC = \dfrac{a}{a + b + c}
$$
* FM 指数
$$
FMI = \sqrt{\dfrac{a}{a + b}}\sqrt{\dfrac{a}{a + c}}
$$
* Rand 指数
$$
RI = \dfrac{2(a + b)}{m(m - 1)}
$$

这些指数都在 $[0, 1]$，且越大越好。

### 内部指标

* DB 指数

$$
DBI = \dfrac{1}{d}\sum_{i = 1}^d\max_{j\neq i, 1\le j\le d}\left(\dfrac{\text{avg}(G_i) + \text{avg}(G_j)}{d_{cen}(G_i,G_j)}\right)
$$

* Dunn 指数

$$
DI = \min_{1\le i\le d}\left\{\max_{j\neq i}\left(\dfrac{d_{min}(G_i, G_j)}{\underset{{1\le l\le k}}{\max}d_{max}(G_l)}\right)\right\}
$$

## 算法原理

K 均值聚类实质上是一个最优化问题，它希望所有样本点到该点所在簇的中心的距离之和最小，以此为目的将 $n$ 个点划分到 $d$ 个簇。但是，由于原始最优化问题的求解是 NP 难的，因此 K 均值聚类使用迭代求解。

K 均值聚类的算法流程其实相当简单

（1）初始化 $d$ 个簇心。

（2）将样本点逐个分配到与其距离最近的簇心所在的簇中，得到聚类结果。

（3）更新每个簇的簇均作为新的簇心。

（4）若新簇心与旧簇心相同，则停机，否则转（2）。

> 注：聚类结果的质量可以用簇的平均直径来衡量，且随着簇数增大，簇的平均直径单调递减，因此簇数 $d$ 的选择可以通过二分查找来寻求较优解。