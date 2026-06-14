import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage
from core.graph import workflow
from .schemas import ChatRequest, ChatResponse, ChatResponseData, EvaluasiRequest
from core.config import settings

router = APIRouter()

# Compile the workflow statelessly (no checkpointer)
app_graph = workflow.compile()

# Fungsi yang sudah diupdate untuk injeksi [Emosi: ...] dan [Konteks: ...]
def build_messages_from_history(history, new_message=None, emosi=None, konten_konteks=None):
    messages = []
    for msg in history:
        if msg.role.lower() in ["user", "siswa"]:
            messages.append(HumanMessage(content=msg.teks))
        else:
            messages.append(AIMessage(content=msg.teks))
            
    if new_message:
        # INJEKSI METADATA SFT: Hanya tambahkan tag Emosi & Konteks jika ini adalah pesan pertama (history kosong)
        if len(history) == 0 and emosi and konten_konteks:
            formatted_message = f"[Emosi: {emosi}]\n[Konteks:\n{konten_konteks}\n]\n{new_message}"
            messages.append(HumanMessage(content=formatted_message))
        else:
            messages.append(HumanMessage(content=new_message))
            
    return messages

@router.post("/mentor/pesan", response_model=ChatResponse)
async def mentor_pesan(req: ChatRequest):
    config = {} 
    
    # Panggil fungsi dengan tambahan parameter emosi dan konten_konteks
    messages = build_messages_from_history(
        req.history, 
        req.pesan, 
        req.emosi, 
        req.konten_konteks
    )
    
    # State input disesuaikan agar sesuai dengan parameter SFT yang baru
    state_input = {
        "messages": messages,
        "mode": "chat",
        "jenis_konteks": req.jenis_konteks
    }
    
    try:
        final_state = await app_graph.ainvoke(state_input, config=config)
        bot_msg = final_state["messages"][-1].content
        
        return ChatResponse(
            data=ChatResponseData(balasan=bot_msg, sesi_id=req.sesi_id),
            meta=None,
            error=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mentor/evaluasi/stream")
async def mentor_evaluasi_stream(req: EvaluasiRequest):
    config = {}
    
    # Parameter emosi dan konteks dikosongkan (None) karena evaluasi punya format berbeda
    messages = build_messages_from_history(req.history, "Tolong evaluasi hasil kuis saya.")
    
    state_input = {
        "messages": messages,
        "mode": "evaluasi",
        "atp": req.atp,
        "quiz_data": req.quiz_data or {}
    }

    async def event_generator():
        try:
            async for event in app_graph.astream_events(state_input, config, version="v2"):
                if event["event"] == "on_chat_model_stream":
                    chunk = event["data"]["chunk"].content
                    if chunk:
                        yield chunk
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(event_generator(), media_type="text/event-stream")