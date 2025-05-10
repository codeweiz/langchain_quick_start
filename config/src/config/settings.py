import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    全局配置管理，自动加载 .env 文件。
    """
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")

settings = Settings() 