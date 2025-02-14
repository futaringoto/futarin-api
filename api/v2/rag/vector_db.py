from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence


llm = ChatOpenAI()
prompt = PromptTemplate(
    input_variables=["conversation"],
    template="""
    以下はユーザーの過去に話した会話の記録です。

    {conversation}

    この会話に基づいて、ユーザに対して一つ質問を生成してください。
    """
)

chain = RunnableSequence(prompt | llm)

def generate_question(raspi_id: int):
    with open(f"./v2/rag/text/{raspi_id}_prompt.txt") as f:
        conversation_history = f.read()
    response = chain.invoke({"conversation": conversation_history})
    return response