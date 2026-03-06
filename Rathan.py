# ==========================================================
# 🤖 RATHAN AI ASSISTANT
# Multi-Tool Agent using LangGraph + Google GenAI
# ==========================================================

import os
from google import genai
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
import operator
# ==========================================================
# 🔐 SET YOUR API KEY
# ==========================================================
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"

# Create Gemini client
client = genai.Client()
# ==========================================================
# 🧮 TOOL 1 — CALCULATOR
# ==========================================================
@tool
def calculator(expression: str) -> str:
    """Evaluate math expressions like 2+3*4"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception:
        return "❌ Invalid math expression"

# ==========================================================
# 🌍 TOOL 2 — GEMINI SEARCH
# ==========================================================
@tool
def search(query: str) -> str:
    """Ask Gemini for information"""
    response = client.models.generate_content(
        model="models/gemini-1.5-flash",  # include models/
        contents=query
    )
    return response.text
# ==========================================================
# 🧠 AGENT STATE
# ==========================================================
class AgentState(TypedDict):
    messages: Annotated[Sequence, operator.add]
# ==========================================================
# 🤖 ASSISTANT NODE
# ==========================================================
def assistant(state: AgentState):
    user_input = state["messages"][-1].content.strip()

    # Smart routing logic
    if any(op in user_input for op in ["+", "-", "*", "/"]):
        result = calculator.invoke({"expression": user_input})
    else:
        result = search.invoke({"query": user_input})

    return {"messages": [AIMessage(content=result)]}
# ==========================================================
# 🔄 BUILD LANGGRAPH WORKFLOW
# ==========================================================
builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.set_entry_point("assistant")
builder.add_edge("assistant", END)

graph = builder.compile()
# ==========================================================
# 🚀 INTERACTIVE CHAT LOOP
# ==========================================================
print("Welcome to Rathan AI Assistant!")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Rathan AI Assistant: Excellent")
        break

    result = graph.invoke({
        "messages": [HumanMessage(content=user_input)]
    })

    print("Rathan AI Assistant:", result["messages"][-1].content)

