from app.domain.models import Diff, ReviewResult
from app.domain.interfaces import QualityChecker
from app.llm_checker.prompt_templates import CODE_REVIEW_PROMPT
from common.llm.deepseek import get_deepseek_chat_model
from langchain_core.messages import HumanMessage

class LangChainQualityChecker(QualityChecker):
    """
    基于 LangChain 的 LLM 代码质量分析实现，支持 deepseek-chat
    """
    def __init__(self, llm=None):
        self.llm = llm or get_deepseek_chat_model()

    def check_quality(self, diff: Diff) -> ReviewResult:
        prompt = CODE_REVIEW_PROMPT.format(diff=diff.patch)
        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        # 简单分割 summary 和建议
        lines = response.content.splitlines()
        summary = lines[0] if lines else ""
        suggestions = [l for l in lines[1:] if l.strip()]
        return ReviewResult(summary=summary, suggestions=suggestions) 