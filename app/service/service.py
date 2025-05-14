from typing import Tuple, List

from app.domain.models import PullRequest, Diff, Commit, ReviewResult
from app.service.git.github import GitHubDiffFetcher
from app.llm_checker.langchain_checker import LangChainQualityChecker


class CodeReviewService:
    """
    代码审查主流程服务
    """

    def __init__(self, diff_fetcher: GitHubDiffFetcher, quality_checker: LangChainQualityChecker):
        self.diff_fetcher = diff_fetcher
        self.quality_checker = quality_checker

    def review_pr(self, pr: PullRequest) -> Tuple[Diff, List[Commit], ReviewResult]:
        """
        拉取 PR 的 diff、commit 信息，并用 LLM 分析代码质量
        :param pr: PullRequest 实例
        :return: (Diff, Commit 列表, ReviewResult)
        """
        diff = self.diff_fetcher.fetch_diff(pr)
        print(f"\ndiff:{diff.to_dict()}")
        commits = self.diff_fetcher.fetch_commits(pr)
        print(f"\ncommits:{[c.to_dict() for c in commits]}")
        review_result = self.quality_checker.check_quality(diff)
        return diff, commits, review_result
