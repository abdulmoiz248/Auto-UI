import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7
)

def call_gemini(messages, systemPrompt="You are a helpful assistant.", system_prompt=None):
    # Support both systemPrompt and system_prompt parameter names
    prompt = system_prompt if system_prompt is not None else systemPrompt
    chatMessages = [SystemMessage(content=prompt)]

    for msg in messages:
        chatMessages.append(HumanMessage(content=msg["content"]))

    response = llm.invoke(chatMessages)
    return response.content
