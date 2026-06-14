import os
import json
from typing import Annotated, TypedDict, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig

from .prompts import SYSTEM_PROMPT_MATERI, SYSTEM_PROMPT_ESSAY, SYSTEM_PROMPT_PG

# Fallback jika SYSTEM_PROMPT_EVALUASI terhapus saat modifikasi file prompts.py
try:
    from .prompts import SYSTEM_PROMPT_EVALUASI
except ImportError:
    SYSTEM_PROMPT_EVALUASI = "Kamu adalah mentor chatbot virtual. Tolong evaluasi hasil kuis berikut:\nATP: {atp}\nData: {quiz_data}"

from .config import settings

# Menambahkan total=False agar parameter opsional seperti quiz_data tidak memicu error saat mode chat biasa
class GraphState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    mode: str
    jenis_konteks: str
    atp: str
    quiz_data: Dict[str, Any]

llm = ChatOpenAI(
    model="ub-sr5",
    api_key=settings.OPENAI_API_KEY, # Otomatis membaca "sk-local-vllm-testing" dari .env
    base_url="https://refine-processed-instant-defined.trycloudflare.com/v1", # Diisi URL Cloudflare aktif dari Colab
    streaming=True
)

async def chatbot_node(state: GraphState, config: RunnableConfig):
    mode = state.get("mode", "chat")
    messages = state["messages"]
    jenis_konteks = state.get("jenis_konteks", "materi")
    
    if mode == "chat":
        # Gunakan prompt SFT sesuai jenis konteks dari dataset
        if jenis_konteks == "essay":
            sys_prompt = SYSTEM_PROMPT_ESSAY
        elif jenis_konteks == "pg":
            sys_prompt = SYSTEM_PROMPT_PG
        else:
            sys_prompt = SYSTEM_PROMPT_MATERI
            
    elif mode == "evaluasi":
        # Mode bawaan dari template untuk stream evaluasi kuis
        quiz_data_str = json.dumps(state.get("quiz_data", {}), indent=2)
        sys_prompt = SYSTEM_PROMPT_EVALUASI.format(
            atp=state.get("atp", ""),
            quiz_data=quiz_data_str
        )
    else:
        sys_prompt = "Kamu adalah mentor chatbot virtual."

    # Injeksi system prompt SFT tanpa variabel .format() karena tag SFT diproses di user prompt pertama
    all_messages = [SystemMessage(content=sys_prompt)] + messages
    response = await llm.ainvoke(all_messages, config)
    
    return {"messages": [response]}

workflow = StateGraph(GraphState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)