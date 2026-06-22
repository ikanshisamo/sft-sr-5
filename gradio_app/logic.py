import requests
import json
import os
import gradio as gr

# ── KONFIGURASI ──────────────────────────────────────────────
API_BASE    = "https://economics-powder-transition-spent.trycloudflare.com/v1/chat/completions"
API_KEY     = "not-needed"
MODEL_NAME  = "ub-sr-all"
MAX_TOKENS  = 8192
TEMPERATURE = 0.7
STOP_TOKENS = ["user", "\nuser", "<|im_end|>", "User:"]

# Matikan reasoning/think mode Qwen. Server abaikan field ini jika tidak didukung.
ENABLE_THINKING = False

# Label emosi dari dropdown (simulasi pengganti hasil face emotion recognition)
# Value harus persis sama dengan tag [Emosi: ...] di dataset SFT, huruf kecil semua.
EMOTION_LABELS = {
    "antusias": "antusias",
    "bingung": "bingung",
    "netral": "tidak terdeteksi",
    "bosan": "bosan",
    "frustrasi": "frustrasi",
}

def apply_emotion_tag(user_message, emotion_key):
    label = EMOTION_LABELS.get(emotion_key)
    if not label:
        return user_message
    return f"[Emosi: {label}]\n{user_message}"

# ── SYSTEM PROMPTS DARI FOLDER ───────────────────────────────
PROMPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")

MODE_TO_FILE = {
    "Materi": "materi.md",
    "Essay": "essay.md",
    "Pilihan Ganda": "pilgan.md",
}

def load_system_prompt(mode):
    filename = MODE_TO_FILE.get(mode)
    if not filename:
        return ""
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def load_all_system_prompts():
    return {mode: load_system_prompt(mode) for mode in MODE_TO_FILE}

SYSTEM_PROMPTS = load_all_system_prompts()

CHOICE_TO_MODE = {
    "Materi": "Materi",
    "Essay": "Essay",
    "Pilihan Ganda": "Pilihan Ganda",
}
INITIAL_CHOICE = "Materi"

# ── FUNGSI ───────────────────────────────────────────────────
def on_mode_change(mode):
    return SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS.get(CHOICE_TO_MODE.get(mode, mode))), []

def chat(user_message, history, system_prompt, temperature, max_tokens, emotion=None):
    if not user_message.strip():
        return "", history

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": ""})

    tagged_message = apply_emotion_tag(user_message, emotion)

    messages_payload = [{"role": "system", "content": system_prompt}]
    for turn in history[:-2]:
        messages_payload.append(turn)
    messages_payload.append({"role": "user", "content": tagged_message})

    payload = {
        "model":             MODEL_NAME,
        "messages":          messages_payload,
        "max_tokens":        int(max_tokens),
        "temperature":       float(temperature),
        "stream":            True,
        "stop":              STOP_TOKENS,      # <--- Tambahkan ini
        "frequency_penalty": 1.2,              # <--- Tambahkan ini
        "presence_penalty":  1.2,              # <--- Tambahkan ini
        "chat_template_kwargs": {"enable_thinking": ENABLE_THINKING}
    }
    
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    try:
        with requests.post(
            f"{API_BASE}",
            headers=headers,
            json=payload,
            stream=True,
            timeout=120,
        ) as resp:
            resp.raise_for_status()
            collected = ""
            for raw_line in resp.iter_lines():
                if not raw_line: continue
                line = raw_line.decode("utf-8")
                if line.startswith("data: "): line = line[6:]
                if line.strip() == "[DONE]": break
                
                try:
                    chunk = json.loads(line)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    collected += delta
                    history[-1]["content"] = collected
                    yield "", history
                except (json.JSONDecodeError, KeyError):
                    continue

    except requests.exceptions.ConnectionError:
        error_msg = "Koneksi gagal. Pastikan endpoint Cloudflare aktif."
        history[-1]["content"] = error_msg
        yield "", history
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history[-1]["content"] = error_msg
        yield "", history

def clear_history():
    return "", []

def toggle_edit(is_editing: bool):
    new_state = not is_editing
    return gr.update(interactive=new_state), new_state