from typing import Union

from langchain.chat_models import init_chat_model
from langchain.chat_models.base import _ConfigurableModel
from langchain_core.language_models import BaseChatModel

from common.config.settings import settings




def get_deepseek_chat_model(model_name: str = "deepseek-chat") -> Union[BaseChatModel, _ConfigurableModel]:
    """
    获取 deepseek-chat 模型实例。
    :param model_name: 模型名称
    :return: 模型实例
    """
    return init_chat_model(model_name, model_provider="deepseek", api_key=settings.DEEPSEEK_API_KEY)
