import os
from typing import List

import httpx

from app.domain.interfaces import DiffFetcher, CommitFetcher, GITHUB_API_URL
from app.domain.models import PullRequest, Diff, Commit


class GitHubDiffFetcher(DiffFetcher, CommitFetcher):
    """
    GitHub PR Diff/Commit 拉取实现
    """

    def __init__(self, token: str = None):
        self.token = token or os.getenv("GITHUB_TOKEN")

    def _headers(self, accept: str = "application/vnd.github.v3+json") -> dict:
        headers = {"Accept": accept}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def fetch_diff(self, pr: PullRequest) -> Diff:
        """
        获取 PR 的 diff/patch 和变更文件列表
        """
        owner, repo = pr.repo.split("/")
        pr_number = pr.pr_id

        # 获取 diff/patch
        diff_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
        resp = httpx.get(diff_url, headers=self._headers("application/vnd.github.v3.diff"))
        resp.raise_for_status()
        patch = resp.text

        # 获取变更文件列表
        files_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        resp_files = httpx.get(files_url, headers=self._headers())
        resp_files.raise_for_status()
        files = [f["filename"] for f in resp_files.json()]

        return Diff(files=files, patch=patch)

    def fetch_commits(self, pr: PullRequest) -> List[Commit]:
        """
        获取 PR 的所有 commit 信息
        """
        owner, repo = pr.repo.split("/")
        pr_number = pr.pr_id

        commits_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}/commits"
        resp = httpx.get(commits_url, headers=self._headers())
        resp.raise_for_status()
        commits = []
        for c in resp.json():
            commits.append(Commit(
                sha=c["sha"],
                message=c["commit"]["message"],
                author=c["commit"]["author"]["name"]
            ))
        return commits
