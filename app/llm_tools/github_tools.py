from langchain.tools import BaseTool
from typing import List
import httpx
import os

GITHUB_API_URL = "https://api.github.com"

def get_headers():
    token = os.getenv("GITHUB_TOKEN")  # 每次调用时动态获取
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    print(f"\nheaders: {headers}")
    return headers


class GetPRFilesTool(BaseTool):
    name: str = "get_pr_files"
    description: str = "输入格式：owner/repo|pr_number，例如 octocat/Hello-World|1，获取指定 GitHub PR 的变更文件列表"

    def _run(self, input: str) -> List[str]:
        repo, pr_number = input.split("|")
        url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/files"
        resp = httpx.get(url, headers=get_headers())
        resp.raise_for_status()
        return [f["filename"] for f in resp.json()]


class GetPRDiffTool(BaseTool):
    name: str = "get_pr_diff"
    description: str = "输入格式：owner/repo|pr_number，例如 octocat/Hello-World|1，获取指定 GitHub PR 的 diff/patch"

    def _run(self, input: str) -> str:
        repo, pr_number = input.split("|")
        url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}"
        resp = httpx.get(url, headers={**get_headers(), "Accept": "application/vnd.github.v3.diff"})
        resp.raise_for_status()
        return resp.text


class GetPRCommitsTool(BaseTool):
    name: str = "get_pr_commits"
    description: str = "输入格式：owner/repo|pr_number，例如 octocat/Hello-World|1，获取指定 GitHub PR 的所有 commit 信息"

    def _run(self, input: str) -> List[str]:
        repo, pr_number = input.split("|")
        url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/commits"
        resp = httpx.get(url, headers=get_headers())
        resp.raise_for_status()
        return [c["commit"]["message"] for c in resp.json()]


class PostPRCommentTool(BaseTool):
    name: str = "post_pr_comment"
    description: str = "输入格式：owner/repo|pr_number|comment，例如 octocat/Hello-World|1|你的评论内容，在指定 GitHub PR 下评论"

    def _run(self, input: str) -> str:
        try:
            repo, pr_number, comment = input.split("|", 2)
        except ValueError:
            return "输入格式错误，应为 owner/repo|pr_number|comment"
        url = f"{GITHUB_API_URL}/repos/{repo}/issues/{pr_number}/comments"
        resp = httpx.post(url, headers=get_headers(), json={"body": comment})
        resp.raise_for_status()
        return "评论成功"
