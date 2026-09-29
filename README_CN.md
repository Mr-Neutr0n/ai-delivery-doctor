# AI Delivery Doctor

[![CI](https://github.com/Yazhou-Li/ai-delivery-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/Yazhou-Li/ai-delivery-doctor/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/Yazhou-Li/ai-delivery-doctor)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](pyproject.toml)
[![Stars](https://img.shields.io/github/stars/Yazhou-Li/ai-delivery-doctor?style=social)](https://github.com/Yazhou-Li/ai-delivery-doctor/stargazers)
[![Issues](https://img.shields.io/github/issues/Yazhou-Li/ai-delivery-doctor)](https://github.com/Yazhou-Li/ai-delivery-doctor/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

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
- OpenAI-compatible `/models` 与指定模型存在性检查；
- JSON evidence；
- Markdown 报告；
- `--shareable` 脱敏证据模式；
- before / after evidence 对比；
- required regression 的非零退出码，可用于 CI；
- Agent Skill；
- Skill 自动校验与确定性打包；
- Windows / macOS / Linux 跨平台 CI；
- Python 3.10–3.13 自动测试。

## 一条命令看懂项目

```bash
python scripts/showcase.py
```

它会在纯合成、无网络、无账号的临时环境中演示：

```text
required FAIL
    ↓
FIRST BLOCKER
    ↓
补齐可观察的验收条件
    ↓
PASS
    ↓
before / after evidence compare
    ↓
IMPROVED
```

## Agent Skill

参赛/可移植 Skill 位于：

```text
.agents/skills/ai-delivery-doctor/
```

验证并打包：

```bash
python scripts/validate_skill.py .agents/skills/ai-delivery-doctor
python scripts/package_skill.py \
  .agents/skills/ai-delivery-doctor \
  --output dist/ai-delivery-doctor-skill.zip
```

## 文档入口

- [Getting Started](docs/GETTING_STARTED.md)
- [Contract Reference](docs/CONTRACT_REFERENCE.md)
- [Technical Philosophy](docs/PHILOSOPHY.md)
- [三分钟 Showcase](docs/SHOWCASE_CN.md)
- [黑客松展示说明](docs/HACKATHON_CN.md)
- [路演脚本](docs/DEMO_SCRIPT_CN.md)
- [EdgeSafe Vision 案例桥接](docs/CASE_STUDY_EDGESAFE.md)
- [Roadmap](ROADMAP.md)

更完整说明见英文 [README](README.md) 与 [Architecture](docs/ARCHITECTURE.md)。
