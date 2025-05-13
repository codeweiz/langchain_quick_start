
# 项目结构与顶层设计

## 目录结构

```text
src/
  app/                # 应用服务层，业务编排
    main.py           # FastAPI 入口
    service.py        # 业务流程编排
  domain/             # 领域层，核心接口和模型
    interfaces.py     # 领域接口（抽象类/协议）
    models.py         # 领域模型（实体/VO）
  infrastructure/     # 基础设施层，接口实现
    git/
      github.py       # GitHub 适配器
    llm/
      langchain_checker.py
    feedback/
      github_feedback.py
  config/
    settings.py       # 配置管理
  llm_checker/
    prompt_templates.py
services/
  tests/              # 单元测试
.env.example          # 环境变量示例
requirements.txt
pyproject.toml
README.md
```

## 各层职责

### app（应用服务层）
- 负责接收 Webhook 事件，调用领域服务编排业务流程。
- 不直接依赖具体实现，只依赖接口。

### domain（领域层）
- 定义核心业务接口（抽象类/协议）和领域模型。
- 只描述"做什么"，不关心"怎么做"。

### infrastructure（基础设施层）
- 实现 domain 层定义的接口，适配具体平台（如 GitHub、LangChain）。
- 通过依赖注入或工厂模式与 app 层解耦。

### config（配置管理）
- 统一管理环境变量、API Key、模型参数等。

### llm_checker（LLM 相关工具）
- 存放 prompt 模板、辅助工具等。

### services/tests（测试）
- 所有单元测试代码，覆盖率需大于 80%。

---

如需详细接口定义和实现方案，请参考 `src/domain/interfaces.py` 和 `src/domain/models.py`。