import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

@st.cache_data
def load_data():
    # Streamlit akan mencoba mencari file main_data.csv di beberapa lokasi umum di repo Anda
    try:
        # Kemungkinan 1: Jika file ada di folder utama (root) repo
        df = pd.read_csv("main_data.csv")
    except FileNotFoundError:
        try:
            # Kemungkinan 2: Jika file ada di dalam folder 'dashboard'
            df = pd.read_csv("dashboard/main+data.csv")
        except FileNotFoundError:
            # Kemungkinan 3: Mengambil langsung dari URL GitHub sebagai jalan terakhir
            url = "https://raw.githubusercontent.com/jmn-cdcc185d6y2746/analisa-data/main/main_data.csv"
            df = pd.read_csv(url)
    
    # PERBAIKAN GRAFIK 1: Memastikan year_label dibaca sebagai teks (String)
    if 'year_label' in df.columns:
        df['year_label'] = df['year_label'].astype(str)
        
    return df

df = load_data()

st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown("Dashboard ini menganalisis data penyewaan sepeda berdasarkan musim dan jam menggunakan 1 dataset yang sudah terintegrasi.")

st.divider()

# ---------------------------------------------------------------------
# Pertanyaan 1: Pertumbuhan berdasarkan Musim (2011 vs 2012)
# ---------------------------------------------------------------------
st.header("1. Pertumbuhan Jumlah Penyewa Sepeda (2011 vs 2012) Berdasarkan Musim")

# Agregasi data (menggunakan cnt_hour)
season_yr_df = df.groupby(['year_label', 'season_label'])['cnt_hour'].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=season_yr_df, 
    x='season_label', 
    y='cnt_hour', 
    hue='year_label', 
    palette='Set2', 
    ax=ax1,
    order=['Spring', 'Summer', 'Fall', 'Winter']
)
ax1.set_title("Total Penyewaan Sepeda per Musim (2011 vs 2012)")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Penyewaan")
ax1.legend(title="Tahun")
st.pyplot(fig1)

st.info("**Kesimpulan Visualisasi 1:** Terdapat pertumbuhan positif yang signifikan pada jumlah penyewa sepeda dari tahun 2011 ke 2012 di semua musim. Musim gugur (Fall) mencatatkan angka penyewaan tertinggi.")

st.divider()

# ---------------------------------------------------------------------
# Pertanyaan 2: Titik Puncak Demand Berdasarkan Jam
# ---------------------------------------------------------------------
st.header("2. Puncak Permintaan Penyewaan Sepeda per Jam")

# Kolom jam bernama 'hr', dan total penyewaan ada di 'cnt_hour'
hourly_demand = df.groupby('hr')['cnt_hour'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=hourly_demand, 
    x='hr', 
    y='cnt_hour', 
    marker='o', 
    color='b', 
    linewidth=2.5,
    ax=ax2
)
ax2.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam (0-23)")
ax2.set_xlabel("Jam (00:00 - 23:00)")
ax2.set_ylabel("Rata-rata Penyewaan (Demand)")
ax2.set_xticks(range(0, 24))
ax2.grid(True, linestyle='--', alpha=0.6)

# Menandai titik puncak
peak_hour = hourly_demand.loc[hourly_demand['cnt_hour'].idxmax()]
ax2.axvline(x=peak_hour['hr'], color='r', linestyle='--', label=f'Puncak: Jam {int(peak_hour["hr"])}')
ax2.legend()

st.pyplot(fig2)

st.info(f"**Kesimpulan Visualisasi 2:** Demand penyewaan sepeda mencapai titik tertingginya pada **jam {int(peak_hour['hr'])}:00** (sore hari). Ini menunjukkan bahwa mayoritas orang menyewa sepeda setelah selesai beraktivitas.")
