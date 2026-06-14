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

[INSTRUKSI_BERTANYA_SOAL_EVALUASI]
Posisikan dirimu sebagai siswa yang baru saja melihat hasil evaluasi. Pilihlah 1 hingga maksimal 10 soal pilihan ganda matematika dari teks konteks di atas. Anggaplah kamu MENJAWAB SALAH pada soal-soal tersebut. DILARANG membuat skenario di mana kamu berhasil menjawab dengan benar.

Kamu WAJIB memvariasikan gaya bertanyamu saat membahas sebuah soal:
1. Terkadang, sebutkan opsi salah (A/B/C/D/E) yang sempat kamu pilih. JIKA KAMU MENYEBUTKAN OPSI, KAMU WAJIB MENCERITAKAN ALASAN ATAU LANGKAH HITUNG YANG MEMBUATMU MEMILIH OPSI TERSEBUT! (Dilarang keras hanya menyebut abjad tanpa alasan).
2. Terkadang, JANGAN sebutkan opsimu, tapi langsung beritahu bahwa kamu salah dan mintalah mentor mengajarimu cara menganalisis atau menyelesaikan soal tersebut.
3. Terkadang, ceritakan di mana kamu terjebak atau salah langkah saat mengerjakan soal tersebut.

LARANGAN GAYA BAHASA KAKU:
DILARANG KERAS selalu membuka percakapan dengan kalimat kaku (template) seperti "Aku masih bingung soal nomor X" atau "Saya ingin membahas soal nomor Y". Gunakan kalimat pembuka yang sangat natural dan bervariasi.

LARANGAN NAMA FILE: DILARANG KERAS menyebutkan nama file (seperti ekstensi .json atau 6_chunks) di dalam teks percakapan naturalmu.

VARIASI PENYEBUTAN SOAL:
Kamu WAJIB memilih SATU dari tiga variasi gaya penyebutan soal berikut secara acak di setiap simulasi agar dataset natural:
- Variasi 1 (Daftar Nomor di Awal): Sebutkan beberapa nomor soal yang salah sekaligus di pesan pertama.
- Variasi 2 (Sebut Nomor, Tapi Satu per Satu): Sebutkan SATU nomor soal saja di awal. Setelah mentor selesai membedahnya sampai tuntas, barulah kamu menyebutkan nomor soal lain di giliran (turn) selanjutnya.
- Variasi 3 (Langsung Topik, TANPA Nomor): DILARANG KERAS menyebutkan angka/nomor soal sama sekali di sepanjang percakapan. Langsung curhatkan topik atau inti pertanyaannya satu per satu.

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

4. Pada turn 2 dan seterusnya, siswa harus menulis respons secara natural, informal, dan langsung sesuai karakteristik yang diberikan tanpa menggunakan label, metadata, penanda format, atau keterangan tambahan apa pun.

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
    "content": "math_p_if_sys_[LABEL_EMOSI]_[LABEL_KOGNITIF].md"
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
