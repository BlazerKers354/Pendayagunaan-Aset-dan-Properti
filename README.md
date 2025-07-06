# Sistem Prediksi Harga Properti Telkom

Sistem web berbasis Flask untuk prediksi harga properti (tanah dan bangunan) menggunakan machine learning dengan antarmuka admin dan user yang terpisah.

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Struktur Proyek](#-struktur-proyek)
- [Teknologi](#-teknologi)
- [Instalasi](#-instalasi)
- [Penggunaan](#-penggunaan)
- [API Endpoints](#-api-endpoints)
- [Model Machine Learning](#-model-machine-learning)
- [Database](#-database)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

## 🚀 Fitur Utama

### Dashboard Admin
- **Manajemen Data**: CRUD data properti tanah dan bangunan
- **Analytics**: Visualisasi data menggunakan Chart.js
- **Export Data**: Download data dalam format CSV/Excel
- **User Management**: Kelola akses pengguna
- **Report Generation**: Generate laporan komprehensif

### Dashboard User
- **Prediksi Harga**: Input data properti untuk prediksi harga
- **Riwayat Prediksi**: Lihat hasil prediksi sebelumnya
- **Visualisasi**: Grafik dan chart hasil prediksi
- **Profile Management**: Kelola profil pengguna

### Sistem Prediksi
- **Multiple Models**: CatBoost, XGBoost, Random Forest
- **Real-time Prediction**: Prediksi instan
- **Model Comparison**: Perbandingan akurasi model
- **Feature Engineering**: Preprocessing otomatis

## 📁 Struktur Proyek

```
project_KP/
├── app/                          # Aplikasi Flask utama
│   ├── __init__.py              # Inisialisasi aplikasi
│   ├── routes.py                # Route handlers
│   ├── models.py                # Database models
│   ├── database.py              # Konfigurasi database
│   ├── data_processor.py        # Preprocessing data
│   ├── prediction_models.py     # Model ML
│   ├── static/                  # File statis (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/               # Template HTML
├── data/                        # Dataset
│   └── raw/                     # Data mentah
├── ml_model/                    # Model tersimpan
│   ├── catboost_model.pkl
│   ├── xgboost_model.pkl
│   ├── random_forest_model.pkl
│   └── model_comparison.csv
├── notebooks/                   # Jupyter notebooks
├── instance/                    # Database files
├── docs/                        # Dokumentasi
├── archive/                     # File backup
├── config.py                    # Konfigurasi aplikasi
├── run.py                       # Entry point aplikasi
└── requirements.txt             # Dependencies
```

## 🛠 Teknologi

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM database
- **SQLite**: Database
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing

### Machine Learning
- **CatBoost**: Gradient boosting
- **XGBoost**: Extreme gradient boosting
- **Scikit-learn**: Random Forest & preprocessing
- **Joblib**: Model serialization

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling (Bootstrap 5)
- **JavaScript**: Interaktivitas
- **Chart.js**: Visualisasi data
- **jQuery**: DOM manipulation

### Development
- **Python 3.8+**: Programming language
- **Jupyter**: Data analysis
- **Git**: Version control

## 💻 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/username/project_KP.git
cd project_KP
```

### 2. Buat Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 5. Setup Environment Variables
Buat file `.env`:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/telkom_assets.db
FLASK_ENV=development
```

### 6. Jalankan Aplikasi
```bash
python run.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## 📖 Penggunaan

### Login Sistem
- **Admin**: Akses penuh ke semua fitur
- **User**: Akses terbatas untuk prediksi

### Input Data Properti
1. Pilih jenis properti (Tanah/Bangunan)
2. Isi form dengan data properti
3. Submit untuk mendapat prediksi

### Kelola Data (Admin)
1. Login sebagai admin
2. Navigasi ke "Manajemen Data"
3. Tambah, edit, atau hapus data

## 🔌 API Endpoints

### Authentication
```http
POST /login          # Login user
POST /register       # Register user baru
POST /logout         # Logout user
```

### Dashboard
```http
GET /dashboard_admin # Dashboard admin
GET /dashboard_user  # Dashboard user
```

### Data Management
```http
GET /data                    # Tampil data
POST /add_data_tanah        # Tambah data tanah
POST /add_data_bangunan     # Tambah data bangunan
PUT /edit_data/<id>         # Edit data
DELETE /delete_data/<id>    # Hapus data
```

### Predictions
```http
POST /predict_tanah         # Prediksi harga tanah
POST /predict_bangunan      # Prediksi harga bangunan
GET /prediction_history     # Riwayat prediksi
```

### Visualizations
```http
GET /visualization          # Halaman visualisasi
GET /api/chart_data        # Data untuk chart
```

## 🤖 Model Machine Learning

### Model yang Digunakan
1. **CatBoost Regressor**
   - Optimal untuk categorical features
   - Handling missing values otomatis
   - Akurasi tinggi

2. **XGBoost Regressor**
   - Gradient boosting yang cepat
   - Regularization built-in
   - Feature importance

3. **Random Forest Regressor**
   - Ensemble method
   - Robust terhadap outliers
   - Interpretable

### Feature Engineering
- **Scaling**: StandardScaler untuk numerical features
- **Encoding**: LabelEncoder untuk categorical features
- **Missing Values**: Imputation dengan median/mode
- **Feature Selection**: Berdasarkan importance

### Evaluasi Model
- **Metrics**: MAE, MSE, RMSE, R²
- **Cross Validation**: 5-fold CV
- **Model Comparison**: Automatic best model selection

## 🗄 Database

### Schema Utama

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tanah Table
```sql
CREATE TABLE tanah (
    id INTEGER PRIMARY KEY,
    lokasi VARCHAR(200) NOT NULL,
    luas_tanah FLOAT NOT NULL,
    harga_per_m2 FLOAT NOT NULL,
    total_harga FLOAT NOT NULL,
    koordinat_x FLOAT,
    koordinat_y FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Bangunan Table
```sql
CREATE TABLE bangunan (
    id INTEGER PRIMARY KEY,
    lokasi VARCHAR(200) NOT NULL,
    luas_tanah FLOAT NOT NULL,
    luas_bangunan FLOAT NOT NULL,
    jumlah_lantai INTEGER,
    tahun_bangun INTEGER,
    kondisi VARCHAR(50),
    harga_total FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🤝 Kontribusi

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Coding Standards
- PEP 8 untuk Python
- ESLint untuk JavaScript
- Meaningful commit messages
- Comprehensive testing

## 📜 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Kontak

**Developer Team**
- Email: developer@telkom.co.id
- Project Link: [https://github.com/username/project_KP](https://github.com/username/project_KP)

## 🙏 Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [CatBoost Documentation](https://catboost.ai/docs/)
- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- Telkom Indonesia untuk dukungan proyek

---

## 📊 Status Proyek

- ✅ **Core Features**: Completed
- ✅ **Authentication**: Implemented
- ✅ **ML Models**: Trained & Deployed
- ✅ **UI/UX**: Responsive Design
- 🚧 **API Documentation**: In Progress
- 🚧 **Unit Testing**: In Progress
- 📋 **Deployment**: Planned

**Last Updated**: 06 Juli 2025
