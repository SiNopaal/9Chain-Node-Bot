# 9Chain Node Automation Bot 🚀

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-9Chain%20v2%20API-orange.svg)](https://www.9chain.com)

## Bot otomasi multi-akun tangguh untuk ekosistem **9Chain** https://www.9chain.com/ref/517464432 .
Dibangun menggunakan Python standard library (zero-dependency core) dengan fitur auto check-in, auto-tap batch, smart node tier upgrade, dan optimasi komponen berbasis Return of Investment (ROI) terbaik.

---

## 📋 Daftar Fitur Utama

- 👥 **Multi-Account Management**:
  - Mendukung banyak akun secara terstruktur di `accounts.txt`.
  - Format kredensial fleksibel: `email:password` atau baris `email` (fallback otomatis ke `DEFAULT_PASSWORD` di `.env`).
- 📅 **Auto Daily Check-in**:
  - Memeriksa status check-in harian dan mengklaim bonus XP harian serta mempertahankan check-in streak.
- ⚡ **Auto-Tap (Batch Tap Execution)**:
  - Membaca sisa kuota tap harian (`tapsRemaining`).
  - Melakukan batch tap otomatis secara aman hingga sisa tap habis.
- 📈 **Smart Node Tier Upgrade**:
  - Mengecek syarat XP dan melakukan upgrade tingkat Node Tier akun ke level tertinggi yang terjangkau secara otomatis.
- 🛠️ **Smart Component Upgrade (Best ROI)**:
  - Menganalisis katalog komponen (`relay_nodes`, `firewall`, `anti_sybil`, `cpu`, `ram`, `consensus_tuner`, `sharding`, dll.).
  - Memilih upgrade berdasarkan `paybackHours` tercepat / ROI terbaik agar menghasilkan laju XP (`contributionRate`) maksimal.
- 🔄 **Mode Loop 24 Jam**:
  - Berjalan otomatis secara berkala dengan jeda waktu istirahat (`LOOP_REST_MINUTES`) yang dapat disesuaikan.
- 📊 **Pengecekan Status Instan (Read-Only)**:
  - Mode audit cepat untuk memantau Tier, XP Total, Contribution Rate, dan sisa Tap semua akun tanpa menghabiskan kuota atau resource.

---

## 📁 Struktur Direktori

```text
9chain-bot/
├── config.py             # Parser konfigurasi & pembaca akun
├── api_client.py         # HTTP Client ke API 9Chain v2 (urllib)
├── bot_runner.py         # Runner alur otomatis per-akun & loop
├── main.py               # Menu interaktif CLI & argumen eksekusi
├── accounts.example.txt  # Template daftar akun
├── .env.example          # Template konfigurasi environment
├── requirements.txt      # Dependensi Python
├── .gitignore            # Proteksi keamanan data sensitif
└── README.md             # Dokumentasi panduan lengkap
```

---

## ⚙️ Instalasi & Konfigurasi

### 1. Clone Repository
```bash
git clone https://github.com/SiNopaal/9Chain-Node-Bot.git
cd 9Chain-Node-Bot
```

### 2. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Environment (`.env`)
Salin file `.env.example` menjadi `.env`:
```bash
cp .env.example .env
```
Sesuaikan parameter sesuai kebutuhan:
```ini
BASE_API_URL=https://api.9chain.com/v2
DEFAULT_PASSWORD=YourPassword123
TAP_BATCH_SIZE=500
DELAY_BETWEEN_ACCOUNTS=2
LOOP_REST_MINUTES=60
AUTO_UPGRADE_TIER=true
AUTO_UPGRADE_COMPONENTS=true
MAX_RETRIES=3
TIMEOUT=15
```

### 4. Tambahkan Daftar Akun (`accounts.txt`)
Salin `accounts.example.txt` menjadi `accounts.txt`:
```bash
cp accounts.example.txt accounts.txt
```
Masukkan akun Anda (satu baris per akun):
```text
user1@gmail.com:PasswordKustom123
user2@gmail.com
```
*(Jika tidak menyertakan password, bot akan otomatis menggunakan `DEFAULT_PASSWORD` dari file `.env`)*.

---

## 🚀 Cara Menjalankan

### Mode Menu Interaktif
Jalankan menu CLI:
```bash
python main.py
```
Pilihan menu:
- `[1]` Jalankan 1 Siklus Penuh (Semua Akun)
- `[2]` Jalankan Mode Loop 24 Jam (Loop otomatis terus-menerus)
- `[3]` Cek Status, XP, dan Sisa Tap Semua Akun (Read-only)
- `[4]` Jalankan Satu Akun Tertentu
- `[0]` Keluar

### Mode Perintah Cepat (Direct Argument)
- **Jalankan 1 Siklus Penuh**:
  ```bash
  python main.py 1
  ```
- **Jalankan Mode Loop 24 Jam**:
  ```bash
  python main.py 2
  ```
- **Cek Status Semua Akun**:
  ```bash
  python main.py 3
  ```
- **Jalankan Akun Nomor 1 saja**:
  ```bash
  python main.py 4 1
  ```

---

## 🔒 Keamanan
File `.env`, `accounts.txt`, dan file wallet otomatis dikecualikan oleh `.gitignore` sehingga data pribadi Anda tidak akan pernah bocor ke repository GitHub publik.

---

## ⚠️ Disclaimer
Script ini dibuat semata-mata untuk keperluan otomasi pribadi dan pembelajaran. Penggunaan bot sepenuhnya merupakan tanggung jawab pengguna masing-masing.
