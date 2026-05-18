import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

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
st.markdown("Dashboard ini menganalisis data penyewaan sepeda berdasarkan musim dan jam menggunakan 1 dataset yang sudah terintegrasi.")

st.divider()

st.header("Pertumbuhan Jumlah Penyewa Sepeda (2011 vs 2012) Berdasarkan Musim")

season_yr_df = df.groupby(['year_label', 'season_label'])['cnt_hour'].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=season_yr_df, 
    x='season_label', 
    y='cnt_hour', 
    hue='year_label', 
    palette='Set2', 
    ax=ax1,]
)
ax1.set_title("Total Penyewaan Sepeda per Musim (2011 vs 2012)")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Penyewaan")
ax1.legend(title="Tahun")
st.pyplot(fig1)

st.info("**Dapat dilihat bahwa ada perkembangan signifikan dari tahun 2011 ke 2012. Sesuai dengan trendnya juga, total penyewaan tertinggi terdapat pada musim gugur")

st.divider()


st.header("Puncak Permintaan Penyewaan Sepeda per Jam")

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

peak_hour = hourly_demand.loc[hourly_demand['cnt_hour'].idxmax()]
ax2.axvline(x=peak_hour['hr'], color='r', linestyle='--', label=f'Puncak: Jam {int(peak_hour["hr"])}:00')
ax2.legend()

st.pyplot(fig2)

st.info(f"**Kesimpulan Visualisasi 2:** Demand penyewaan sepeda mencapai titik tertingginya pada **jam {int(peak_hour['hr'])}:00** (sore hari). Ini menunjukkan bahwa mayoritas orang menyewa sepeda setelah selesai beraktivitas.")
