# AI Delivery Doctor｜黑客松展示说明

## 作品一句话

**让 AI 判断“该证明什么”，让确定性程序证明“实际上发生了什么”。**

AI Delivery Doctor 面向 FDE、AI 应用工程师、Agent/RAG/MCP 项目开发者，解决一个非常具体的问题：

> AI Demo 已经能跑，但在交付、上线、排障和验收时，我们怎么证明整条链路真的成立？

## 服务对象

- FDE / AI 实施 / AI 解决方案工程师；
- Agent / RAG / MCP 开发者；
- 需要把 AI POC 交给真实用户或客户的团队；
- 需要在 CI / 部署前后留下可复验证据的人。

## 核心痛点

传统排障经常出现：

- “进程启动了，所以应该没问题”；
- “接口 200 了，所以业务应该通了”；
- “Agent 说配置正常，所以应该能交付”；
- “十个检查九个通过，所以生产就绪度 90%”。

这些判断都可能把真正的关键阻塞项淹没。

AI Delivery Doctor 使用**有顺序的交付契约**，把链路拆成可以被观察的条件，并找到第一处 required FAIL。

## 一条命令演示

安装后运行：

```bash
python scripts/showcase.py
```

这个完全合成、无网络依赖的演示会自动完成：

```text
交付条件缺失
   ↓
Doctor 发现 required FAIL
   ↓
FIRST BLOCKER = handoff-receipt
   ↓
在临时目录创建合成验收证据
   ↓
重新执行同一份 contract
   ↓
required check → PASS
   ↓
比较 before / after evidence
   ↓
IMPROVED
```

它不会修改真实生产系统。

## Skill 形式

参赛 Skill 位于：

```text
.agents/skills/ai-delivery-doctor/
```

生成可提交压缩包：

```bash
python scripts/package_skill.py \
  .agents/skills/ai-delivery-doctor \
  --output dist/ai-delivery-doctor-skill.zip
```

Skill 的职责不是自己“宣布系统健康”，而是：

1. 理解用户真正要交付的结果；
2. 把结果拆成 3–8 个必要验证环节；
3. 生成/调整 `aidoc-v1` contract；
4. 调用确定性 Doctor；
5. 根据 evidence 找到第一处无法证明成立的链路；
6. 给出下一步验证，而不是脑补根因。

## 已实现能力

- file / env / executable / TCP / HTTP；
- OpenAI-compatible `/models` 检查；
- required / optional 语义；
- FIRST BLOCKER；
- JSON evidence；
- Markdown report；
- shareable 脱敏模式；
- before / after evidence compare；
- Agent Skill；
- Windows / macOS / Linux CI；
- Python 3.10–3.13 自动测试。

## 创新点

### 1. 不做“玄学生产就绪分”

一个关键模型凭据失败，不会因为另外九项通过就变成“90% ready”。

### 2. Agent 与确定性程序分工

```text
LLM / Agent
负责理解目标和设计验收链路
        ↓
Acceptance Contract
        ↓
AI Delivery Doctor
负责真实执行和留证
        ↓
Evidence
        ↓
Agent / 工程师解释下一步
```

### 3. 把 FDE 现场经验产品化

项目不是从抽象概念出发。

它与另一个真实开源项目 EdgeSafe Vision 形成关系：

```text
真实边缘 AI 交付问题
        ↓
抽象“证据优先”的方法
        ↓
AI Delivery Doctor
        ↓
未来复用到更多 AI 项目
```

## 当前边界

现在仍是早期版本。

它不声称：

- 能自动修复所有 AI 系统；
- TCP/HTTP 可达就代表业务结果成立；
- 能替代 RAG Eval、MCP 专项分析或完整 observability 平台；
- 能替代人工安全/合规判断。

当前重点是把“交付验证的底层语义”做稳，再逐步扩展 AI-native adapters。
