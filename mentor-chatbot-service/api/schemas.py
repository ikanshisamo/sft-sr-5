from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class MessageHistory(BaseModel):
    role: str
    teks: str

class ChatRequest(BaseModel):
    siswa_id: str
    sesi_id: str
    pesan: str
    
    # Variabel baru yang disesuaikan dengan kebutuhan dataset SFT (SMAN 22)
    emosi: Optional[str] = "netral" 
    jenis_konteks: str = "materi"          # Pilihan: "materi", "essay", atau "pg"
    konten_konteks: Optional[str] = None   # Teks bacaan materi / soal essay / soal pg
    
    # Variabel bawaan template (dijadikan opsional agar tidak memicu error)
    mapel_id: Optional[str] = None
    elemen_id: Optional[str] = None
    elemen_label: Optional[str] = None
    materi: Optional[str] = None
    materi_id: Optional[str] = None
    atp: Optional[str] = None
    level: Optional[str] = None
    
    history: List[MessageHistory] = Field(default_factory=list)

class EvaluasiRequest(BaseModel):
    siswa_id: str
    sesi_id: str
    hasil_quiz_id: str
    mapel_id: str
    elemen_id: str
    elemen_label: str
    materi: str
    materi_id: str
    level: str
    atp: str
    quiz_data: Optional[Dict[str, Any]] = None
    history: List[MessageHistory] = Field(default_factory=list)

class ChatResponseData(BaseModel):
    balasan: str
    sesi_id: str

class ChatResponse(BaseModel):
    data: ChatResponseData
    meta: Optional[Any] = None
    error: Optional[Any] = None