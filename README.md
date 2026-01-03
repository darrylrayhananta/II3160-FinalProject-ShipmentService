# II3160 Teknologi Sistem Terintegrasi - Final Project
## Service: Shipment & Tracking Service

Layanan ini bertanggung jawab untuk menangani proses pengiriman, kalkulasi biaya ongkir, dan pelacakan lokasi barang secara real-time.

### 👥 Anggota Kelompok
- **Muhammad Adam Mirza** - [18223015] 
- **Darryl Rayhananta Adenan** - [18223042] 

### 📝 Deskripsi Sistem
Shipment Service merupakan *core subdomain* yang mengorkestrasi proses logistik. Service ini terintegrasi dengan Warehouse Core melalui komunikasi REST API yang aman (menggunakan Token Authentication). Fitur utama meliputi kalkulasi biaya berdasarkan dimensi volumetrik dan berat asli, otomatisasi pembuatan resi, serta fitur tracking lokasi pengiriman.

### 🛠️ Tech Stack
- **Framework:** Django 5.x
- **Integration:** Python Requests (Synchronous API Call)
- **Database:** Supabase (PostgreSQL)
- **Security:** API Key / Bearer Token Authentication

### 🚀 Cara Menjalankan (Local)
1. Install dependencies: `pip install -r requirements.txt`
2. Konfigurasi `.env`: Masukkan `WAREHOUSE_API_TOKEN` dan `WAREHOUSE_URL` dan kunci database `DATABASE_URL`.
3. Jalankan migrasi: `python manage.py migrate`
4. Jalankan server: `python manage.py runserver 8001`

### 📡 API Endpoints
- `POST /api/shipments/` - Inisiasi pengiriman baru
- `GET /api/shipments/<id>/` - Tracking lokasi & status
- `PATCH /api/shipments/<id>/` - Update lokasi kurir