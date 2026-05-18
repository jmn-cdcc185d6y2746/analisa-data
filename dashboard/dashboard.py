import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# 1. Memuat 1 Dataset (Merged CSV)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("main_data.csv")
    except FileNotFoundError:
        try:
            df = pd.read_csv("dashboard/main_data.csv")
        except FileNotFoundError:
            url = "https://raw.githubusercontent.com/jmn-cdcc185d6y2746/analisa-data/main/main_data.csv"
            df = pd.read_csv(url)
    
    if 'year_label' in df.columns:
        df['year_label'] = df['year_label'].astype(str)
        
    return df

df = load_data()

st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown("Dashboard ini menganalisis data penyewaan sepeda berdasarkan musim dan jam.")

# --- FITUR DEBUGGING ---
# Anda bisa mengeklik tombol ini di web Anda untuk melihat isi asli file main_data.csv
with st.expander("🛠️ Klik di sini untuk Debugging (Cek Isi Data)"):
    st.write("**Daftar Kolom yang tersedia di file Anda:**", df.columns.tolist())
    st.write("**5 Baris Pertama Data Anda:**")
    st.dataframe(df.head())

st.divider()

# ---------------------------------------------------------------------
# Pertanyaan 1: Pertumbuhan berdasarkan Musim (2011 vs 2012)
# ---------------------------------------------------------------------
st.header("1. Pertumbuhan Jumlah Penyewa Sepeda (2011 vs 2012) Berdasarkan Musim")

# Auto-detect kolom total penyewaan (cnt)
cnt_col = 'cnt_hour' if 'cnt_hour' in df.columns else 'cnt' if 'cnt' in df.columns else None

if cnt_col and 'year_label' in df.columns and 'season_label' in df.columns:
    season_yr_df = df.groupby(['year_label', 'season_label'])[cnt_col].sum().reset_index()

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=season_yr_df, 
        x='season_label', 
        y=cnt_col, 
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
else:
    st.error("⚠️ Gagal memuat grafik 1: Pastikan data Anda memiliki kolom `year_label`, `season_label`, dan `cnt_hour`.")

st.divider()

# ---------------------------------------------------------------------
# Pertanyaan 2: Titik Puncak Demand Berdasarkan Jam
# ---------------------------------------------------------------------
st.header("2. Puncak Permintaan Penyewaan Sepeda per Jam")

# Auto-detect kolom jam (hr)
hr_col = None
for col_name in ['hr', 'hr_hour', 'hr_x', 'hour']:
    if col_name in df.columns:
        hr_col = col_name
        break

# Jika kolom jam ditemukan, buat grafik. Jika tidak, tampilkan peringatan.
if hr_col and cnt_col:
    hourly_demand = df.groupby(hr_col)[cnt_col].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=hourly_demand, 
        x=hr_col, 
        y=cnt_col, 
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
    peak_hour = hourly_demand.loc[hourly_demand[cnt_col].idxmax()]
    ax2.axvline(x=peak_hour[hr_col], color='r', linestyle='--', label=f'Puncak: Jam {int(peak_hour[hr_col])}')
    ax2.legend()

    st.pyplot(fig2)
    
    st.info(f"**Kesimpulan Visualisasi 2:** Demand penyewaan sepeda mencapai titik tertingginya pada **jam {int(peak_hour[hr_col])}:00** (sore hari). Ini menunjukkan bahwa mayoritas orang menyewa sepeda setelah selesai beraktivitas.")

else:
    st.error(f"⚠️ **Grafik 2 Tidak Dapat Ditampilkan** ⚠️\n\n"
             f"Kolom jam tidak ditemukan di file `main_data.csv` Anda. "
             f"Silakan buka menu drop-down **'🛠️ Debugging'** di bagian atas halaman ini untuk melihat kolom apa saja yang Anda miliki. "
             f"Kemungkinan besar file CSV yang Anda unggah saat ini bukan gabungan dataset yang tepat, atau Anda tidak sengaja mengunggah file `day.csv`.")
