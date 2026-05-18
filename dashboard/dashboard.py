import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Interaktif Dashboard Penyewaan Sepeda", layout="wide")

# 1. Memuat Dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("main_data.csv")
    except FileNotFoundError:
        url = "https://raw.githubusercontent.com/jmn-cdcc185d6y2746/analisa-data/main/main_data.csv"
        df = pd.read_csv(url)
    
    # Konversi dteday ke datetime agar bisa difilter kalender
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Memastikan year_label adalah string agar warna plot konsisten
    if 'year_label' in df.columns:
        df['year_label'] = df['year_label'].astype(str)
        
    return df

df = load_data()

# ======================================================================
# SIDEBAR SETUP
# ======================================================================
st.sidebar.image("https://img.icons8.com/plasticine/100/000000/bicycle.png")
st.sidebar.title("Filter Data")

# Filter 1: Kalender untuk Visualisasi Pertama
st.sidebar.subheader("Filter Rentang Tanggal")
min_date = df['dteday'].min().to_pydatetime()
max_date = df['dteday'].max().to_pydatetime()

start_date, end_date = st.sidebar.date_input(
    label='Pilih Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter 2: Slider Waktu untuk Visualisasi Kedua
st.sidebar.subheader("Filter Rentang Jam")
hour_range = st.sidebar.slider(
    "Pilih Jam (Format 24 Jam):",
    min_value=0,
    max_value=23,
    value=(0, 23) # Default rentang dari jam 0 sampai 23
)

# ======================================================================
# MAIN PAGE
# ======================================================================
st.title("🚲 Dashboard Interaktif Penyewaan Sepeda")
st.markdown(f"Menampilkan data dari **{start_date}** sampai **{end_date}**")

# Memproses Filter Tanggal
main_df_filtered = df[(df["dteday"] >= str(start_date)) & 
                       (df["dteday"] <= str(end_date))]

# ---------------------------------------------------------------------
# Visualisasi 1: Pertumbuhan berdasarkan Musim
# ---------------------------------------------------------------------
st.header("1. Pertumbuhan Penyewa Sepeda Berdasarkan Musim")

if not main_df_filtered.empty:
    season_yr_df = main_df_filtered.groupby(['year_label', 'season_label'])['cnt_hour'].sum().reset_index()

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=season_yr_df, 
        x='season_label', 
        y='cnt_hour', 
        hue='year_label', 
        palette='viridis', 
        ax=ax1,
        order=['Spring', 'Summer', 'Fall', 'Winter']
    )
    ax1.set_title(f"Total Penyewaan: {start_date} s/d {end_date}")
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Total Penyewaan")
    st.pyplot(fig1)
else:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")

st.divider()

# ---------------------------------------------------------------------
# Visualisasi 2: Puncak Demand Berdasarkan Jam
# ---------------------------------------------------------------------
st.header("2. Tren Permintaan Sepeda Berdasarkan Jam")

# Memproses Filter Jam (Slider)
# Filter diterapkan pada dataset asli (df) agar tren jam tetap terlihat stabil 
# namun user bisa melakukan zoom-in ke jam tertentu.
hourly_df_filtered = df[(df["hr"] >= hour_range[0]) & (df["hr"] <= hour_range[1])]

if not hourly_df_filtered.empty:
    hourly_demand = hourly_df_filtered.groupby('hr')['cnt_hour'].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=hourly_demand, 
        x='hr', 
        y='cnt_hour', 
        marker='o', 
        color='#E67E22', 
        linewidth=3,
        ax=ax2
    )
    ax2.set_title(f"Rata-rata Demand Jam {hour_range[0]}:00 sampai {hour_range[1]}:00")
    ax2.set_xlabel("Jam (24 Jam)")
    ax2.set_ylabel("Rata-rata Penyewaan")
    ax2.set_xticks(range(hour_range[0], hour_range[1] + 1))
    ax2.grid(True, alpha=0.3)

    # Menandai titik puncak di dalam rentang yang dipilih
    peak_val = hourly_demand.loc[hourly_demand['cnt_hour'].idxmax()]
    ax2.axvline(x=peak_val['hr'], color='red', linestyle='--', label=f"Puncak: Jam {int(peak_val['hr'])}")
    ax2.legend()
    
    st.pyplot(fig2)
    st.caption(f"Menampilkan statistik demand untuk rentang waktu jam {hour_range[0]}:00 hingga {hour_range[1]}:00.")
else:
    st.error("Data jam tidak ditemukan.")

st.sidebar.markdown("---")
st.sidebar.info("Gunakan filter di atas untuk menyesuaikan tampilan grafik secara otomatis.")
