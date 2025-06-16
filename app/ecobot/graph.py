# graph.py
from langgraph.graph import StateGraph, START, END
from app.ecobot.memory import get_memory_store, get_checkpointer
from langchain_openai import ChatOpenAI
from app.ecobot.prompt import react_prompt
from app.ecobot.state import BotState
from contextlib import ExitStack
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
#model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

import json

def call_model(state, config, store):
    user_input = state["messages"][-1]["content"]
    prompt = react_prompt.format_prompt(input=user_input).to_messages()
    resp = model.invoke(prompt)
    content = resp.content
    try:
        final_answer = json.loads(content.replace("Final Answer:", "").strip())
        msg = final_answer.get("msg", "")
        accion = final_answer.get("accion", "")
        data = final_answer.get("data", {})

        state["last_accion"] = accion

        state["messages"].append({"role": "assistant", "content": content})
        return state
    except Exception as e:
        state["messages"].append({"role": "assistant", "content": content})
        return state


def write_memory(state, config, store):
    uid = config["configurable"]["user_id"]
    store.put(("memory", uid), "user_data", {
        "userid": uid,
        "last_message": state["messages"][-1]["content"]
    })
    return state

builder = StateGraph(BotState)
builder.add_node("call_model", call_model)
builder.add_node("write_memory", write_memory)
builder.add_edge(START, "call_model")
builder.add_edge("call_model", "write_memory")
builder.add_edge("write_memory", END)

with ExitStack() as stack:
    store = stack.enter_context(get_memory_store())
    chk = stack.enter_context(get_checkpointer())
    store.setup()
    chk.setup()
    graph = builder.compile(store=store, checkpointer=chk)
