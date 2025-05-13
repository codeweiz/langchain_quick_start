from typing import List, Optional

class PullRequest:
    """
    PR/MR 基本信息
    :param repo: 仓库名（格式 owner/repo）
    :param pr_id: PR/MR 编号
    :param author: 作者
    :param title: 标题
    :param description: 描述
    """
    def __init__(self, repo: str, pr_id: int, author: str, title: str, description: str):
        self.repo = repo
        self.pr_id = pr_id
        self.author = author
        self.title = title
        self.description = description

class Diff:
    """
    PR/MR 变更内容
    :param files: 变更文件列表
    :param patch: diff/patch 内容
    """
    def __init__(self, files: List[str], patch: str):
        self.files = files
        self.patch = patch

class Commit:
    """
    Commit 信息
    :param sha: commit 哈希
    :param message: commit message
    :param author: 作者
    """
    def __init__(self, sha: str, message: str, author: str):
        self.sha = sha
        self.message = message
        self.author = author

class ReviewResult:
    """
    代码质量分析结果
    :param summary: 总结
    :param suggestions: 建议列表
    """
    def __init__(self, summary: str, suggestions: Optional[List[str]] = None):
        self.summary = summary
        self.suggestions = suggestions or [] 