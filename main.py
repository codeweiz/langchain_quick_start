from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from app.domain.models import PullRequest
from app.llm_checker.langchain_checker import LangChainQualityChecker
from app.service.feedback.github_feedback import GitHubFeedbackSender
from app.service.git.github import GitHubDiffFetcher
from app.service.service import CodeReviewService
from dotenv import load_dotenv

app = FastAPI()

diff_fetcher = GitHubDiffFetcher()
quality_checker = LangChainQualityChecker()
review_service = CodeReviewService(diff_fetcher, quality_checker)
feedback_sender = GitHubFeedbackSender()
load_dotenv()

# 异步执行 review 和 feedback
def process_review_and_feedback(pr: PullRequest):
    diff, commits, review_result = review_service.review_pr(pr)
    feedback_sender.send_feedback(pr, review_result)
    # 可选：日志输出
    print(f"[Review] files: {diff.files}, commit_count: {len(commits)}")
    print(f"[Review] summary: {review_result.summary}")
    print(f"[Review] suggestions: {review_result.suggestions}")


@app.post("/webhook")
async def webhook_listener(request: Request, background_tasks: BackgroundTasks):
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
    # 后台异步执行耗时任务
    background_tasks.add_task(process_review_and_feedback, pr)
    return JSONResponse(content={"msg": "已接收，后台处理中"}, status_code=200)
