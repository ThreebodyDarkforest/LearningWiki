# ER模型

## 基本概念

- 基本对象
	- 实体集
		- 实体是独存的实在物
		- 实体有属性
		- 属性集是一组相同类型的实体
	- 关系集
		- relationship：一些实体之间的联系，是一个由多个实体的主键组成的元组
		- relationship 也可以有一些注释性属性
		- relationship set：一组相同类型的relationship
	- 属性集
		- 一个实体被一组属性表示
		- 域：属性可取的值
			- 简单属性
			- 复合属性：嵌套的属性
			- 多值属性
			- 派生属性：从其他属性计算可得
- 术语
	- relation：表
	- relationship：实体之间的关系
	- roles：参与一个 relationshp 的实体集扮演的功能。如果 relationship 涉及自指，则有必要显式地指明实体如何参与 relati onship

## 约束

- 与 integery constraint 不同
- 映射基数：表示一个实体通过一个联系集能关联的实体的个数
	- 一对一
	- 一对多：A 对 B，那么 B 里一个实体最多对一个 A 的实体
	- 多对一
	- 多对多
- 参与：某个实体参与某个关系
	- total：该实体集全部参与某个关系
	- partial：该实体集部分参与某个关系
	- 连线上的 `min...max`：参与的实体个数需要满足范围在 `min...max`

## 键

- 参与的所有实体集合的主键组成一个关系集的超键（superkey）
- 关系集的主键与SQL类似
	- 主键是 many 那边的
	- 一对一的都是主键

## 弱实体集

- 实体集分类
	- 强实体集：有主键
	- 弱实体集：属性不足以组成主键
- 辨识联系（identifying relationship）
	- 一个弱实体集必须与一个标识实体集（有主码的强实体集）有联系
	- 用双菱形表示这联系
	- 多（弱）对一（强）
	- 弱实体集 total participate
- 分辨符
	- 一组能够区分弱实体的属性（可以有多个）
	- 用虚线下划线表示
	- **弱实体集的主键由标识实体集的主键 + 弱实体集的分辨符号组成**

## ER模型转换为Schema

- 实体集
	- 强实体集：直接转换
	- 弱实体集：弱实体集的所有分辨符 + 依赖的强实体集的主码
- 联系集
	- 多对多：两个实体集的主码 + 联系的注释
	- 多对一：把**一侧的主码加到多侧**中
	- 一对一：除了自身的键，还添加另一侧的主码
	- 联系的注释可以写到多侧
- 复合属性：只写复合属性的底层属性，忽略多值属性
- 多值属性：创建一个新 relation，包含原表的主码和原表的多值属性
- 可能的错误：
	- 把主键写到其它实体集里去
	- 把主键写到联系集里去
- 当一个属性是由参与实体集的组合决定的，而不是由任一实体单独决定时，该属性必须与**多对多**关系集相关联。

## 扩展 ER 特性

- 特化
	- 概念上就是继承/模板特化偏特化，自顶向下设计
	- 用空心箭头从子指向父
- 泛化
	- 特化过程的逆，自底向上设计
- 聚集：即缩点，聚合是一种抽象，其中关系集（以及它们相关的实体集）被视为更高级别的实体集，并且可以参与关系。

