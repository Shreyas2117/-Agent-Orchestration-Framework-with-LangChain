from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def create_basic_agent():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY in .env file!")

    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # ✅ newer model
    google_api_key=api_key,
    temperature=0.7,
)


    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful AI assistant. Answer briefly."),
            ("human", "{user_input}"),
        ]
    )

    def run_agent(user_input: str) -> str:
        chain = prompt | llm
        res = chain.invoke({"user_input": user_input})
        return res.content

    return run_agent
