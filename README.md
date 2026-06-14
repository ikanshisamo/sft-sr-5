# 🎓 Sekolah Rakyat — SFT Pipeline & Mentor Chatbot Service (Matematika)

> End-to-end Supervised Fine-Tuning pipeline and deployment service for an AI Mentor chatbot for Sekolah Rakyat students, developed as part of the **AI Talent Factory (AITF) Program** by Kementerian Komunikasi dan Digital RI.

---

## 📌 Overview

This repository contains the complete SFT pipeline and deployment service for an **AI Mentor chatbot** specialized in **Mathematics** (Matematika), designed to guide students through learning materials using a **Socratic, empathetic approach** — without directly providing answers.

The system covers three learning contexts: reading material (materi), essay evaluation, and multiple-choice quiz review (pilihan ganda), with adaptive responses based on student emotion and comprehension level.

> **Note:** Datasets for Bahasa Indonesia (Bindo) and IPS are managed separately on HuggingFace. This repository focuses on the Mathematics pipeline.

## Video Simulasi Gradio Chatbot saat RunPod Aktif
(https://drive.google.com/file/d/1Iz59lH_5iuYe23twGJxk48Jdpz3Lw2Vt/view?usp=sharing)

---

## 🏗️ System Architecture

```
Dataset Generation (Matematika)
┌─────────────────────────────────────────────┐
│  Prompts (system_prompts_train + user)      │
│               │                             │
│               ▼                             │
│    OpenRouter API → Generate SFT Data       │
│               │                             │
│               ▼                             │
│    raw_data → clean_data → ready_to_train   │
└─────────────────────────────────────────────┘
               │
               ▼
        SFT Training
      (Qwen 3.5 9B via RunPod)
               │
               ▼
  ┌────────────────┐    ┌──────────────────────────┐
  │  gradio_app/   │    │  mentor-chatbot-service/  │
  │  (Testing UI)  │    │  FastAPI + LangGraph      │
  │  Flask + HTML  │    │  (Production Service)     │
  └────────────────┘    └──────────────────────────┘
```

---

## 📁 Repository Structure

```
sft-sr-5/
├── README.md
├── .gitignore
│
├── dataset-matematika/
│   ├── output/                          # Generated SFT datasets
│   │   ├── all_output_generate/         # All raw generation results
│   │   │   ├── clean_data/
│   │   │   ├── data_train/
│   │   │   ├── processed_data/
│   │   │   ├── raw_data/
│   │   │   ├── ready_to_train/
│   │   │   └── system_prompts_train/
│   │   ├── base_output_generate_batch_1/
│   │   │   └── materi_matematika.json
│   │   ├── essay_output_generate_batch_1/
│   │   │   └── essay_matematika.json
│   │   └── pilgan_output_generate_batch_1/
│   │       └── pilgan_matematika.json
│   │
│   └── prompts/
│       ├── komponen_system_formal/      # Formal system prompt components
│       │   ├── aturan_oot_bad/
│       │   ├── larangan_tambahan/
│       │   ├── struktur_respons/
│       │   ├── treatment_emosi/
│       │   └── treatment_kognitif/
│       ├── komponen_system_informal/    # Informal system prompt components
│       │   └── [same structure as formal]
│       ├── komponen_user_formal/
│       └── komponen_user_informal/
│
├── gradio_app/                          # Model testing interface
│   ├── app.py                           # Flask backend (serves UI + proxies to LLM)
│   ├── logic.py                         # LLM inference with streaming
│   └── templates/
│       └── index.html                   # Custom HTML/CSS chat UI
│
├── mentor-chatbot-service/              # Production microservice
│   ├── main.py                          # FastAPI app entry point
│   ├── requirements.txt
│   ├── .env.example                     # Environment variables template
│   ├── api/
│   │   ├── routes.py                    # /mentor/pesan + /mentor/evaluasi/stream
│   │   └── schemas.py                   # Pydantic request/response models
│   └── core/
│       ├── graph.py                     # LangGraph stateful conversation graph
│       ├── prompts.py                   # System prompts (Materi, Essay, PG)
│       └── config.py                    # Settings & environment config
│
├── output_matematika_mpe/               # MPE reference materials by curriculum
│   ├── K-13/
│   ├── KTSP/
│   └── Kurikulum Merdeka/
│
└── src/
    └── source_code/                     # Generation & training scripts
        ├── materi_mat_generate_sft.ipynb
        ├── essay_mtk_generate_sft.ipynb
        ├── pilgan_mtk_generate_sft.ipynb
        ├── merge_json.py
        ├── cleaning_user.py
        ├── sft_replace_content.ipynb
        ├── road_to_training.py
        ├── cek_saldo_token_api.ipynb
        └── test_gradio_4x.py
```

---

## 🛠️ Tech Stack

| Component | Tools |
|---|---|
| Language | Python 3.10+ |
| Dataset Generation | OpenRouter API, Custom prompt engineering |
| Fine-Tuning | Transformers, PEFT/LoRA, Qwen 3.5 9B |
| Backend Service | FastAPI, LangGraph, LangChain |
| Testing Interface | Flask, Gradio, HTML/CSS |
| API Testing | Postman |
| Infrastructure | RunPod (Komdigi) / Google Colab + Cloudflare Tunnel |
| Model Serving | vLLM (OpenAI-compatible endpoint) |

---

## 📊 Dataset Variations

The SFT dataset (Matematika) covers the following dimensions:

| Dimension | Variations |
|---|---|
| Context Type | Materi (reading), Essay, Pilihan Ganda (MCQ) |
| Student Emotion | Antusias, Bingung, Frustrasi, Bosan, Netral |
| Comprehension Level | Low, Mid, High |
| Edge Cases | Out-of-topic, Bad context, Minimal context |
| Curriculum | K-13, KTSP, Kurikulum Merdeka |

---

## 🚀 How to Run

### Testing Interface (Gradio App)

```bash
# 1. Install dependencies
pip install flask requests

# 2. Configure the LLM endpoint in logic.py
#    The endpoint URL depends on whether RunPod (Komdigi) is active.
#    There are two scenarios:

#    Scenario A — RunPod active (Komdigi provides Cloudflare Tunnel URL):
API_BASE = "https://xxxx-xxxx.trycloudflare.com/v1"   # changes every session

#    Scenario B — Local testing via Google Colab + Cloudflare Tunnel:
#    Run the Colab notebook to get a new tunnel URL, then paste it here.

# 3. Run the Flask app
python gradio_app/app.py

# 4. Open in browser
# http://127.0.0.1:5000/
```

> ⚠️ **Important:** The Cloudflare Tunnel URL changes every time RunPod is
> restarted. Always update `API_BASE` in `logic.py` before running.
> The model name is fixed: `MODEL_NAME = "ub-sr5"`

### Production Service (FastAPI + LangGraph)

```bash
# 1. Install dependencies
pip install -r mentor-chatbot-service/requirements.txt

# 2. Set environment variables
cp mentor-chatbot-service/.env.example mentor-chatbot-service/.env
# Edit .env:
#   OPENAI_API_KEY=sk-local-vllm-testing
#   (base_url is set in graph.py — update Cloudflare URL there)

# 3. Run
cd mentor-chatbot-service
uvicorn main:app --reload --port 8000

# 4. Test with Postman or curl
# POST http://localhost:8000/mentor/pesan
# POST http://localhost:8000/mentor/evaluasi/stream
```

---

## 🤖 API Endpoints

### `POST /mentor/pesan`
Synchronous chat for student-mentor interaction.

```json
{
  "siswa_id": "student_001",
  "sesi_id": "session_abc",
  "pesan": "Saya tidak mengerti soal ini",
  "emosi": "bingung",
  "jenis_konteks": "materi",
  "konten_konteks": "Teks bacaan materi...",
  "history": []
}
```

### `POST /mentor/evaluasi/stream`
Streaming SSE endpoint for quiz evaluation. Returns chunked response.

---

## ⚙️ Environment Variables

Copy `.env.example` and fill in your values:

```env
# mentor-chatbot-service/.env
OPENAI_API_KEY=sk-local-vllm-testing
REDIS_URL=redis://localhost:6379
```

The vLLM base URL (Cloudflare Tunnel) is configured directly in `core/graph.py`
and must be updated each time RunPod is restarted.

---

## 🔗 Related Resources

- 🤗 **Model**: [AITF-SR-05/UB-SR5-Qwen3.5-9B-Base-SFT-v2-3000](https://huggingface.co/AITF-SR-05)
- 🤗 **Datasets (Bindo & IPS)**: [AITF-SR-05 on HuggingFace](https://huggingface.co/AITF-SR-05)

---

## 👥 Team

Developed by **Tim 5 — AITF SR-05**, Kementerian Komunikasi dan Digital RI, 2026.

| Role | Contributor |
|---|---|
| SFT Dataset Engineering (Matematika) | Mutiara Dwi Artono, Dini Anjani P, Alif Eriksandi A |
| DPO Dataset | Coming Soon |
| Gradio Testing Interface | Dini Anjani P |
| FastAPI + LangGraph Service | Dini Anjani P |
| Collaboration | Tim Konten Belajar AITF & MVP Team|

---

## 📄 License

This project was developed under the AITF program. Model weights and full
datasets are managed through the AITF-SR-05 HuggingFace organization.
