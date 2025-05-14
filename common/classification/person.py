from typing import Optional, List

from pydantic import BaseModel, Field


# 需要 description 提高 LLM 信息抽取的质量、不要强迫 LLM 编造信息，用 Optional 表示 LLM 在不知道的情况下输出 None

# 人
class Person(BaseModel):
    # 名称
    name: Optional[str] = Field(default=None, description="The name of the person")

    # 发色
    hair_color: Optional[str] = Field(default=None, description="The color of the person's hair if known")

    # 身高，单位米
    height_in_meters: Optional[str] = Field(default=None, description="The Person's height measured in meters if known")


# 一些人
class PersonList(BaseModel):
    persons: List[Person] = Field(default_factory=list)
