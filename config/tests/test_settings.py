from config.settings import settings

def test_settings_env():
    # 检查 settings 能否正确加载环境变量
    assert hasattr(settings, "DEEPSEEK_API_KEY")
    # 允许为空，但类型必须为 str
    assert isinstance(settings.DEEPSEEK_API_KEY, str) 