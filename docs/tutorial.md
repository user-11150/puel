<h1 align="center">UEL的教学——官方文档</h1>

# 前言
1. 本文档原文基于markdown编写，如果你的不是markdown编写的，有可能是因为你的经过中间人编译后分发，请注意文档格式是否正确，是否出现空白页，缺字等情况。
2. 本文档于贰零贰肆年伍月叁日开始编写，若不延长，将维护至贰零贰肆年拾贰月叁拾壹号，若延长，时间后续决定。
# 教程
## 专业术语或开发人员自定义术语
1. UP
他是指的UEL plan，主要是指代的UEL想要在未来修改或添加什么功能。
2. Build
指的是UEL的编译（编译器；编译流程）
3. Runner
指的是UEL的运行（运行时）
## Hello world——程序员梦开始的地方
```
put "Hello world"
```
好了，你现在已经入门UEL了，接下来让我们接着从示例一步步走向教学
## `put`的相关教学以及示例
`put`是一个关键字（下文会有介绍什么是关键字）。他可以让计算机在屏幕上输出文本（默认行为）。当然，你也可以不让他输出到屏幕上，可以输出到任何地方，比如一个文件，一个Stream，不过当前不会介绍太多，这样达到了吸引读者注意的效果，生动形象的写出了`put`的功能多的特点。

相信你已经有了基本认识了，接下来让我们看一个示例来达到深刻认识的效果
```
put "Hello world"
```
很简单，对吧，接下来我们可以引入加减
```
put 1 + 2
```
也很简单对吧，接下来让我们引入乘除
```
put 1 * 3
```
好，现在一个小小的`put`好像已经难不倒你了，接下来让我们看一些混合计算
```
put 1 * 3 + 2
put 2 + 3 * 5
```
先不要着急尝试，想想一想，结果会是什么？
结果是：1×3+2=3+2=5<br>
2+3×5=5×5=25

实际上这虽然反直觉，但是也是有规律的，永远从左到右，这样有利有弊，利是某些情况下可读性会更好
比如
```python
1 + 2 if condition else 5
```
有的人会以为是
```python
1 + (2 if condition else 5)
```
而有一部分人以为是
```python
(1 + 2) if condition else 5
```
*而作为重视可读性的UEL，肯定不会引入括号，因为它经常用于处理复杂的逻辑，如：*
```python
(1 / ((((π*r1)**2) / (v2 / π / 2)) ** 0.5)) ** 2
```
而优先级不是很好判断，虽然可以使用TeX

$$(1 ÷ {\sqrt{\frac{π(r_1)^2}{v_2 ÷ 2π}}})^2$$
虽然这样可以解决问题，但是源代码没法看了
```tex
(1 ÷ {\sqrt{\frac{π(r_1)^2}{v_2 ÷ 2π}}})^2
```

而不引入括号是一个很好的选择，他可以让程序的可读性更高。
## 变量的基本概念及认识
### 变量的概念
变量是大多数语言都有的特征，作用主要包括但不限于以下几种常见作用：
1. 给数据起个名字
2. 方便后续计算
3. 减少重复代码
### 语法——Syntax
`<name> = <value>`
其中，name是这个变量名的名称，可以理解为name是一个容器（不准确的叫法，方便小白理解）。而value就是这个容器的里面放的值。
eg：```
```
a = 5
```
eg：```
```
a = 48
```
很简单，对吧，让我们加入运算
eg:
```
a = 31 - 3
```
eg:
```
a = 12 - 3
```
需要注意的是值是存的时候计算好之后才存的进这“容器”中的，而不是使用时（下文介绍如何使用）才计算

也很简单，对吧，接下来让我们在计算或存入“容器”时使用变量
eg:
```
c = 2
d = 3
a = c + d
```
## 类型
### 何为类型
#### 简介
在其他语言（eg: C, C++, Java, Python等语言）中，常常会出现“类型”这个概念。那么UEL肯定也是有“类型”，这个概念的。
#### 字面意思
类：类别；分类；种类
型：形态；形体

接下来让我们组合起来吧！

类型：表示一个东西的种类
换句话说，一个东西是属于哪一个种类称之为类型。
#### UEL的内置类型
|名称|可取值|描述|eg|
|---|:---------|---------|--|
|string|字符串|字符串|`"a"`|
|number|任何数字|数字|143|
|boolean|true,false|布尔||

相同类型的运算通常符合直觉，接下来来看不同类型会发生什么……
### 类型不同怎么办？
报错
## 循环
循环就是用来把一段代码重复执行，接下来让我们看如何使用循环
eg:
```
repeat
  put 5
  put "
"
end
```
恭喜你，你已经学会了循环
## GQueue
GQueue是一个FILO的Queue。
### 如何操作
1. push
2. TOP
## 函数
需要：你需要先会GQueue
定义函数
eg:
```
function a arg1;
  put 5
end
```
调用
eg:
```
push 2
call a
```