# 🚲 Bike Sharing Dashboard

Dashboard analisis data interaktif untuk dataset **Capital Bikeshare** (2011–2012), dibuat sebagai proyek akhir kursus **Belajar Analisis Data dengan Python** – Dicoding Indonesia.

---

## 📋 Deskripsi Proyek

Dashboard ini menganalisis pola peminjaman sepeda berdasarkan tiga pertanyaan bisnis utama:

1. **Bagaimana tren peminjaman sepeda dari waktu ke waktu?**
2. **Bagaimana musim dan kondisi cuaca memengaruhi jumlah peminjaman?**
3. **Bagaimana pola peminjaman antara pengguna kasual vs pengguna terdaftar?**

---

## 🗂️ Struktur Folder

```
submission/
├── dashboard/
│   ├── main_data.csv        ← Data utama yang digunakan dashboard
│   └── dashboard.py         ← Aplikasi Streamlit
├── data/
│   ├── day.csv              ← Dataset harian (raw)
│   └── hour.csv             ← Dataset per jam (raw)
├── notebook.ipynb           ← Notebook analisis lengkap
├── README.md                ← File ini
├── requirements.txt         ← Daftar library yang dibutuhkan
└── url.txt                  ← URL deployment (Streamlit Cloud)
```

---

## ⚙️ Cara Menjalankan Dashboard Secara Lokal

### 1. Prasyarat
Pastikan Anda sudah menginstal **Python 3.9+** di komputer. Cek dengan:
```bash
python --version
```

### 2. Clone / Unduh Proyek
Unduh atau clone seluruh folder `submission/` ke komputer Anda.

### 3. Buat Virtual Environment (Direkomendasikan)
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate

# Aktifkan (macOS/Linux)
source venv/bin/activate
```

### 4. Instal Dependensi
Dari dalam folder `submission/`, jalankan:
```bash
pip install -r requirements.txt
```

### 5. Jalankan Dashboard
Pastikan Anda berada di dalam folder `submission/`, lalu jalankan:
```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan otomatis terbuka di browser pada alamat:
```
http://localhost:8501
```

---

## 🎛️ Fitur Dashboard

| Fitur | Deskripsi |
|---|---|
| **Filter Tanggal** | Pilih rentang periode analisis (Jan 2011 – Des 2012) |
| **Filter Musim** | Filter berdasarkan Springer, Summer, Fall, Winter |
| **Filter Cuaca** | Filter berdasarkan kondisi cuaca |
| **Filter Jenis Hari** | Pilih antara Hari Kerja, Hari Libur, atau Semua |
| **Tab Tren Waktu** | Grafik tren harian, rata-rata bulanan, perbandingan 2011 vs 2012 |
| **Tab Musim & Cuaca** | Bar chart musim, bar chart cuaca, heatmap musim×cuaca |
| **Tab Pola Pengguna** | Pie chart proporsi, bar chart per hari, stacked area bulanan |
| **Tab Faktor Lingkungan** | Scatter suhu & kelembaban, matriks korelasi |

---

## 📦 Library yang Digunakan

| Library | Versi | Kegunaan |
|---|---|---|
| `streamlit` | 1.41.1 | Framework dashboard web interaktif |
| `pandas` | 2.2.3 | Manipulasi dan analisis data |
| `numpy` | 1.26.4 | Komputasi numerik |
| `matplotlib` | 3.9.4 | Visualisasi data (chart & plot) |
| `seaborn` | 0.13.2 | Visualisasi statistik (heatmap) |

---

## 🌐 Link Demo (Streamlit Cloud)

Lihat file `url.txt` untuk tautan deployment online dashboard ini.

---

## 👤 Author

**Proyek Analisis Data Dicoding**
Dataset: [Capital Bikeshare System Data](https://capitalbikeshare.com/system-data)
Sumber: UCI Machine Learning Repository
