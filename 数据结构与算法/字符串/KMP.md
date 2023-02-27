# KMP算法

> 之前[学OI的时候](https://www.cnblogs.com/DarkValkyrie/p/11268983.html)其实是没怎么学会KMP的，现在再看一遍才算是学明白了，顿感当时写得实在是非常烂，故再写一篇。

## 写在前面

首先我们当然要知道，KMP算法是用来在字符串中寻找子串位置的。

比起暴力枚举，KMP试图利用模式串的自相似性**自递归地**寻找串内前后缀一致的部分，并试图通过这种信息来加速字符串的模式匹配。

> 注：
> （1）串的前后缀：顾名思义，就是从一个串最开头往后的一个子串或最末尾往前的一个子串。
> （2）模式串：一个相对短一点串，或者说一个我们希望在目标字符串中寻找其位置的子串。
> （3）模式匹配：在目标字符串中寻找子串的过程。

其实光看代码你会以为这是个递推，但是这算法实际上应该算是递推+递归，就全局计算过程来看，它是递推的，但是在计算每一个递推值时，它却是通过递归计算的。

## 算法步骤

首先说暴力。

你可以形象地把暴力的做法理解成这样：拿模式串叠在主串上，一开始就叠在主串的头部。然后从模式串的头开始逐个字符进行比对，每当匹配不上，就把模式串在主串上整体往后挪一个字符，再匹配一次，依此类推。

```cpp
step 1:
abcdab(c)da...
abcdab(e)fg
c!=e

step 2:
a(b)cdabcda...
 (a)bcdabefg
b!=a

step 3:...
```

不过说实话，你难道不觉得这么一点一点地挪看上去很费事吗？而且确实，在最坏情况下暴力的复杂度在 $O(nm)$ 的级别（主串长 $n$，模式串长 $m$）。

KMP也发现了这一点，它的的核心思想就是尽可能在每次失配的时候把这个模式串挪远一点，这个操作就依赖于模式串的子串的自相似性，更具体地说是**模式串的前缀子串的相同前后缀有多长**（注意，这里就是个递归定义了）。

举个例子，这是一个模式串

```cpp
abcdabefgh
```

这是该模式串的一个前缀子串

```cpp
abcdab
```

它们显然具有相同的前后缀 `ab`，长度为 $2$。

然后KMP也没什么高深的，它就是暴力的改进，说白了也是搁主串上挪模式串这么一个事儿。

我们可以假想一下模式串的某个真前缀子串的前后缀是一样的，比如这个模式串 `abcdabefg`，它有一个真前缀 `abcdab` 的前后缀 `ab` 是一样的，而且是最长的。如果主串长这样 `abcdabcda...`，显然会在 `e != c` 这里失配。

```cpp
abcdab(c)da...
abcdab(e)fg
```

KMP做了一件十分有意思的事，就是直接把模式串移到主串第二个 `ab` 所在的地方，也就是这样

```cpp
abcdabcda...
    abcdabefg
```

然后再逐个字符匹配。

不难发现，这正是因为模式串的真前缀 `abcdab` 具有相同的前后缀 `ab` ，才能使得在这个真前缀的后一个字符（`e != c`）失配时能够直接把模式串往后挪到主串中与真前缀相同的子串的后缀 `ab` 所在的位置。

至于这种操作的正确性（为什么能直接挪这么多格），用**反证法**是很好证明的，你不妨仔细想一下前面说的**最长相同前后缀**是什么意思。

不失一般性，这个性质对任意模式串的任意真前缀都成立。注意这里又是一个递归的性质，因为模式串的真前缀中又有真前缀。

那么这个操作怎么实现呢？答案是搞一个辅助数组 $next[i]$ 记录模式串真前缀自相似信息，这样说太笼统了，下面具体来看看。

> 下面为了方便讨论，设主串 $s$，模式串 $ms$。

我们这样定义 $next[i]$：

* $next[i]$ 从下标 $1$ 开始。
* $next[i]$ 仅仅是模式串的信息计算得到的。
* $next[i]$ 定义为模式串中第 $i$ 个字符（不包括 $i$）之前的真前缀 $s[1\sim i - 1]$ 中的最长相同前后缀的长度 $+1$。
* $next[i]$ 的使用意义为模式串在第 $i$ 个字符失配时应当重新开始匹配的位置。
* $next[i] = k$ 意味着 $s[1\sim k] = s[i - k + 1\sim i]$。

比如： `abcdabcda` 的 $next[7] = 3$，这意味着 $s[1\sim 2] = s[5\sim 6]$。

首先我们要搞清楚这个数组怎么用于KMP算法，先把代码贴出来。

```cpp
// 记得下标都从 1 开始
int kmp(string s, string ms)
{
    int len_s = strlen(s), len_ms = strlen(ms);
    int i = 1, j = 1;
    while(i <= len_s && j <= len_ms) {
        if(j == 0 || s[i] == ms[j]) { i++, j++; }
        else j = next[j];
    }
    if(j > len_ms) return i - len_ms;
    else return 0;
}
```

也就是先正常匹配，失配的时候就**不断跳转**模式串的匹配指针 $j$ 到 $next[j]$，直到之前失配的字符可以被匹配（或重新开始匹配）。这里的跳转，其实就等价于之前的挪模式串这么一个操作。

但是别忘了，现在 $next[i]$ 怎么算我们还不知道，而这部分才是重头戏——这需要一个自递归求解方法。

也是先上代码。

```cpp
// 记得下标都从 1 开始
void kmp_next(string ms)
{
    int len_ms = strlen(ms);
    int i = 1, j = 0;
    while(i <= len_ms) {
        if(j == 0 || ms[i] == ms[j]) { i++, j++; next[i] = j; }
        else j = next[j];
    }
}
```

好吧，我承认我是从上面复制粘贴的，因为事实上这算法就等同于在模式串上做模式串匹配，只不过是在匹配模式串的所有真前缀的真前缀和真后缀罢了。

首先，从小问题推出大问题，确实是递推，但是在求解每一个 $next[i]$ 时，如果偶遇失配的情况，就需要对子串 $ms[1\sim j]$ 进行递归了。这个过程就是 $j$ 不断地向 $next[j]$ 跳转，直到此时 $ms[1\sim j]$ 拥有最长相同前后缀，即最大的 $k$ 使 $ms[1\sim k] = ms[j - k + 1\sim j]$，然后 $next[i + 1] \leftarrow k + 1$。

至于这个算法为什么正确，看图。

![Screenshot-from-2022-09-21-20-12-00.png](http://image.tjzfile.xyz/images/2022/09/21/Screenshot-from-2022-09-21-20-12-00.png)
![Screenshot-from-2022-09-21-20-12-06.png](http://image.tjzfile.xyz/images/2022/09/21/Screenshot-from-2022-09-21-20-12-06.png)
![Screenshot-from-2022-09-21-20-12-11.png](http://image.tjzfile.xyz/images/2022/09/21/Screenshot-from-2022-09-21-20-12-11.png)
![Screenshot-from-2022-09-21-20-24-30.png](http://image.tjzfile.xyz/images/2022/09/21/Screenshot-from-2022-09-21-20-24-30.png)

$next$ 数组的自递归和自相似的性质一览无余。

直接分析代码就能看出复杂度，显然 KMP 和 $next$ 数组的计算里面 $i$ 都没有半点回溯的意思，所以最坏复杂度也就是 $O(n + m)$。

## 模板

板子在这 [P3375](https://www.luogu.com.cn/problem/P3375)，把我 n 年前的题解拿出来贴着。

```cpp
#include<cstdio>
#include<iostream>
#include<cmath>
#include<cstring>
#include<ctime>
#include<cstdlib>
#include<algorithm>
#include<queue>
#include<set>
#include<map>
#define N 1000010
using namespace std;
int next[N];
char a[N],b[N];
int main()
{
	cin>>a+1,cin>>b+1;
	int la=strlen(a+1),lb=strlen(b+1);
	int j=0;
	for(int i=2;i<=lb;i++){
		while(j&&b[j+1]!=b[i]) j=next[j];
		if(b[j+1]==b[i]) j++;
		next[i]=j;
	}
	j=0;
	for(int i=1;i<=la;i++){
		while(j&&b[j+1]!=a[i]) j=next[j];
		if(b[j+1]==a[i]) j++;
		if(j==lb){
			printf("%d\n",i-lb+1);
			j=next[j];
		}
	}
	for(int i=1;i<=lb;i++) printf("%d ",next[i]);
	return 0;
}

```