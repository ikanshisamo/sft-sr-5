[PERINTAH]
Buatkan simulasi SELURUH percakapan (dari awal hingga akhir) antara Mentor Matematika dan Siswa SMA berdasarkan konteks dan aturan di bawah ini.

[KONTEKS_SESI]
[ISI_KONTEKS]

[KARAKTERISTIK_SISWA]
Perankan siswa dengan karakteristik gabungan berikut ini:

-- Sisi Kognitif --
[TEKS_KARAKTER_KOGNITIF]

-- Sisi Emosi --
[TEKS_KARAKTER_EMOSI]

-- Sisi Konteks --
[TEKS_KARAKTER_OOT]
[TEKS_KARAKTER_BAD]

Siswa harus memulai pesan pertama (turn 1) dengan format baku berikut:
[PREFIX_SISWA]
(Setelah baris awalan di atas, lanjutkan dengan pertanyaan atau pernyataan awal siswa secara natural sesuai karakteristik yang diberikan.)

INSTRUKSI KHUSUS:

1. HANYA pesan pertama (turn 1) dari role "user" yang boleh dan wajib menggunakan label:
   * [Emosi: ...]
   * [Konteks: ...]

2. Format label tersebut WAJIB muncul di awal pesan pertama sebelum isi percakapan siswa.

3. Mulai dari pesan kedua (turn 2) dan seluruh pesan berikutnya, DILARANG menyertakan kembali label:
   * [Emosi: ...]
   * [Konteks: ...]

4. Pada turn 2 dan seterusnya, siswa harus menulis respons secara natural, formal, dan langsung sesuai karakteristik yang diberikan tanpa menggunakan label, metadata, penanda format, atau keterangan tambahan apa pun.

5. Label [Emosi: ...] dan [Konteks: ...] hanya berfungsi sebagai metadata pembuka pada turn 1 dan tidak boleh diulang pada bagian mana pun setelah turn pertama.

6. Apabila percakapan memiliki banyak turn, aturan ini tetap berlaku: label hanya muncul satu kali pada pesan pertama siswa dan tidak pernah muncul kembali pada turn berikutnya.

[KARAKTERISTIK_MENTOR]
Patuhi seluruh pedoman Sokratik dan struktur respons yang ada di system prompt yang direferensikan.
[KARAKTERISTIK_MENTOR_DINAMIS]

[ATURAN_SIMULASI]
1. TARGET TURN: Tepat [JUMLAH_TURN] turn (pasangan user-assistant). Kamu dilarang keras menyelesaikan percakapan sebelum mencapai target ini.
2. INSIDEN OOT: Siswa WAJIB memunculkan obrolan di luar topik (OOT) sebanyak tepat [JUMLAH_OOT]. Insiden ini dapat disebar di turn mana saja secara natural.
3. INSIDEN BAD: Siswa WAJIB memunculkan pernyataan negatif/menyimpang sebanyak tepat [JUMLAH_BAD]. Insiden WAJIB diletakkan pada turn yang berbeda dengan kemunculan insiden OOT. Insiden ini dapat disebar di turn mana saja secara natural.

[FORMAT_OUTPUT]
Keluarkan HANYA array JSON yang valid.
- Tidak ada teks pengantar/penutup, tidak ada markdown (```json).
- JSON HARUS memuat SELURUH percakapan dari turn 1 sampai turn target selesai.
- Format JSON:
[
  {
    "role": "system",
    "content": "math_f_sys_[LABEL_EMOSI]_[LABEL_KOGNITIF].md"
  },
  {
    "role": "user",
    "content": "(Pesan Turn 1 - Wajib pakai awalan [Emosi] dan [Konteks] dari prefix)"
  },
  {
    "role": "assistant",
    "content": "(Paragraf penjelasan materi dan validasi)\n\n> (Pertanyaan pancingan/penutup. WAJIB DIAWALI TANDA > DAN SPASI SETELAH 2x ENTER!)"
  },
  {
    "role": "user",
    "content": "(Pesan Turn 2 - Natural, TANPA label apapun, mungkin mulai OOT/Bad di sini)"
  },
  {
    "role": "assistant",
    "content": "(Paragraf penjelasan materi dan validasi)\n\n> (Pertanyaan pancingan/penutup. WAJIB DIAWALI TANDA > DAN SPASI SETELAH 2x ENTER!)"
  },
  ... lanjutkan terus objek user dan assistant secara bergantian hingga mencapai target [JUMLAH_TURN] ...
]
