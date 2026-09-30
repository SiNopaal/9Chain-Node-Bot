# 9Chain Automation Bot 🚀

Bot otomasi multi-akun untuk ekosistem **9Chain** (`https://www.9chain.com` / API v2 `https://api.9chain.com/v2`).
Bot ini telah direorganisasi dan dipindahkan ke folder:
`C:\Users\asust\OneDrive\Documents\Script Bot Automation\9chain-bot`

---

## 📋 Daftar Fitur Otomasi

1. **Multi-Account Management (35 Akun)**:
   - Mendukung 35 akun yang tersimpan secara terstruktur di `accounts.txt`.
   - Format kredensial fleksibel: `email:password` atau baris `email` (fallback otomatis ke `DEFAULT_PASSWORD`).
2. **Auto Daily Check-in**:
   - Mengecek status check-in harian dan mengklaim bonus XP harian serta mempertahankan check-in streak.
3. **Auto-Tap (Taps Execution)**:
   - Membaca sisa tap harian (`tapsRemaining`).
   - Melakukan batch tap otomatis secara aman hingga sisa tap habis.
4. **Auto Smart Upgrade Node Tier**:
   - Memeriksa syarat XP dan upgrade tingkat Node Tier akun ke level tertinggi yang terjangkau.
5. **Auto Smart Upgrade Komponen (ROI Terbaik)**:
   - Menganalisis katalog komponen (`relay_nodes`, `firewall`, `anti_sybil`, `cpu`, `ram`, `consensus_tuner`, `sharding`, dll.).
   - Memilih upgrade berdasarkan `paybackHours` tercepat / ROI terbaik agar menghasilkan laju XP (`contributionRate`) maksimal.
6. **Mode Loop 24 Jam**:
   - Siklus otomatis berulang setelah jeda waktu istirahat (`LOOP_REST_MINUTES`).
7. **Pengecekan Status Instan**:
   - Mode read-only untuk memantau Tier, XP Total, Contribution Rate, dan sisa Tap 35 akun tanpa menghabiskan resource.

---

## 📁 Struktur Direktori

```
9chain-bot/
├── accounts.txt          # Daftar 35 email & password akun
├── config.py             # Parser konfigurasi & pembaca akun
├── api_client.py         # HTTP Client ke API 9Chain v2 (urllib)
├── bot_runner.py         # Runner alur otomatis per-akun & loop
├── main.py               # Menu interaktif CLI & argumen eksekusi
├── .env                  # Pengaturan environment & preferensi bot
├── .env.example          # Contoh template konfigurasi
├── requirements.txt      # Dependensi (Zero dependency / Standard Library)
├── wallets_600.json      # File data dompet cadangan dari repositori lama
├── scripts/              # Skrip JavaScript pendukung (claim, buy, fund)
└── README.md             # Dokumentasi panduan lengkap
```

---

## ⚙️ Konfigurasi (`.env`)

```ini
BASE_API_URL=https://api.9chain.com/v2
DEFAULT_PASSWORD=Naufal123
TAP_BATCH_SIZE=500
DELAY_BETWEEN_ACCOUNTS=2
LOOP_REST_MINUTES=60
AUTO_UPGRADE_TIER=true
AUTO_UPGRADE_COMPONENTS=true
MAX_RETRIES=3
TIMEOUT=15
```

---

## 🚀 Cara Menjalankan

Buka PowerShell / Terminal di folder bot:
```powershell
cd "C:\Users\asust\OneDrive\Documents\Script Bot Automation\9chain-bot"
```

### 1. Mode Menu Interaktif
```powershell
python main.py
```
Pilihan menu:
- `[1]` Jalankan 1 Siklus Penuh (Semua 35 Akun)
- `[2]` Jalankan Mode Loop 24 Jam (Loop otomatis terus-menerus)
- `[3]` Cek Status, XP, dan Sisa Tap Semua Akun (Read-only)
- `[4]` Jalankan Satu Akun Tertentu
- `[0]` Keluar

### 2. Mode Perintah Cepat (Direct Argument)
- **Jalankan 1 Siklus Penuh**:
  ```powershell
  python main.py 1
  ```
- **Jalankan Mode Loop 24 Jam**:
  ```powershell
  python main.py 2
  ```
- **Cek Status Semua Akun**:
  ```powershell
  python main.py 3
  ```
- **Jalankan Akun Nomor 1 saja**:
  ```powershell
  python main.py 4 1
  ```

---

## 👥 Status Akun (35 Akun)
Semua 35 akun telah dipindahkan dan terkonfigurasi di `accounts.txt`.
Satu akun dengan password kustom (`aaiyaa33331@gmail.com`: `Naufal1233`) telah disetel dengan benar.
*Catatan: Akun `maulana88778@gmail.com` sebelumnya mengalami kegagalan login dengan password default `Naufal123` - Anda dapat memperbarui passwordnya kapan saja langsung di `accounts.txt`.*
