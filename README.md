# LangChain PR 代码质量自动审查 MVP

## 项目简介

本项目实现了一个自动化的 PR 代码质量审查 MVP：
- 监听 GitHub PR Webhook 事件
- 自动拉取 PR 的 diff、commit 信息
- 基于 LangChain + Deepseek LLM 进行代码质量分析
- 自动将分析结果评论到 PR
- 支持异步后台处理，主线程快速响应

---

## 目录结构

```
langchain_quick_start/
├── app/
│   ├── main.py                  # FastAPI Webhook 入口
│   ├── domain/                  # 领域模型与接口
│   ├── service/                 # 主流程、GitHub、反馈等实现
│   └── llm_checker/             # LLM 质量分析与 prompt
├── test/                        # 测试代码
├── common/                      # 通用工具/配置
├── services/                    # 其他微服务
├── .env                         # 环境变量
├── pyproject.toml               # 依赖管理
├── README.md
```

---

## 依赖安装

推荐使用 [uv](https://github.com/astral-sh/uv)：

```bash
uv pip install
```

---

## 环境变量配置

在项目根目录新建 `.env` 文件，内容示例：
```
GITHUB_TOKEN=你的github token
DEEPSEEK_API_KEY=你的deepseek api key
```

---

## 运行方式

```bash
uvicorn main:app --reload
```

---

## 主要接口说明

- Webhook 入口：`POST /webhook`
  - 监听 GitHub PR 事件（opened/synchronize）
  - 自动拉取 diff、commit，LLM 分析并评论到 PR
  - 主线程快速返回 `{"msg": "已接收，后台处理中"}`

---

## 设计亮点

- 领域驱动分层，接口解耦，易扩展
- LLM 代码质量分析可插拔，支持多模型
- 所有敏感信息通过环境变量管理，安全合规
- 支持 LangChain Tool 封装 GitHub 能力，便于智能体扩展

---

## TODO
- [ ] 支持更多平台（如 GitLab）
- [ ] LLM 质量分析异步化/多模型切换
- [ ] LangChain Tool/Agent 智能体集成
- [ ] 单元测试与覆盖率提升