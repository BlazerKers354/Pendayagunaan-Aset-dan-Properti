# Database Update Documentation

## Perubahan Database Schema

### Sebelum Perubahan:
- Tabel `properties` tunggal dengan field `property_type` untuk membedakan jenis properti

### Setelah Perubahan:
- Tabel `properties` dihapus
- Dibuat 2 tabel terpisah:
  1. `properti_tanah` - untuk properti tanah saja
  2. `properti_tanah_bangunan` - untuk properti tanah + bangunan

## Struktur Tabel Baru

### Tabel `properti_tanah`
```sql
CREATE TABLE properti_tanah (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(100) NOT NULL,
    price BIGINT NOT NULL,
    land_area DECIMAL(10,2) NOT NULL,
    certificate VARCHAR(50),
    facing VARCHAR(50),
    water_source VARCHAR(50),
    internet ENUM('Ya','Tidak') DEFAULT 'Tidak',
    hook ENUM('Ya','Tidak') DEFAULT 'Tidak',
    power INT DEFAULT 0,
    road_width VARCHAR(50),
    description TEXT,
    status ENUM('aktif','tidak_aktif') DEFAULT 'aktif',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);
```

### Tabel `properti_tanah_bangunan`
```sql
CREATE TABLE properti_tanah_bangunan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(100) NOT NULL,
    price BIGINT NOT NULL,
    land_area DECIMAL(10,2) NOT NULL,
    building_area DECIMAL(10,2) NOT NULL,
    bedrooms INT DEFAULT 0,
    bathrooms INT DEFAULT 0,
    floors INT DEFAULT 1,
    certificate VARCHAR(50),
    condition_property VARCHAR(50),
    facing VARCHAR(50),
    water_source VARCHAR(50),
    internet ENUM('Ya','Tidak') DEFAULT 'Tidak',
    hook ENUM('Ya','Tidak') DEFAULT 'Tidak',
    power INT DEFAULT 0,
    dining_room VARCHAR(50),
    living_room VARCHAR(50),
    road_width VARCHAR(50),
    furnished VARCHAR(50),
    description TEXT,
    status ENUM('aktif','tidak_aktif') DEFAULT 'aktif',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);
```

## Model Classes yang Ditambahkan

### PropertiTanah
- Mengelola data properti tanah saja
- Methods: get_all(), get_by_id(), save(), delete(), to_dict()

### PropertiTanahBangunan  
- Mengelola data properti tanah + bangunan
- Methods: get_all(), get_by_id(), save(), delete(), to_dict()

## API Endpoints yang Diupdate

### Public API
- `/api/properties` - Mendukung filter `property_type` ('tanah' atau 'tanah_bangunan')

### Admin API (CRUD)
- `GET /api/admin/properties` - List semua properti dengan pagination
- `POST /api/admin/property` - Create properti baru
- `PUT /api/admin/property/<type>/<id>` - Update properti
- `DELETE /api/admin/property/<type>/<id>` - Delete properti  
- `GET /api/admin/property/<type>/<id>` - Get detail properti

## Fitur Baru

### Dashboard Statistics
- Total properti dari kedua tabel
- Hitung rata-rata harga gabungan
- Jumlah lokasi unik
- Breakdown: jumlah properti tanah vs tanah+bangunan

### CRUD Operations
- Form input otomatis menyesuaikan berdasarkan jenis properti
- Field khusus bangunan hanya muncul untuk properti tanah+bangunan
- Validasi sesuai jenis properti

## Data Sample
File `db_KP_updated.sql` berisi:
- 3 contoh properti tanah
- 4 contoh properti tanah+bangunan
- User admin default

## Cara Menggunakan
1. Import `db_KP_updated.sql` ke database MySQL
2. Jalankan aplikasi Flask
3. Login sebagai admin (admin@telkom.co.id / admin123)
4. Akses menu "Manajemen Data Aset" untuk CRUD operations

## Breaking Changes
- Tabel `properties` lama akan dihapus otomatis
- API responses sekarang menyertakan field `property_type`
- Frontend perlu disesuaikan untuk handle 2 jenis properti

## Migration Notes
- Backup data lama sebelum menjalankan update
- Re-train ML models dengan data baru jika diperlukan
- Update frontend JavaScript untuk handle API changes
