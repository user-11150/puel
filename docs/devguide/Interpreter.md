<h1>
  <p>解释器（Interpreter）——UEL运行时的核心</p>
</h1>

## 1. 依赖
1. Stack => 因为*UEL*是stack based的，所以stack是必须有的。
2. GQUEUE => 模拟队列
## 2. 如何实现？
> 你必须达到以下（↓）的目录结构以便于更好的实现

```
runner
    |--> Stack.py
    |--> Ueval.py
```
---
其中，Stack模拟栈，Ueval模拟CPython执行Bytecode的文件名