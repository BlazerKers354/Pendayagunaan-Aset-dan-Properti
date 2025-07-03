# Panduan Setup Database di XAMPP

## 🚀 Langkah-langkah Setup

### 1. Persiapan XAMPP
```bash
1. Buka XAMPP Control Panel
2. Start Apache dan MySQL services
3. Klik "Admin" pada MySQL untuk membuka phpMyAdmin
```

### 2. Setup Database
```sql
-- Di phpMyAdmin, jalankan query berikut:

-- Buat database
CREATE DATABASE IF NOT EXISTS `db_kp` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_general_ci;

-- Gunakan database
USE `db_kp`;

-- Import file db_KP.sql atau jalankan query berikut:
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','pengguna') NOT NULL DEFAULT 'pengguna',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert admin user
INSERT INTO `users` VALUES 
(1,'Administrator','admin@telkom.co.id','pbkdf2:sha256:600000$KvdIFquH8tgupXs3$cdbe17684980c07ca70b9edff6db949969e53618b01b6cffcae03259df080706','admin');
```

### 3. Konfigurasi Environment
Update file `.env` sesuai konfigurasi XAMPP:
```env
# Flask Configuration
SECRET_KEY=telkom-dashboard-secret-key-2024
FLASK_DEBUG=True

# Database Configuration (XAMPP Default)
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=db_kp
MYSQL_PORT=3306

# Development Settings
FLASK_ENV=development
```

### 4. Menjalankan Aplikasi
```bash
# Pastikan virtual environment aktif
cd "path/to/project"
python run.py
```

### 5. Login Admin
```
URL: http://127.0.0.1:5000
Email: admin@telkom.co.id
Password: admin123
```

## 🔧 Troubleshooting

### Jika Login Gagal:
1. **Jalankan script setup admin:**
   ```bash
   python setup_admin.py
   ```

2. **Periksa koneksi database:**
   - Pastikan MySQL service running di XAMPP
   - Cek username/password di phpMySQL
   - Verifikasi nama database `db_kp` sudah dibuat

3. **Reset password admin:**
   ```sql
   -- Di phpMyAdmin, jalankan:
   UPDATE users 
   SET password = 'pbkdf2:sha256:600000$KvdIFquH8tgupXs3$cdbe17684980c07ca70b9edff6db949969e53618b01b6cffcae03259df080706' 
   WHERE email = 'admin@telkom.co.id';
   ```

### Jika Database Error:
1. **Buat database manual:**
   ```sql
   CREATE DATABASE db_kp CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   ```

2. **Import file SQL:**
   - Upload `db_KP.sql` melalui phpMyAdmin
   - Atau copy-paste isi file ke SQL tab

3. **Cek tabel users:**
   ```sql
   SELECT * FROM users WHERE role = 'admin';
   ```

## ✅ Verifikasi Setup

### Database berhasil jika:
- Database `db_kp` muncul di phpMyAdmin
- Tabel `users` memiliki 1 record admin
- Aplikasi Flask bisa connect ke MySQL

### Login berhasil jika:
- Form login menerima email: `admin@telkom.co.id`
- Password: `admin123` diterima
- Redirect ke dashboard admin

---

**Status:** ✅ **Setup Complete**  
**Admin Account:** admin@telkom.co.id / admin123  
**Database:** MySQL via XAMPP
