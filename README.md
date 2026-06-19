# 🥤 Bottle Counting API

## 📖 Deskripsi Program

Bottle Counting API adalah aplikasi berbasis Python dan FastAPI yang digunakan untuk melakukan deteksi dan perhitungan jumlah produk secara otomatis menggunakan model YOLO.

Sistem ini dirancang untuk membantu proses inspeksi produk pada lini produksi dengan memanfaatkan kamera yang terhubung ke Mesin. Setiap hasil deteksi akan disimpan ke database beserta gambar original, gambar hasil deteksi, jumlah produk yang terdeteksi, status inspeksi, ukuran file, dan waktu proses.

---

## ✨ Fitur Utama

- 📸 Upload gambar melalui REST API
- 🤖 Deteksi produk menggunakan YOLO
- 🔢 Perhitungan jumlah produk otomatis
- 💾 Penyimpanan gambar original
- 🖼️ Penyimpanan gambar hasil deteksi
- 🗄️ Penyimpanan log inspeksi ke MySQL
- 🔐 API Key Authentication
- 🌐 Optional IP Whitelist
- 📊 Monitoring ukuran file dan processing time
- ❤️ Health Check Endpoint

---

## 🏗️ Arsitektur Sistem

### Topologi

```text
Internet User
       │
       ▼
Domain Dashboard
(Cloudflare Tunnel)
       │
       ▼
Dashboard Server
192.168.1.10 //Ip Lokal
       │
       │ Internal LAN
       ▼
Bottle Counting API
192.168.1.20 // Ip Lokal
       │
       ├── YOLO Model
       ├── Storage
       └── MySQL
```

### Alur Kerja

```text
Operator
    │
    ▼
Dashboard
    │
    ▼
Capture Image
    │
    ▼
POST /detect
    │
    ▼
FastAPI
    │
    ▼
YOLO Detection
    │
    ▼
Save Image
    │
    ▼
Save Database
    │
    ▼
Return Result
```

---

## 🛠️ Teknologi yang Digunakan

### Backend

- Python 3.11+
- FastAPI
- Uvicorn

### Artificial Intelligence

- Ultralytics YOLO
- OpenCV

### Database

- MySQL / MariaDB

### Library Tambahan

- python-dotenv
- mysql-connector-python
- python-multipart

---

## 📁 Struktur Folder

```text
Program_Counting/
│
├── api/
│   └── routes.py
│
├── database/
│   ├── db.py
│   └── migrate.py
│
├── detector/
│   └── detection.py
│
├── helpers/
│   └── storage.py
│
├── models/
│   └── best.pt
│
├── storage/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

### 📂 Penjelasan Folder

| Folder   | Fungsi                            |
| -------- | --------------------------------- |
| api      | Endpoint API                      |
| database | Koneksi dan migration database    |
| detector | YOLO detection                    |
| helpers  | Utility dan storage helper        |
| models   | Model YOLO                        |
| storage  | Penyimpanan gambar hasil inspeksi |

---

## 🗄️ Struktur Database

### inspection_logs

```sql
CREATE TABLE inspection_logs (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(100) NOT NULL,

    image_original VARCHAR(255) NOT NULL,

    image_result VARCHAR(255) NOT NULL,

    count INT NOT NULL,

    status VARCHAR(10) NOT NULL,

    file_size_mb DECIMAL(10,2) NOT NULL DEFAULT 0,

    processing_time DECIMAL(10,2) NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
```

---

## 📥 Getting Started

Clone repository:

```bash
git clone https://github.com/username/bottle-counting-api.git
```

Masuk ke folder project:

```bash
cd bottle-counting-api
```

---

## ⚙️ Instalasi

### 1️⃣ Buat Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependency

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Konfigurasi Environment

Rename file `.env.example` menjadi `.env`

```env
DB_HOST= Host Database >> Default: localhost
DB_PORT= Port Database >> Default: 3306
DB_NAME= Nama Database

DB_USER= User Database >> Default: root
DB_PASSWORD= Password Database

EXPECTED_PRODUCTS= Minimal Produk yang Diharapkan
API_KEY= Unique API Key untuk mengakses API

MAX_FILE_SIZE_MB= Batas Maksimal Ukuran File dalam MB

ENABLE_IP_WHITELIST= Apakah IP Whitelist diaktifkan (true/false)
DASHBOARD_IP= IP yang diizinkan untuk mengakses aplikasi counting

STORAGE_PATH= Path untuk menyimpan file yang diunggah >> Default: storage

YOLO_MODEL=models/best.pt #Jangan dirubah, ini adalah path default untuk model YOLO
YOLO_CONFIDENCE= Confidence Threshold untuk YOLO Model >> Default: 0.5
```

---

### 4️⃣ Jalankan Migration

```bash
python database/migrate.py
```

---

## 🚀 Menjalankan Program

Development

```bash
uvicorn app:app --reload
```

Production

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 📡 API Endpoint

### Health Check

```http
GET /health
```

Response

```json
{
  "status": "healthy",
  "service": "bottle-counting-api",
  "version": "1.0.0"
}
```

---

### Deteksi Produk

```http
POST /detect
```

Header

```http
X-API-KEY: your-secret-api-key
```

Form Data

```text
username : UwaaW
file     : image.jpg
```

---

## 💾 Struktur Storage

```text
storage/
└── YYYY/
    └── MM/
        └── DD/
            ├── original/
            └── result/
```

Contoh

```text
storage/
└── 2026/
    └── 06/
        └── 19/
            ├── original/
            └── result/
```

---

## 📊 Monitoring Statistik

Setiap inspeksi menyimpan:

- Username
- Jumlah Produk
- Status
- Ukuran File
- Processing Time
- Waktu Inspeksi

Contoh statistik harian:

```sql
SELECT
    DATE(created_at) AS tanggal,
    COUNT(*) AS total_scan,
    SUM(file_size_mb) AS total_storage_mb,
    AVG(processing_time) AS avg_processing_time
FROM inspection_logs
GROUP BY DATE(created_at);
```

---

## 🔐 Security

- API Key Authentication
- Optional IP Whitelist
- File Extension Validation
- Upload Size Limitation
- Internal Service Architecture

---

## 🚀 Deployment Target

- Ubuntu Server
- FastAPI
- YOLO
- MySQL
- Internal LAN
- Dashboard via Cloudflare Tunnel

---

### AI Model

🤖 YOLO

### Backend

⚡ FastAPI

### Database

🗄️ MySQL

---

## 📌 Version

**Bottle Counting API v1.0**

### Built with ❤️ by Mr_UwaaW
