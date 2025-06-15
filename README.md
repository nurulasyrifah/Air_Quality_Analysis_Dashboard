# Air Quality Analysis Dashboard

Proyek ini bertujuan untuk menganalisis dan memvisualisasikan data polusi udara (PM2.5) dari berbagai stasiun monitoring menggunakan Python dan Streamlit. Dashboard interaktif ini membantu mengidentifikasi pola polusi berdasarkan waktu dan lokasi, serta merekomendasikan kebijakan berbasis data.

---

## Struktur Direktori

```
Air-Quality-Analysis/
│
├── air_quality_analysis.ipynb     # Notebook eksplorasi awal
│
├── dashboard/                     # Folder utama Streamlit App
│   ├── all_data_cleaned.csv       # Dataset hasil cleaning
│   └── dashboard.py               # File utama dashboard
│
├── dataset/                       # Folder dataset mentah
│                                    sebelum preprocessing
│
├── env/                           # Lingkungan virtual environment
│
├── requirements.txt               # Dependensi Python
│
└── README.md                      # Dokumentasi proyek
```

---

## Cara Menjalankan Dashboard

### 1. **Clone Repository**

```bash
git clone https://github.com/username/Air-Quality-Analysis.git
cd Air-Quality-Analysis/dashboard
```

### 2. **Buat Virtual Environment (opsional)**

```bash
python -m venv env
source env/bin/activate      # Mac/Linux
env\Scripts\activate       # Windows
```

### 3. **Install Dependensi**

```bash
pip install -r requirements.txt
```

### 4. **Jalankan Streamlit App**

```bash
streamlit run dashboard.py
```

---

## Dependensi Utama

- `streamlit`
- `pandas`
- `matplotlib`
- `seaborn`
- `folium`
- `streamlit-folium`

---

## Kontak

Dikembangkan oleh **Nurul Asyrifah**  
📧 [nu.asyrifah@gmail.com]  
📍 Indonesia

---

© 2025 Nurul Asyrifah. All rights reserved.
