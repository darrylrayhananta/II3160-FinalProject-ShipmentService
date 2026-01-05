# II3160 Teknologi Sistem Terintegrasi - Final Project
## Service: Shipment & Tracking Service

Layanan ini bertanggung jawab untuk menangani proses pengiriman, kalkulasi biaya ongkir, dan pelacakan lokasi barang secara real-time.

### 👥 Anggota Kelompok
- **Muhammad Adam Mirza** - [18223015] 
- **Darryl Rayhananta Adenan** - [18223042] 

---

## 📝 Deskripsi Sistem

Shipment Service merupakan *core subdomain* yang mengorkestrasi proses logistik. Service ini terintegrasi dengan Warehouse Core melalui komunikasi REST API yang aman (menggunakan Token Authentication). Fitur utama meliputi kalkulasi biaya berdasarkan dimensi volumetrik dan berat asli, otomatisasi pembuatan resi, serta fitur tracking lokasi pengiriman.

---

## 🛠️ Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Framework | Django 5.x |
| Database | PostgreSQL (Supabase) |
| Integration | Python Requests (Synchronous API Call) |
| Security | Bearer Token Authentication |
| CORS | django-cors-headers |

---

## 📦 Instalasi

### Prerequisites
- Python 3.10+
- PostgreSQL database (atau Supabase)
- Git

### Langkah Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/II3160-FinalProject-ShipmentService.git
   cd II3160-FinalProject-ShipmentService
   ```

2. **Buat virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi environment variables**
   
   Buat file `.env` di root folder:
   ```env
   DATABASE_URL=postgresql://username:password@host:port/database_name
   WAREHOUSE_URL=https://your-warehouse-service.com/api/packages/
   WAREHOUSE_API_TOKEN=your_secret_token_here
   ```

5. **Jalankan migrasi database**
   ```bash
   python manage.py migrate
   ```

---

## 🚀 Cara Menjalankan

### Development Server
```bash
python manage.py runserver 8001
```
Server akan berjalan di `http://localhost:8001`

### Production (dengan Gunicorn)
```bash
gunicorn shipment_service.wsgi:application --bind 0.0.0.0:8001
```

### Docker
```bash
docker build -t shipment-service .
docker run -p 8001:8001 --env-file .env shipment-service
```

---

## 📡 API Endpoints

Semua endpoint memerlukan header **Authorization** dengan format:
```
Authorization: Bearer <WAREHOUSE_API_TOKEN>
```

### 1. List Semua Shipment
```http
GET /api/shipments/
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "package_id": 101,
    "courier_name": "JNE Express",
    "tracking_number": "TRX-A1B2C3",
    "status": "IN_TRANSIT",
    "current_location": "Jakarta Hub",
    "created_at": "2026-01-05T10:00:00Z",
    "updated_at": "2026-01-05T12:30:00Z"
  }
]
```

---

### 2. Buat Shipment Baru
```http
POST /api/shipments/
Content-Type: application/json
```

**Request Body:**
```json
{
  "package_id": 101,
  "courier_name": "JNE Express"
}
```

**Response (201 Created):**
```json
{
  "message": "Shipment Created",
  "tracking_number": "TRX-A1B2C3",
  "status": "IN_TRANSIT"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Error message here"
}
```

---

### 3. Detail & Tracking Shipment
```http
GET /api/shipments/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "tracking_number": "TRX-A1B2C3",
  "status": "IN_TRANSIT",
  "current_location": "Bandung Distribution Center",
  "courier": "JNE Express"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Not Found"
}
```

---

### 4. Update Lokasi/Status Shipment
```http
PATCH /api/shipments/{id}/
Content-Type: application/json
```

**Request Body:**
```json
{
  "location": "Surabaya Hub",
  "status": "DELIVERED"
}
```

**Response (200 OK):**
```json
{
  "message": "Status Updated",
  "status": "DELIVERED"
}
```

---

## 🔐 Authentication

Service ini menggunakan **Bearer Token Authentication**. Token didefinisikan di environment variable `WAREHOUSE_API_TOKEN`.

### Contoh Request dengan cURL

```bash
# List all shipments
curl -X GET http://localhost:8001/api/shipments/ \
  -H "Authorization: Bearer your_token_here"

# Create new shipment
curl -X POST http://localhost:8001/api/shipments/ \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"package_id": 101, "courier_name": "JNE Express"}'

# Get shipment detail
curl -X GET http://localhost:8001/api/shipments/1/ \
  -H "Authorization: Bearer your_token_here"

# Update shipment location
curl -X PATCH http://localhost:8001/api/shipments/1/ \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"location": "Surabaya Hub", "status": "DELIVERED"}'
```

---

## 📊 Status Codes

| Status | Deskripsi |
|--------|-----------|
| `IN_TRANSIT` | Barang sedang dalam perjalanan |
| `DELIVERED` | Barang sudah sampai tujuan |
| `SHIPPED` | Barang sudah dikirim dari warehouse |

---

## 🔗 Integrasi dengan Warehouse Service

Saat membuat shipment baru, service ini akan:
1. Memvalidasi `package_id` ke Warehouse Service
2. Jika valid, membuat record shipment baru dengan tracking number unik
3. Mengupdate status package di Warehouse menjadi `SHIPPED`

---

## 📁 Struktur Project

```
├── main/
│   ├── models.py        # Model Shipment
│   ├── views.py         # API Views
│   ├── services.py      # Business Logic
│   ├── repositories.py  # Data Access Layer
│   ├── urls.py          # URL Routing
│   └── migrations/      # Database Migrations
├── shipment_service/
│   ├── settings.py      # Django Settings
│   ├── urls.py          # Root URL Config
│   └── wsgi.py          # WSGI Application
├── manage.py
├── requirements.txt
├── Dockerfile
└── README.md
```