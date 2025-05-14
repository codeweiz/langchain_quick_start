import pytest
from services.memory import memory_chat

def test_memory_chat_basic():
    """
    测试 memory_chat 的基本功能。
    """
    # 这里只测试调用是否报错，实际输出需人工检查
    try:
        memory_chat("你好，我是测试用户")
    except Exception as e:
        pytest.fail(f"memory_chat 执行异常: {e}") 