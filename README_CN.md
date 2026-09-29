# AI Delivery Doctor

> **面向 AI 应用交付的“证据优先”验收工具：在客户发现问题之前，先找到第一处无法被证明成立的链路。**

AI Delivery Doctor（`aidoc`）关注的不是“再做一个 Agent 框架”，而是 AI 从 Demo 到真实交付之间最容易失控的部分。

核心思想：

```text
定义交付链路
   ↓
执行有边界的确定性检查
   ↓
保存 PASS / WARN / FAIL 证据
   ↓
找到第一个无法证明成立的必要环节
   ↓
再决定下一步验证或修复
```

它不使用模糊的“生产就绪 87 分”来掩盖关键阻塞项。

## 三分钟体验

```bash
git clone https://github.com/Yazhou-Li/ai-delivery-doctor.git
cd ai-delivery-doctor

python -m pip install -e .
python -m unittest discover -s tests -v

aidoc doctor --config examples/acceptance.example.json
aidoc doctor --config examples/broken.example.json
```

第二个例子会故意产生一个 required FAIL，并明确给出 `FIRST BLOCKER`。

## 为什么需要它

很多 AI 项目真正失败的地方不是模型能力本身，而是：

- 运行环境和依赖没有对齐；
- 模型/API 在开发机可用，到交付机器不可用；
- MCP/Tool/RAG 某个中间环节没真正工作；
- 上游返回 200，就被误认为整条业务链已经打通；
- 项目有日志，却没有明确“交付前必须证明什么”的验收契约。

AI Delivery Doctor 希望把这些经验沉淀成可复用、可自动化、可被 Agent 调用的基础设施。

## 当前支持

- 文件可读性检查；
- 环境变量存在性检查（永不输出值）；
- 可执行文件检查；
- TCP 可达性检查；
- HTTP 状态检查；
- JSON evidence；
- Markdown 报告；
- `--shareable` 脱敏证据模式；
- Agent Skill；
- CI 与自动测试。

更完整说明见英文 [README](README.md) 与 [Architecture](docs/ARCHITECTURE.md)。
