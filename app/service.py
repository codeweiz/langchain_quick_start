import json

from app.domain.models import PullRequest, Diff, Commit
from app.infrastructure.git.github import GitHubDiffFetcher
from typing import Tuple, List


class CodeReviewService:
    """
    代码审查主流程服务
    """

    def __init__(self, diff_fetcher: GitHubDiffFetcher):
        self.diff_fetcher = diff_fetcher

    def review_pr(self, pr: PullRequest) -> Tuple[Diff, List[Commit]]:
        """
        拉取 PR 的 diff 和 commit 信息
        :param pr: PullRequest 实例
        :return: (Diff, Commit 列表)
        """
        diff = self.diff_fetcher.fetch_diff(pr)
        print(f"\ndiff:{diff.to_dict()}")
        commits = self.diff_fetcher.fetch_commits(pr)
        print(f"\ncommits:{[c.to_dict() for c in commits]}")
        return diff, commits
