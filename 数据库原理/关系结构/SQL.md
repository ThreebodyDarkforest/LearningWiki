---

mindmap-plugin: basic

---

# SQL

## SQL 数据定义

- 每个关系的模式
- 模式中每个属性的类型
	- char：定长字符串
	- varchar：不定长字符串
	- int, smallint, real, double precision
	- numeric(p, d)：p 有效位数，d 小数点后位数
	- float
- SQL 模式定义
	- 形式：`create table r(A1 D1(column constraint1), A2 D2(column constraint2), ..., <integrity-constraint1>, <ingerity-constraint2>);`
		- r：关系名
		- Ai：属性名
		- Di：属性类型
	- 用于保护数据完整性的限制（integrity consraints）：SQL 不允许违反这些限制的改动
		- 主键（primary key）
			- 不能为空（null），不能有相同元素
			- 最好定义它
		- 外键（foreign key）
			- 外键的取值必须跟被引用的主键值域相同
		- 非空（not null）
			- 该列不能取空值
	- 删除和添加列
		- 删除全表：`drop table <table name>`
		- 删除内容：`delete from <table name>`
		- 添加列：`alter table <table name>, add <attribute> <datatype> [integrity-constraint]`
		- 删除列：`alter table <table name>, drop <attribute>`
- SQL 查询语句
	- 形式：`select A1, A2, ..., An from r1, r2, ... rm where P`，等价于 $\prod_{A_1, A_2, \cdots, A_n}(\sigma_P(r_1\times r_2\times, \cdots,\times r_m))$
	- 选择列：`select`
		- 选择所有：`select *`
		- 允许数学运算：`select salary/12`
		- 允许别名：易于辨认，`select salary/12 as 月工资`
		- 去重：`select distinct dept_name`
	- 选择表：`from r1, r2, ..., rm`，是笛卡尔积
		- 跨表查询
		- 允许用自然连接，及它的隐患：两表相同属性名不同语义
		- 允许别名：同表比较，利用别名
	- 过滤条件：`where`
		- 允许比较运算
		- 允许逻辑关系连接
		- 允许函数
	- 字符串操作
		- `%` 匹配子串，`_` 匹配字符