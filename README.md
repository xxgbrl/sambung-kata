# 🎮 Sambung Kata — Cheatsheet

> Cheatsheet tool untuk game **Sambung Kata** dengan database 71.000+ kata Bahasa Indonesia dari KBBI.

Cari kata berdasarkan awalan, akhiran, atau huruf yang terkandung. Tandai kata yang sudah terpakai, hapus kata yang tidak valid, dan jebak lawan dengan fitur **Trap**.

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 📸 Preview

|     Pencarian Awalan      |          Trap Dialog           |
| :-----------------------: | :----------------------------: |
| Cari kata berawalan "men" | Atur suffix jebakan buat lawan |

---

## ✨ Fitur

- **🔍 3 Mode Pencarian** — Awalan (Prefix), Akhiran (Suffix), dan Mengandung (Contains)
- **⚡ Binary Search** — Pencarian prefix super cepat di 71k+ kata
- **🪤 Trap System** — Prioritaskan kata yang berakhiran huruf susah (z, x, q, dll.) biar lawan mati kutu
- **✅ Tandai Terpakai** — Klik kata untuk centang, biar ga kepake dua kali
- **🗑️ Hapus Kata** — Hapus kata yang tidak valid langsung dari database (permanen ke `words.json`)
- **➕ Tambah Kata** — Tambah kata baru yang belum ada di database
- **📋 Copy Kata** — Satu klik langsung copy ke clipboard
- **🔀 Urutan Acak** — Hasil pencarian di-shuffle setiap kali biar ga monoton
- **💾 Persistent** — Semua perubahan (hapus/tambah) langsung tersimpan ke database

---

## 🚀 Quick Start

### Prasyarat

- [Python 3.7+](https://www.python.org/downloads/) (sudah terinstall di kebanyakan sistem)

### Jalankan

```bash
# Clone repository
git clone https://github.com/verssache/sambung-kata.git
cd sambung-kata

# Jalankan server
python server.py
```

Buka browser ke **[http://localhost:8000](http://localhost:8000)** — selesai!

> **Catatan:** Jangan pakai `python -m http.server` karena fitur hapus/tambah kata butuh API dari `server.py` untuk persist ke `words.json`.

---

## 📁 Struktur Proyek

```
sambungkata/
├── index.html      # Single-page app (HTML + CSS + JS, semua dalam satu file)
├── server.py       # Dev server dengan API untuk modifikasi words.json
├── words.json      # Database 71.000+ kata Bahasa Indonesia (sorted array)
└── README.md
```

---

## 🪤 Fitur Trap

Fitur andalan buat menang sambung kata. Konsepnya sederhana:

1. Buka dialog **🪤 Trap** dan masukkan suffix-suffix yang susah (misal: `z`, `x`, `za`)
2. Saat mencari kata, hasil yang berakhiran suffix trap akan **muncul duluan**
3. Pakai kata tersebut biar lawan harus nyambung dari huruf yang susah

### Saran Suffix Jebakan

| Suffix | Tingkat Kesulitan | Alasan                                    |
| ------ | :---------------: | ----------------------------------------- |
| `z`    |        🔴         | Hampir tidak ada kata berawalan Z di KBBI |
| `x`    |        🔴         | Nyaris mustahil untuk disambung           |
| `q`    |        🔴         | Tidak ada di KBBI                         |

Trap bersifat **prioritas**, bukan filter — kalau tidak ada kata yang cocok dengan trap suffix, kata-kata biasa tetap ditampilkan.

---

## ⚙️ Server API

`server.py` menyediakan dua endpoint untuk memodifikasi database secara langsung:

### `POST /api/delete`

Menghapus kata dari `words.json`.

```json
{
  "word": "atam"
}
```

**Response:**

```json
{
  "ok": true,
  "total": 71234
}
```

### `POST /api/add`

Menambahkan kata baru ke `words.json` (sorted insert).

```json
{
  "word": "newword"
}
```

**Response:**

```json
{
  "ok": true,
  "total": 71236
}
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Aksi                   |
| -------- | ---------------------- |
| `/`      | Fokus ke search bar    |
| `Escape` | Clear pencarian & blur |

---

## 🛠️ Development

### Modifikasi Database

Semua perubahan melalui UI (hapus/tambah) otomatis tersimpan ke `words.json` via server API. Tidak perlu export manual.

### Sumber Data

Database kata dikumpulkan dari berbagai sumber KBBI open-source:

Sambung Kata

- [kumpulan-kata-bahasa-indonesia-KBBI](https://github.com/damzaky/kumpulan-kata-bahasa-indonesia-KBBI)
- [kbbi-harvester-cdn](https://github.com/Naandalist/kbbi-harvester-cdn)
- [ays-stemming](https://github.com/Notnoir/ays-stemming)
- [ays-stemming](https://github.com/Notnoir/ays-stemming)

Last Letter

- [wordlist-medicalterms-en](https://github.com/glutanimate/wordlist-medicalterms-en)
- [Wordlist](https://github.com/jeremy-rifkin/Wordlist)
- [english-wordlists](https://github.com/mahavivo/english-wordlists)
- [top-english-wordlists](https://github.com/david47k/top-english-wordlists)
- [The-Oxford-3000](https://github.com/sapbmw/The-Oxford-3000)

Filter yang diterapkan:

- Hanya huruf `a-z` (tanpa spasi, tanda hubung, atau karakter unicode)
- Minimal 3 karakter
- Kata tunggal (bukan frasa)

---

## 📄 License

MIT License — bebas digunakan dan dimodifikasi.

---

<div align="center">
  <sub>Built for winning Sambung Kata 🏆</sub>
</div>
