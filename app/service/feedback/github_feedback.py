import os
import httpx
from app.domain.models import PullRequest, ReviewResult
from app.domain.interfaces import FeedbackSender

GITHUB_API_URL = "https://api.github.com"

class GitHubFeedbackSender(FeedbackSender):
    """
    GitHub PR 评论反馈实现
    """
    def __init__(self, token: str = None):
        self.token = token or os.getenv("GITHUB_TOKEN")

    def _headers(self):
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def send_feedback(self, pr: PullRequest, review: ReviewResult) -> None:
        owner, repo = pr.repo.split("/")
        pr_number = pr.pr_id
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{pr_number}/comments"
        content = f"### 🤖 代码质量分析结果\n**总结：**\n{review.summary}\n\n**建议：**\n" + "\n".join(f"- {s}" for s in review.suggestions)
        resp = httpx.post(url, headers=self._headers(), json={"body": content})
        resp.raise_for_status() 