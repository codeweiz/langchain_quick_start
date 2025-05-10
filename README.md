# LangChain Quick Start 项目

## 目录结构

```
langchain_quick_start/
│
├── core/                  # 核心模块（llm、prompts、tools）
│   ├── llm/               # LLM底层封装（如 deepseek.py）
│   ├── prompts/           # Prompt模板（可扩展）
│   └── tools/             # 自定义工具（可扩展）
│
├── services/              # 业务服务层（如 memory、chatbot 等）
│
├── config/                # 配置（如 settings.py，自动加载 .env）
│
├── tests/                 # 测试用例
│
├── main.py                # 入口
├── pyproject.toml         # 依赖与元数据
├── .env                   # 环境变量（需手动创建）
└── README.md
```

## 环境搭建

1. 安装依赖：

推荐使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理：
```bash
uv pip install -r requirements.txt
# 或
uv pip install .
```

2. 配置环境变量

在项目根目录新建 `.env` 文件，内容如下：
```
DEEPSEEK_API_KEY=你的API密钥
```

## 运行说明

```bash
python main.py
```

## 测试说明

所有测试代码位于 `tests/` 目录，使用 pytest 运行：
```bash
pytest
```

## 主要接口示例

- 记忆对话示例：
```python
from services.memory import memory_chat
memory_chat("你好，我是 Bob")
memory_chat("我的名字叫什么？")
```

- deepseek-chat 模型获取示例：
```python
from core.llm.deepseek import get_deepseek_chat_model
model = get_deepseek_chat_model()
```

## 依赖

详见 `pyproject.toml`，主要依赖：
- langchain
- langchain-core
- langchain-deepseek
- langgraph
- python-dotenv
- pytest

## 说明

- 所有配置均通过环境变量或 .env 文件管理，严禁硬编码。
- 代码结构高度模块化，便于扩展和维护。
- 推荐使用 Black 格式化代码，遵循 PEP8。