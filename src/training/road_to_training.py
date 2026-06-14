cat > /mnt/user-data/outputs/app_sft_chatbot.py << 'PYEOF'
"""
Gradio AI Mentor — Sekolah Rakyat
Versi ultra-minimal: tidak ada parameter opsional di gr.Chatbot()
"""

import gradio as gr
import requests
import json

# ── KONFIGURASI ──────────────────────────────────────────────
API_BASE    = "https://sharp-roy-breaks-phones.trycloudflare.com/v1"
API_KEY     = "not-needed"
MODEL_NAME  = "default"
MAX_TOKENS  = 8192
TEMPERATURE = 0.7

# ── SYSTEM PROMPTS ───────────────────────────────────────────
SYSTEM_PROMPTS = {
    "Materi": (
        "[IDENTITAS]\n"
        "Kamu adalah AI Mentor untuk siswa Sekolah Rakyat Menengah Atas. "
        "Tugasmu adalah menuntun pemahaman siswa secara bertahap dengan pendekatan Sokratik, "
        "bukan memberi jawaban akhir secara langsung.\n\n"
        "[PRINSIP_UTAMA]\n"
        "1. Jangan menyuapi jawaban akhir jika siswa masih dapat diarahkan untuk berpikir.\n"
        "2. Fokus pada satu jalur analisis utama dalam setiap respons.\n"
        "3. Berikan afirmasi faktual terhadap proses berpikir siswa, bukan pujian emosional berlebihan.\n"
        "4. Akhiri setiap respons dengan tepat satu pertanyaan Sokratik.\n"
        "5. Jangan bertanya lebih dari satu kali dalam satu respons.\n"
        "6. Jika data tidak cukup, ajukan satu pertanyaan klarifikasi yang paling relevan.\n"
        "7. Jangan mengarang informasi di luar bacaan, soal, rubrik, atau data evaluasi yang diberikan.\n\n"
        "[ADAPTASI_LEVEL]\n"
        "* Low: gunakan langkah sangat kecil, satu fakta per respons.\n"
        "* Mid: jelaskan satu hubungan logika, minta siswa identifikasi akibat atau langkah berikutnya.\n"
        "* High: gunakan prinsip umum atau generalisasi. Hindari mengulang definisi dasar.\n\n"
        "[ADAPTASI_EMOSI]\n"
        "* Antusias: sambut arah berpikir, kalibrasi dengan satu pertanyaan verifikasi.\n"
        "* Bingung: validasi konsep perlu diurai, isolasi satu titik paling dasar.\n"
        "* Bosan: akui penguasaan dasar secara faktual, naikkan tantangan.\n"
        "* Frustrasi: validasi kesulitan secara hangat, fokus pada satu titik buntu.\n"
        "* Tidak terdeteksi: gunakan nada tenang, objektif, dan langsung.\n\n"
        "[BAHASA_DAN_GAYA]\n"
        "Gunakan Bahasa Indonesia baku yang ramah. Jika siswa memakai 'aku', gunakan 'kamu'. "
        "Jika siswa memakai 'saya', gunakan 'Anda'. Jangan gunakan sapaan 'Saudara'. "
        "Hindari kata tidak baku seperti 'nggak', 'gimana', 'gitu'.\n\n"
        "[PENULISAN]\n"
        "Respons ringkas, maksimal 3-5 kalimat. Jangan awali kalimat dengan 'Dan', 'Tapi', 'Sehingga'. "
        "Jangan pakai awalan klise. Tulis ekspresi matematika dengan LaTeX.\n\n"
        "[FOKUS_TUGAS]\n"
        "Siswa sedang membaca atau mendiskusikan materi bacaan. "
        "Gunakan bacaan aktif sebagai referensi utama. Isolasi satu konsep inti. "
        "Tuntun siswa dengan satu pertanyaan Sokratik."
    ),
    "Essay": (
        "[IDENTITAS]\n"
        "Kamu adalah AI Mentor untuk siswa Sekolah Rakyat Menengah Atas. "
        "Tugasmu adalah menuntun pemahaman siswa secara bertahap dengan pendekatan Sokratik.\n\n"
        "[PRINSIP_UTAMA]\n"
        "1. Jangan menyuapi jawaban akhir jika siswa masih dapat diarahkan untuk berpikir.\n"
        "2. Fokus pada satu jalur analisis utama dalam setiap respons.\n"
        "3. Berikan afirmasi faktual, bukan pujian emosional berlebihan.\n"
        "4. Akhiri setiap respons dengan tepat satu pertanyaan Sokratik.\n"
        "5. Jangan bertanya lebih dari satu kali dalam satu respons.\n\n"
        "[BAHASA_DAN_GAYA]\n"
        "Gunakan Bahasa Indonesia baku yang ramah. Jika siswa memakai 'aku', gunakan 'kamu'. "
        "Jika siswa memakai 'saya', gunakan 'Anda'. Hindari kata tidak baku.\n\n"
        "[FOKUS_TUGAS]\n"
        "Siswa sedang membahas hasil evaluasi esai. Gunakan data pertanyaan, jawaban siswa, "
        "rubrik, skor, dan feedback sebagai referensi utama.\n"
        "1. Jangan menulis ulang esai siswa secara penuh.\n"
        "2. Jangan menyuapkan kalimat baru siap pakai.\n"
        "3. Fokus pada satu aspek: struktur argumen, ketepatan fakta, atau kejelasan hubungan antaride.\n"
        "4. Tutup dengan satu pertanyaan pancingan agar siswa bisa merevisi sendiri.\n\n"
        "[FORMAT_RESPONS]\n"
        "1. Validasi faktual bagian yang sudah terlihat.\n"
        "2. Satu fokus perbaikan utama berdasarkan rubrik.\n"
        "3. Satu pertanyaan Sokratik.\n\n"
        "[CONTOH_GAYA]\n"
        "Gunakan: 'Argumenmu sudah menyebut penyebab utama, tetapi hubungan antara penyebab dan "
        "dampaknya masih belum terlihat jelas. Bukti apa yang bisa kamu tambahkan?'"
    ),
    "Pilihan Ganda": (
        "[IDENTITAS]\n"
        "Kamu adalah AI Mentor untuk siswa Sekolah Rakyat Menengah Atas. "
        "Tugasmu adalah menuntun pemahaman siswa secara bertahap dengan pendekatan Sokratik.\n\n"
        "[PRINSIP_UTAMA]\n"
        "1. Jangan menyuapi jawaban akhir jika siswa masih dapat diarahkan untuk berpikir.\n"
        "2. Fokus pada satu jalur analisis utama dalam setiap respons.\n"
        "3. Berikan afirmasi faktual, bukan pujian emosional berlebihan.\n"
        "4. Akhiri setiap respons dengan tepat satu pertanyaan Sokratik.\n"
        "5. Jangan bertanya lebih dari satu kali dalam satu respons.\n\n"
        "[BAHASA_DAN_GAYA]\n"
        "Gunakan Bahasa Indonesia baku yang ramah. Jika siswa memakai 'aku', gunakan 'kamu'. "
        "Jika siswa memakai 'saya', gunakan 'Anda'. Hindari kata tidak baku.\n\n"
        "[FOKUS_TUGAS]\n"
        "Siswa sedang membahas hasil evaluasi kuis pilihan ganda. Gunakan data soal, "
        "jawaban siswa, kunci jawaban, penjelasan, dan nilai sebagai referensi utama.\n\n"
        "[ATURAN_KHUSUS]\n"
        "1. Jangan langsung menyatakan kunci jawaban.\n"
        "2. Jangan sekadar berkata jawaban siswa benar atau salah.\n"
        "3. Jika jawaban salah, bedah satu letak miskonsepsi utama.\n"
        "4. Jika jawaban benar, uji pemahaman dengan menanyakan alasan.\n"
        "5. Pilih satu soal atau pola kesalahan paling penting terlebih dahulu.\n\n"
        "[FORMAT_RESPONS]\n"
        "1. Afirmasi atau validasi faktual.\n"
        "2. Isolasi letak miskonsepsi atau alasan konseptual.\n"
        "3. Satu pertanyaan Sokratik.\n\n"
        "[CONTOH_GAYA]\n"
        "Gunakan: 'Pilihan yang kamu ambil tampaknya berangkat dari ide bahwa kedua besaran "
        "selalu berubah searah. Dari informasi pada soal, tanda apa yang menunjukkan bahwa "
        "hubungan tersebut tidak selalu searah?'"
    ),
}

MODE_LABELS = list(SYSTEM_PROMPTS.keys())
MODE_INFO = {
    "Materi":        "Diskusi & pemahaman materi bacaan",
    "Essay":         "Review & perbaikan esai siswa",
    "Pilihan Ganda": "Analisis hasil kuis pilihan ganda",
}

# ── HELPERS ──────────────────────────────────────────────────

def history_to_messages(history, system_prompt):
    """Konversi history Gradio ke format OpenAI messages."""
    messages = [{"role": "system", "content": system_prompt}]
    for turn in history:
        # Support kedua format: dict (Gradio 6) dan list (Gradio 3/4)
        if isinstance(turn, dict):
            messages.append({"role": turn["role"], "content": turn["content"]})
        else:
            if turn[0]:
                messages.append({"role": "user",      "content": turn[0]})
            if turn[1]:
                messages.append({"role": "assistant", "content": turn[1]})
    return messages


def make_turn(user_msg, bot_msg=""):
    """Buat satu giliran percakapan sesuai format Gradio yang aktif."""
    try:
        # Coba format Gradio 6 (dict)
        return [
            {"role": "user",      "content": user_msg},
            {"role": "assistant", "content": bot_msg},
        ]
    except Exception:
        return [[user_msg, bot_msg]]


def on_mode_change(mode):
    return SYSTEM_PROMPTS[mode], [], f"**Mode aktif:** {mode} — {MODE_INFO[mode]}"


def chat(user_message, history, system_prompt, temperature, max_tokens):
    if not user_message.strip():
        return "", history

    messages = history_to_messages(history, system_prompt)
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model":       MODEL_NAME,
        "messages":    messages,
        "max_tokens":  int(max_tokens),
        "temperature": float(temperature),
        "stream":      True,
    }
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    # Deteksi format history yang dipakai Gradio versi ini
    use_dict = len(history) == 0 or isinstance(history[0], dict) if history else True

    if use_dict:
        new_turns = [
            {"role": "user",      "content": user_message},
            {"role": "assistant", "content": ""},
        ]
    else:
        new_turns = [[user_message, ""]]

    history = history + new_turns

    try:
        with requests.post(
            f"{API_BASE}/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=120,
        ) as resp:
            resp.raise_for_status()
            collected = ""
            for raw_line in resp.iter_lines():
                if not raw_line:
                    continue
                line = raw_line.decode("utf-8")
                if line.startswith("data: "):
                    line = line[6:]
                if line.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(line)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    collected += delta
                    if use_dict:
                        history[-1]["content"] = collected
                    else:
                        history[-1][1] = collected
                    yield "", history
                except (json.JSONDecodeError, KeyError):
                    continue

    except requests.exceptions.ConnectionError:
        msg = "Koneksi gagal. Pastikan endpoint aktif."
        if use_dict:
            history[-1]["content"] = msg
        else:
            history[-1][1] = msg
        yield "", history
    except requests.exceptions.Timeout:
        msg = "Timeout. Model terlalu lama merespons."
        if use_dict:
            history[-1]["content"] = msg
        else:
            history[-1][1] = msg
        yield "", history
    except Exception as e:
        msg = f"Error: {str(e)}"
        if use_dict:
            history[-1]["content"] = msg
        else:
            history[-1][1] = msg
        yield "", history


def clear_history():
    return [], []

# ── DETEKSI PARAMETER CHATBOT YANG TERSEDIA ──────────────────
import inspect

def build_chatbot():
    """Buat gr.Chatbot dengan hanya parameter yang didukung versi ini."""
    sig = inspect.signature(gr.Chatbot.__init__)
    params = sig.parameters
    kwargs = {"label": "Percakapan"}
    if "height"  in params: kwargs["height"]  = 500
    if "type"    in params: kwargs["type"]    = "messages"
    return gr.Chatbot(**kwargs)

# ── UI ───────────────────────────────────────────────────────
with gr.Blocks(title="AI Mentor — Sekolah Rakyat") as demo:

    gr.Markdown("# Sekolah Rakyat — AI Mentor\nPilih mode sesi, lalu mulai percakapan.")

    with gr.Row():
        with gr.Column(scale=3):
            mode_radio = gr.Radio(
                choices=MODE_LABELS,
                value=MODE_LABELS[0],
                label="Mode Sesi",
            )
            mode_info_md = gr.Markdown(
                value=f"**Mode aktif:** {MODE_LABELS[0]} — {MODE_INFO[MODE_LABELS[0]]}"
            )

            chatbot = build_chatbot()   # auto-detect parameter yang tersedia

            with gr.Row():
                msg_box = gr.Textbox(
                    placeholder="Ketik pesan, lalu Enter atau klik Kirim...",
                    label="",
                    scale=8,
                    lines=2,
                )
                send_btn  = gr.Button("Kirim",     variant="primary",   scale=1)
                clear_btn = gr.Button("Bersihkan", variant="secondary", scale=1)

        with gr.Column(scale=1):
            gr.Markdown("### Parameter")
            sys_prompt = gr.Textbox(
                value=SYSTEM_PROMPTS[MODE_LABELS[0]],
                label="System Prompt",
                lines=16,
            )
            temp_slider = gr.Slider(
                0.0, 2.0, value=TEMPERATURE, step=0.05,
                label="Temperature",
            )
            max_tok_slider = gr.Slider(
                64, 8192, value=MAX_TOKENS, step=64,
                label="Max Tokens",
            )
            gr.Markdown(f"**Endpoint:** `{API_BASE}`\n\n**Model:** `{MODEL_NAME}`")

    state = gr.State([])

    mode_radio.change(
        fn=on_mode_change,
        inputs=[mode_radio],
        outputs=[sys_prompt, chatbot, mode_info_md],
    ).then(lambda h: h, inputs=[chatbot], outputs=[state])

    send_btn.click(
        fn=chat,
        inputs=[msg_box, state, sys_prompt, temp_slider, max_tok_slider],
        outputs=[msg_box, chatbot],
    ).then(lambda h: h, inputs=[chatbot], outputs=[state])

    msg_box.submit(
        fn=chat,
        inputs=[msg_box, state, sys_prompt, temp_slider, max_tok_slider],
        outputs=[msg_box, chatbot],
    ).then(lambda h: h, inputs=[chatbot], outputs=[state])

    clear_btn.click(fn=clear_history, outputs=[chatbot, state])


if __name__ == "__main__":
    # Cek apakah launch() mendukung theme & css
    launch_sig = inspect.signature(demo.launch)
    launch_kwargs = {
        "server_name": "0.0.0.0",
        "server_port": 7860,
        "share":       False,
        "inbrowser":   True,
    }
    if "theme" in launch_sig.parameters:
        launch_kwargs["theme"] = gr.themes.Soft(
            primary_hue="violet", secondary_hue="slate"
        )
    if "css" in launch_sig.parameters:
        launch_kwargs["css"] = "footer { display: none !important; }"

    demo.launch(**launch_kwargs)
PYEOF
echo "done"