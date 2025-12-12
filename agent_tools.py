# src/agent_tools.py

from dotenv import load_dotenv
import os
import json

# relative imports
from .tools.calculator import calculate
from .tools.weather import get_weather

# LLM import
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ----------------------------------------------------
# TOOL REGISTRY
# ----------------------------------------------------
TOOLS = {
    "calculator": {
        "func": calculate,
        "description": "Performs safe arithmetic calculations."
    },
    "weather": {
        "func": get_weather,
        "description": "Returns simulated weather for a location."
    }
}


def call_tool(tool_name: str, tool_input: str) -> str:
    """Call one of the registered tools."""
    if tool_name not in TOOLS:
        return f"[Tool error] Unknown tool: {tool_name}"
    try:
        func = TOOLS[tool_name]["func"]
        return func(tool_input)
    except Exception as e:
        return f"[Tool error] {e}"


# ----------------------------------------------------
# LLM (Gemini 2.5 Flash)
# ----------------------------------------------------
def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GOOGLE_API_KEY")
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.1
    )


# ----------------------------------------------------
# SYSTEM PROMPT — strict JSON only
# ----------------------------------------------------
SYSTEM_PROMPT = """
You are a tool-using agent.

*** RULES YOU MUST FOLLOW ***
1. You MUST ALWAYS respond using ONLY valid JSON.
2. NO markdown. NO text outside JSON. NO explanations.
3. Use EXACTLY one of the following formats:

To call a tool:
{{
  "action": "call_tool",
  "tool": "<tool_name>",
  "input": "<input>"
}}

To return final answer:
{{
  "action": "final_answer",
  "answer": "<your_answer>"
}}

TOOLS AVAILABLE:
- calculator → for arithmetic
- weather → for weather lookup

If user asks for math → use calculator.
If user asks weather → use weather.
Never invent tools.
Never output anything except valid JSON.
"""


# ----------------------------------------------------
# MAIN AGENT LOOP
# ----------------------------------------------------
def run_agent_with_tools(user_input: str, max_steps=5) -> str:
    """Main agent logic with tool-calling loop."""
    llm = get_llm()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    for step in range(max_steps):

        # Build prompt
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | llm
        response = chain.invoke({})

        # Raw text from model
        text = response.content.strip()

        # --------------------------
        # JSON enforcement
        # --------------------------
        try:
            data = json.loads(text)
        except Exception:
            # If model breaks rules, remind and retry
            messages.append({
                "role": "assistant",
                "content": "Your previous reply violated the JSON-only rule. Respond ONLY in valid JSON."
            })
            continue

        action = data.get("action")

        # --------------------------
        # FINAL ANSWER
        # --------------------------
        if action == "final_answer":
            return data.get("answer", "")

        # --------------------------
        # TOOL CALL
        # --------------------------
        if action == "call_tool":
            tool = data.get("tool")
            t_input = data.get("input", "")

            result = call_tool(tool, t_input)

            # Feed tool result back into context
            messages.append({
                "role": "assistant",
                "content": f"[TOOL_RESULT] {result}"
            })

            messages.append({
                "role": "user",
                "content": "Use the tool result to continue and output the final answer in JSON."
            })

            continue

        # Unknown action
        messages.append({
            "role": "assistant",
            "content": "Invalid action. Respond ONLY using the specified JSON format."
        })

    return "Agent exceeded max tool-steps."
