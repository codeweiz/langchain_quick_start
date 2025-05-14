# LangChain Quick Start 多模块最佳实践

## 目录结构（src 布局 + 多模块 monorepo）

```
langchain_quick_start/
│
├── core/
│   ├── pyproject.toml
│   ├── src/core/llm/...
│   ├── src/core/prompts/...
│   ├── src/core/tools/...
│   └── tests/test_deepseek.py
│
├── services/
│   ├── pyproject.toml
│   ├── src/services/memory.py
│   └── tests/test_memory.py
│
├── config/
│   ├── pyproject.toml
│   ├── src/config/settings.py
│   └── tests/test_settings.py
│
├── main.py
├── pyproject.toml         # 根 workspace 配置
├── .env
└── README.md
```

## 多模块开发与依赖管理

- 每个模块（core、services、config）都是独立 Python 包，采用 src 布局，互不污染。
- 根 pyproject.toml 只声明 workspace，不直接管理依赖。
- 依赖管理推荐用 [uv](https://github.com/astral-sh/uv)：

```bash
uv pip install -e ./app
uv pip install -e ./config
uv pip install -e ./core
uv pip install -e ./services
```

- 跨包 import 直接用包名（如 from core.llm.deepseek import ...），无需相对路径。
- 新增包时，建议统一采用 src 布局和 uv pip install -e 安装。

## 环境变量配置

在项目根目录新建 `.env` 文件，内容如下：
```
DEEPSEEK_API_KEY=你的API密钥
```

## 运行说明

```bash
uvicorn app.main:app --reload
```

## 测试说明

- 各模块下的 tests 目录存放该模块的测试用例。
- 进入对应模块目录，运行：
  ```bash
  pytest tests/
  ```
- 或在根目录用：
  ```bash
  pytest core/tests/
  pytest services/tests/
  pytest config/tests/
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

- 配置读取示例：
```python
from config.settings import settings
print(settings.DEEPSEEK_API_KEY)
```

- main.py 推荐写法：
```python
from services.memory import memory_chat
from core.llm.deepseek import get_deepseek_chat_model
from config.settings import settings

def main():
    print(f"DEEPSEEK_API_KEY: {settings.DEEPSEEK_API_KEY}")
    memory_chat("你好，我是 Bob")
    memory_chat("我的名字叫什么？")
    model = get_deepseek_chat_model()
    print("模型实例：", model)

if __name__ == "__main__":
    main()
```

## 说明

- 所有配置均通过 config/settings.py 管理，严禁硬编码。
- 代码结构高度模块化，便于扩展和维护。
- 推荐使用 Black 格式化代码，遵循 PEP8。