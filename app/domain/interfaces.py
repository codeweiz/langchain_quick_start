from abc import ABC, abstractmethod
from typing import List

from .models import PullRequest, Diff, Commit, ReviewResult

GITHUB_API_URL = "https://api.github.com"


class DiffFetcher(ABC):
    """
    拉取 PR/MR 变更内容的接口
    """

    @abstractmethod
    def fetch_diff(self, pr: PullRequest) -> Diff:
        """
        获取指定 PR/MR 的 diff/patch 内容
        :param pr: PullRequest 实例
        :return: Diff 实例
        """
        pass


class CommitFetcher(ABC):
    """
    拉取 PR/MR 相关 commit 的接口
    """

    @abstractmethod
    def fetch_commits(self, pr: PullRequest) -> List[Commit]:
        """
        获取指定 PR/MR 的所有 commit 信息
        :param pr: PullRequest 实例
        :return: Commit 列表
        """
        pass


class QualityChecker(ABC):
    """
    代码质量分析接口
    """

    @abstractmethod
    def check_quality(self, diff: Diff) -> ReviewResult:
        """
        分析 diff/patch 的代码质量
        :param diff: Diff 实例
        :return: ReviewResult 实例
        """
        pass


class FeedbackSender(ABC):
    """
    结果反馈接口
    """

    @abstractmethod
    def send_feedback(self, pr: PullRequest, review: ReviewResult) -> None:
        """
        将分析结果反馈到 PR/MR
        :param pr: PullRequest 实例
        :param review: ReviewResult 实例
        """
        pass
