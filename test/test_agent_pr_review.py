import os
import pytest
from dotenv import load_dotenv

from app.llm_tools.agent_pr_review import review_pr_with_agent


@pytest.mark.skipif(
    not os.getenv("GITHUB_TOKEN"),
    reason="需要配置 GITHUB_TOKEN 环境变量"
)
def test_review_pr_with_agent():
    """
    验证 Agent 能自动审查 PR 并返回结果
    """

    load_dotenv()

    # 请替换为你有权限的测试仓库和 PR 编号
    repo = "codeweiz/langchain_quick_start"
    pr_number = 3
    result = review_pr_with_agent(repo, pr_number)
    print("Agent 审查结果：", result)
    assert isinstance(result, str)
    assert "建议" in result or "总结" in result
