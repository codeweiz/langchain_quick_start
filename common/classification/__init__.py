from pydantic import BaseModel, Field


# 分类模型
class Classification(BaseModel):
    # 情感
    sentiment: str = Field(description="The Sentiment of the text")

    # 攻击性，按 1 到 10 标注
    aggressiveness: int = Field(description="How aggressive the text is on a scale from 1 to 10")

    # 语言
    language: str = Field(description="The language the text is written in")


# 更精细的分类模型
class FinerClassification(BaseModel):
    # 情感
    sentiment: str = Field(description="The Sentiment of the text", examples=["happy", "neutral", "sad"])

    # 攻击性，按 1 到 5 标注
    aggressiveness: int = Field(
        description="describes how aggressive the statement is, the higher the number the more aggressive",
        examples=[1, 2, 3, 4, 5])

    # 语言
    language: str = Field(description="The language the text is written in",
                          examples=["spanish", "english", "french", "german", "italian"])
