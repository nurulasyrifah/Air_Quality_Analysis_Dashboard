import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

# --- Setup ---
st.set_page_config(page_title="🌫️ Air Quality Dashboard", layout="wide")
st.markdown(
    """
    <style>
    .big-font {
        font-size:32px !important;
        font-weight:600;
    }
    .section-title {
        font-size:24px !important;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight:600;
        border-bottom: 2px solid #ddd;
    }
    .copyright {
        font-size: 14px;
        color: gray;
        margin-top: 3rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Load Data ---
import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "all_data_cleaned.csv")
    df = pd.read_csv(file_path, parse_dates=['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['month'] = df['datetime'].dt.month
    return df

data = load_data()

# --- Judul Utama ---
st.markdown('<p class="big-font">Air Quality Analysis Dashboard</p>', unsafe_allow_html=True)
st.markdown("*Visualisasi interaktif untuk memahami pola polusi udara berdasarkan waktu dan lokasi stasiun.*")

# --- Tabs Layout ---
tab1, tab2 = st.tabs(["📊 Analisis Waktu", "🗺️ Analisis Geospasial"])

# Tab 1: Analisis Waktu
with tab1:
    st.markdown('<p class="section-title">📈 Polusi Udara Berdasarkan Waktu</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Grafik per jam
    with col1:
        st.subheader("Polusi PM2.5 per Jam")
        hourly_avg = data.groupby(['hour', 'station'])['PM2.5'].mean().reset_index()
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=hourly_avg, x="hour", y="PM2.5", hue="station", ax=ax1)
        ax1.set_title("Rata-rata PM2.5 Harian")
        ax1.set_xlabel("Jam")
        ax1.set_ylabel("PM2.5")
        ax1.legend(title="Stasiun", fontsize=8)
        st.pyplot(fig1)

    # Grafik per bulan
    with col2:
        st.subheader("Polusi PM2.5 per Bulan")
        monthly_avg = data.groupby(['month', 'station'])['PM2.5'].mean().reset_index()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=monthly_avg, x="month", y="PM2.5", hue="station", ax=ax2)
        ax2.set_title("Rata-rata PM2.5 Tahunan")
        ax2.set_xlabel("Bulan")
        ax2.set_ylabel("PM2.5")
        ax2.legend(title="Stasiun", fontsize=8)
        st.pyplot(fig2)

    bullets = [
        "Aktivitas outdoor terbaik antara jam 6 hingga 8 pagi",
        "Polusi tinggi pada bulan Desember dan Januari",
    ]

    st.markdown("### Rekomendasi berdasarkan analisis pola waktu dan musim:")
    for item in bullets:
        st.markdown(f"* {item}")

# Tab 2: Peta Persebaran Polusi
with tab2:
    st.markdown('<h3 style="color:#444;">🗺️ Peta Persebaran Polusi PM2.5</h3>', unsafe_allow_html=True)

    station_coords = {
        "Gucheng": [39.9376, 116.3498],
        "Changping": [40.218, 116.231],
        "Dingling": [40.290, 116.225],
        "Dongsi": [39.9296, 116.4177],
        "Nongzhanguan": [39.9335, 116.4610],
        "Aotizhongxin": [39.9826, 116.3925],
        'Guanyuan': [39.929, 116.339],
        "Huairou": [40.3170, 116.6318],
        "Shunyi": [40.125, 116.655],
        "Tiantan": [39.873, 116.413],
        "Wanliu": [39.999, 116.305],
        "Wanshouxigong": [39.879, 116.352]
    }

    station_coords_df = pd.DataFrame.from_dict(
        station_coords, orient='index', columns=['latitude', 'longitude']
    ).reset_index().rename(columns={'index': 'station'})

    avg_pm25 = data.groupby("station")["PM2.5"].mean().reset_index(name="avg_PM2.5")
    map_data = pd.merge(station_coords_df, avg_pm25, on="station", how="inner")

    m = folium.Map(location=[39.9, 116.4], zoom_start=10)

    for _, row in map_data.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=8,
            popup=f"{row['station']}: {row['avg_PM2.5']:.1f} µg/m³",
            color="red" if row['avg_PM2.5'] > 15 else "green",
            fill=True,
            fill_color="red" if row['avg_PM2.5'] > 15 else "green",
            fill_opacity=0.7
        ).add_to(m)

    folium_static(m, width=1000, height=500)

    with st.container():
        st.markdown("## Rekomendasi Kebijakan untuk Lokasi Polusi Tinggi")

        st.markdown("""
        Tiga stasiun menunjukkan rata-rata polusi udara PM2.5 yang paling tinggi dan sering melewati ambang batas aman:
        - **Dongsi**
        - **Wanshouxigong**
        - **Nongzhanguan**

        🛑 **Ambang batas WHO untuk PM2.5 adalah 15 µg/m³** (rata-rata tahunan). Ketiga stasiun ini menunjukkan nilai rata-rata melebihi batas tersebut.
        """)

        st.markdown("### 📌 Rekomendasi Tindakan Mitigasi:")

        rekomendasi = [
            "Pemantauan intensif dengan pemasangan sensor kualitas udara real-time untuk mengidentifikasi lonjakan secara langsung.",
            "Batasi lalu lintas kendaraan berbahan bakar fosil pada jam padat di area tersebut.",
            "Tingkatkan pemantauan emisi dari industri sekitar (jika ada).",
            "Penanaman pohon penyerap polutan seperti *Ficus benjamina*, *Tabebuia*, dan *Sikas*.",
            "Uji coba implementasi Low Emission Zone di kawasan padat lalu lintas di sekitar ketiga stasiun."
        ]

        for item in rekomendasi:
            st.markdown(f"- {item}")

# Copyright
st.markdown('<p class="copyright">© Nurul Asyrifah. All rights reserved.</p>', unsafe_allow_html=True)
