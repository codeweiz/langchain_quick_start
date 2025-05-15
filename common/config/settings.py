import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    全局配置管理，自动加载 .env 文件。
    """
    # LangSmith 配置
    LANGSMITH_TRACING: str = os.getenv("LANGSMITH_TRACING", "")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "")

    # DeepSeep API KEY
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")

    # GITHUB TOKEN
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")


settings = Settings()
