# 三分钟可复现展示

这是给黑客松评审、新用户和贡献者看的最短体验路径。

## 第一分钟：证明项目真的能跑

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
aidoc doctor --config examples/acceptance.example.json
```

你会看到 required 检查通过，optional 的模型 Key 即使没有配置也只会 WARN。

## 第二分钟：证明它不是“打分器”

```bash
aidoc doctor --config examples/broken.example.json
```

这个例子故意缺少一个必要的验收文件。

核心输出：

```text
FIRST BLOCKER  missing-acceptance-artifact
```

它不会告诉你“生产就绪度 82 分”，也不会把一次失败直接脑补成根因。

它只做一件更克制的事：

> 找到当前交付链中第一处无法被证据证明成立的必要环节。

## 第三分钟：证明 Agent 和确定性程序可以分工

仓库包含：

```text
.agents/skills/ai-delivery-doctor/SKILL.md
```

Agent 负责理解：

- 用户真正想交付什么；
- 哪几个环节必须被验证；
- 如何写一个小而明确的 acceptance contract。

AI Delivery Doctor 核心程序负责：

- 真正执行检查；
- 产生 PASS / WARN / FAIL；
- 保存证据；
- 给出第一处 blocker。

一句话概括：

> **让 AI 判断“该证明什么”，让确定性程序证明“实际上发生了什么”。**

## 路演建议

演示顺序不要从架构图开始。

直接先跑 passing example，再跑 broken example。

观众会立刻看到：

1. 这是能运行的；
2. 它处理的是 AI 最后一公里；
3. 它不是另一个 Agent 框架；
4. 它把“AI 自信地说能用”变成“拿证据证明能用”。
