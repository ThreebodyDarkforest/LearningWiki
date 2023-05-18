# 进阶SQL

## 连接

- 自然外连接
	- 定义：在自然连接基础上加几个（含 null 的）元组
	- 分类
		- 左连接 `natural left outer join`：保留左表与右表对不上的元组，其对应右表元素置空
		- 右连接：同理
		- 全连接 `full`：左连接和右连接合起来
- 内连接
	- `inner join`：只连接左右表匹配的元素，保留所有属性（包括相同的）
- `join` 操作数
	- `r natural join s`：自然连接
	- `r () join s on <predicate>`：join 的关联条件（如 A.属性 = B.属性）
	- `r () join s using (A1,A2...)`：要求两个关联字段在关联表中名称一致，而且只能表示关联字段值相等（如 `using (course_id)`）

## 视图

- 定义：`create view v as <query expression>`
- 特性
	- 不创建新表，只存储创建它的表达式
	- 创建后，查询时可以直接用这个视图
	- 单表可创建多个
- 目的
	- 安全
	- 个性化
- 视图更新
	- 方法：`insert into v values(A1, A2, ...)`
	- 限制
		- 数据来自单个表
		- 不能有聚集函数、复杂表达式和 `distinct`
		- 任何未被列出的属性的值都可以被置为空
		- 不含 `group by/having`
		- 不满足视图过滤条件的元组不能插入
- 实体化

## 事务

- 定义：一系列 sql 语句顺序执行
	- commit
	- rollback

## 完整性约束

- 作用：保证表更新是有效的，一致的
- 类型
	- `primary key`
	- `not null`
	- `unique`
	- `check(<predicate>)`
	- `foreign key`
	- `assertion`
- 特性
	- 一行可写多个限制 `unique(A1, A2, ...)`
	- 一个属性定义后可写（多个）限制 `name char(20) not null unique`
- 方法：`create table <name> ... ,[constraint1], ...,[constraintK]`
	- 表达式限制：约束属性取值 `check(attribute in (a1, a2, ...))`
	- 缺省值限制：`tot_cred numeric(3, 0) default 0`
	- 外部引用限制：被引用的列的属性域要跟引用的列相同
		- 外键可为 null，主键不能为 null
	- 级联操作（cascade）：`foreign key(attribute) reference table on delete cascade on update cascade`，同时增删引用表的数据和被引用表的数据
		- 外部引用限制被违反，不允许
	- 交叉引用：添加约束 `initially deferred` （允许限制检查在事务结束时执行）并在插入几条数据使得交叉引用不冲突后手动 `commit`
	- 断言（assertion）：一个总是被遵守的谓词表达式，`create assertion <a-name> check (<predicate>)`
		- 与 `check` 不同，不是针对单个列而是针对整个表或多个表间的数据约束

## 数据类型

- date
- time
- timestamp
- blob
- clob
- 用户定义类型
	- distinct type
		- 创建：`create type Dollars as numeric(12, 2) final`
		- 删除：`drop type, alter type`
	- structured type：允许创建具有嵌套记录结构、数组和多重集的复杂数据类型
- 用户定义属性域
	- 可以拥有限制和默认值
		- 创建：`create domain degree_level varchar(10) constraint degree_level_test check(value in (...))`
- 特性
	- 函数
	- 强制转换：`cast (department.budget to numeric(12, 2))`

## 授权

- 分类
	- 数据变动权限
	- 模式修改权限
- 特性
	- 创建者拥有所有权限
	- 创建者可以为其他人分配权限 `grant/revoke <previlege list> on <relation or view> to/from <user or role list>`
		- `role`：先定义才能用，是一组用户的集合
		- `grant option`：赋予给用户，使得他能够为其他用户分配某些权限

## 数据库便乘

- 高级语言 SQL 库
- SQL 函数
	- 调用类似 SQL 内置函数
	- `returns` 在最开头，内容放在 `begin end` 内
	- 返回值为一个数![IMG_0489.jpg](http://image.tjzfile.xyz/images/2023/04/07/IMG_0489.jpg)
	- 返回值为一个表/视图
- SQL 过程（Procedures）
	- 参数列表，`in` 输入参数，`out` 输出参数
	- 调用要 `Call`
- 过程性语句
	- `while/(repeat until)`
	- `{if/else then} end`，`case {when then} end`
- 触发器（trigger）
	- 特性
		- 响应事件
		- 为了满足完整性约束
		- 在特定条件下自动化执行
	- `before/after/instead of insert/update/delete on table`
	- 获取改动的行
		- `:new`
		- `refrencing new row as nrow`

