from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.domain.models import PullRequest
from app.service.git.github import GitHubDiffFetcher
from app.llm_checker.langchain_checker import LangChainQualityChecker
from app.service.feedback.github_feedback import GitHubFeedbackSender
from app.service.service import CodeReviewService

app = FastAPI()

diff_fetcher = GitHubDiffFetcher()
quality_checker = LangChainQualityChecker()
review_service = CodeReviewService(diff_fetcher, quality_checker)
feedback_sender = GitHubFeedbackSender()


@app.post("/webhook")
async def webhook_listener(request: Request):
    """
    Webhook 事件监听入口，支持 GitHub PR/MR 相关事件。
    """
    event_body = await request.json()
    print("[Webhook] 收到事件:", event_body)

    # 这里只处理 GitHub PR 事件（opened/synchronize）
    action = event_body.get("action")
    pr_data = event_body.get("pull_request")
    repo_data = event_body.get("repository")
    if not pr_data or not repo_data:
        return JSONResponse(content={"msg": "非 PR 事件，忽略"}, status_code=200)

    pr = PullRequest(
        repo=f"{repo_data['owner']['login']}/{repo_data['name']}",
        pr_id=pr_data["number"],
        author=pr_data["user"]["login"],
        title=pr_data["title"],
        description=pr_data.get("body", "")
    )

    diff, commits, review_result = review_service.review_pr(pr)
    # 自动评论到 PR
    # feedback_sender.send_feedback(pr, review_result)
    # 这里只返回文件列表和 commit 数量，后续可扩展为 LLM 分析
    return JSONResponse(content={
        "files": diff.files,
        "commit_count": len(commits),
        "review_summary": review_result.summary,
        "review_suggestions": review_result.suggestions
    }, status_code=200)
