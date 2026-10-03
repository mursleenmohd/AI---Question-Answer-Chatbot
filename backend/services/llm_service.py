from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.schemas.chat import AIResponse
from collections.abc import Iterator

from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

structured_llm = llm.with_structured_output(AIResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful technical AI assistant.

            Rules:
            1. Explain concepts clearly.
            2. Assume the user is a beginner.
            3. Use simple examples.
            4. Avoid unnecessary complexity.
            5. If you are unsure, say so.
            """
        ),
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "{message}"
        ),
    ]
)

chain = prompt | structured_llm

def format_history(history: list):
    formatted_history = []
    for item in history:
        if item.role == "user":
            formatted_history.append(
                HumanMessage(content=item.content)
            )
        elif item.role == "assistant":
            formatted_history.append(
                AIMessage(content=item.content)
            )
    return formatted_history

def get_llm_response(message: str, history: list,) -> AIResponse:
    formatted_history = format_history(history)
    response = chain.invoke(
        {
            "history": formatted_history,
            "message": message,
        }
    )
    return response

def stream_llm_response(message: str, history: list,) -> Iterator[str]:
    formatted_history = format_history(history)
    streaming_chain = prompt | llm
    for chunk in streaming_chain.stream(
        {
            "history": formatted_history,
            "message": message,
        }
    ):
        if chunk.content:
            yield chunk.content