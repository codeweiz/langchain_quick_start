from langchain.agents import initialize_agent, AgentType
from app.llm_tools.github_tools import (
    GetPRFilesTool, GetPRDiffTool, GetPRCommitsTool, PostPRCommentTool
)
from common.llm.deepseek import get_deepseek_chat_model

# 1. 实例化 LLM
llm = get_deepseek_chat_model()

# 2. 注册 Tool
tools = [
    GetPRFilesTool(),
    GetPRDiffTool(),
    GetPRCommitsTool(),
    PostPRCommentTool(),
]

# 3. 初始化 Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

def review_pr_with_agent(repo: str, pr_number: int) -> str:
    """
    让 Agent 自动审查 PR，分析代码质量并评论建议
    :param repo: 仓库名（如 owner/repo）
    :param pr_number: PR 编号
    :return: Agent 执行结果
    """
    tool_input = f"{repo}|{pr_number}"
    prompt = (
        f"请帮我自动审查 GitHub 仓库 {repo} 的 PR #{pr_number}，"
        f"你可以用 get_pr_files、get_pr_diff、get_pr_commits 工具，"
        f"输入格式为 owner/repo|pr_number，例如 {tool_input}。"
        f"分析代码质量、风格、命名、注释、潜在问题，并将建议用 post_pr_comment 工具评论到 PR。"
        f"请一步步思考。"
    )
    return agent.run(prompt)
