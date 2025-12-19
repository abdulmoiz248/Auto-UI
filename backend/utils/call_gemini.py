import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7
)

def call_gemini(messages, systemPrompt="You are a helpful assistant."):
    chatMessages = [SystemMessage(content=systemPrompt)]

    for msg in messages:
        chatMessages.append(HumanMessage(content=msg["content"]))

    response = llm(chatMessages)
    return response.content
