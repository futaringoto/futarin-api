from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from v2.cruds.message import get_histories

llm = ChatOpenAI()
prompt = PromptTemplate(
    input_variables=["conversation"],
    template="""
    以下はユーザーの過去に話した会話の記録です。

    {conversation}

    この会話に基づいて、ユーザに対して一つ質問を生成してください。
    友達とおしゃべりするような口調にしてください。
    """,
)

chain = RunnableSequence(prompt | llm)


async def generate_question(db: AsyncSession, user_id: int):
    conversation_history = await get_histories(db, user_id)
    response = chain.invoke({"conversation": conversation_history})
    return response
