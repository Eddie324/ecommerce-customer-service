"""
LLM客户端
init_chat_model()
ChatOpenAI()

PEP8(coding标准 建议遵循)
1.基础包 from pathlib import Path
2.三方包 from langchain.chat_models import init_chat_model
3.自己定义的包
"""
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from EddieWu.config.settings import settings

llm_client: BaseChatModel = init_chat_model(
    model=settings.llm_model,
    model_provider="openai",
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
    temperature=0, # 控制生成文本的随机性,0-1之间,0表示确定性,1表示随机性
    timeout=120, # 超时时间,单位秒,默认60秒
)


if __name__ == "__main__":
    response = llm_client.invoke("你好,我现在心情不好")
    print(response.content)


