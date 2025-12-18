import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.environ.get("GROQ_API_KEY")
)

def call_ai(messages, systemPrompt="You are a helpful assistant."):
    formattedMessages = [SystemMessage(content=systemPrompt)]

    for msg in messages:
        formattedMessages.append(
            HumanMessage(content=msg["content"])
        )

    response = llm.invoke(formattedMessages)
    return response.content
