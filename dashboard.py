import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# ==============================
# 1. PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ==============================
# 2. DATA LOADING FUNCTION
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

main_data = load_data()
daily_data = main_data.drop_duplicates(subset=['dteday']).copy()

# ==============================
# 3. SIDEBAR & FILTERS
# ==============================
st.sidebar.title("🚲 Bike Sharing Analytics")
st.sidebar.markdown("---")

min_date = main_data['dteday'].min()
max_date = main_data['dteday'].max()

st.sidebar.header("Filter Data")
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

filtered_data = main_data[(main_data['dteday'] >= str(start_date)) & 
                          (main_data['dteday'] <= str(end_date))].copy()
filtered_daily = daily_data[(daily_data['dteday'] >= str(start_date)) & 
                            (daily_data['dteday'] <= str(end_date))].copy()

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard by: Calvin Constantine Raharjo")

# ==============================
# 4. MAIN DASHBOARD AREA
# ==============================
st.title("🚲 Bike Sharing Business Dashboard")
st.markdown("Dashboard interaktif ini menyajikan analisis komprehensif berdasarkan 6 pertanyaan bisnis utama.")

st.subheader("Key Performance Indicators (KPI)")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan (Seluruhnya)", value=f"{filtered_data['cnt_hour'].sum():,}")
with col2:
    st.metric("Total Member (Registered)", value=f"{filtered_data['registered_hour'].sum():,}")
with col3:
    st.metric("Total Kasual (Casual)", value=f"{filtered_data['casual_hour'].sum():,}")

st.markdown("---")

# ==============================
# 5. VISUALIZATION & INSIGHTS
# ==============================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Jam Sibuk", 
    "2. Dampak Cuaca", 
    "3. Tren Pertumbuhan", 
    "4. Pengaruh Suhu", 
    "5. Preferensi Hari", 
    "6. Kecepatan Angin"
])

# --- TAB 1: POLA JAM SIBUK ---
with tab1:
    st.header("1. Pola Jam Sibuk: Registered vs Casual")
    st.markdown("**Pertanyaan Bisnis 1:** *Bagaimana perbedaan pola jam sibuk (peak hours) penyewaan sepeda antara pengguna biasa (casual) dan pengguna terdaftar (registered) pada hari kerja (workingday) dibandingkan hari libur (holiday) selama periode tahun 2011-2012?*")
    st.markdown("---")
    
    work_cond = filtered_data['workingday_hour'].isin([1, '1', 'Hari Kerja', 'Working Day'])
    workday_data = filtered_data[work_cond].groupby('hr').agg({'casual_hour': 'mean', 'registered_hour': 'mean'}).reset_index()
    holiday_data = filtered_data[~work_cond].groupby('hr').agg({'casual_hour': 'mean', 'registered_hour': 'mean'}).reset_index()
    
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    fig1.suptitle('Perbandingan Pola Jam Sibuk Penyewaan Sepeda (Casual vs Registered)', fontsize=20, fontweight='bold', y=1.05)
    
    ax1.plot(workday_data['hr'], workday_data['registered_hour'], marker='o', markersize=5, label='Registered (Member)', color='tab:blue')
    ax1.plot(workday_data['hr'], workday_data['casual_hour'], marker='o', markersize=5, label='Casual (Biasa)', color='tab:orange')
    ax1.set_title('Pola Jam Sibuk pada Hari Kerja (Workingday)', fontsize=14, pad=15)
    ax1.set_xlabel('Jam (0-23)', fontsize=12)
    ax1.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax1.set_xticks(range(0, 24))
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()
    
    ax2.plot(holiday_data['hr'], holiday_data['registered_hour'], marker='o', markersize=5, label='Registered (Member)', color='tab:blue')
    ax2.plot(holiday_data['hr'], holiday_data['casual_hour'], marker='o', markersize=5, label='Casual (Biasa)', color='tab:orange')
    ax2.set_title('Pola Jam Sibuk pada Hari Libur (Holiday)', fontsize=14, pad=15)
    ax2.set_xlabel('Jam (0-23)', fontsize=12)
    ax2.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax2.set_xticks(range(0, 24))
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()
    
    st.pyplot(fig1)
    
    # INSIGHTS TAB 1
    st.info("""
    💡 **Insights:**
- **Hari Kerja (Grafik Kiri):** Pengguna terdaftar (Registered) mendominasi secara mutlak dengan membentuk pola bimodal (dua puncak). Puncak aktivitas (peak hours) terjadi pada pukul 08.00 pagi dan rentang pukul 17.00 - 18.00 sore. Hal ini membuktikan bahwa sepeda utamanya digunakan sebagai moda transportasi komuter harian. Di sisi lain, pengguna kasual sangat sepi sepanjang hari.

- **Hari Libur (Grafik Kanan):** Pola bergeser drastis di mana penyewaan oleh pengguna Casual meningkat tajam membentuk kurva lonjakan tunggal di pertengahan hari (pukul 12.00 hingga 15.00 siang). Ini mengonfirmasi bahwa sepeda disewa untuk tujuan rekreasi dan olahraga santai pada akhir pekan, bukan untuk mengejar waktu pagi buta.    """)


# --- TAB 2: DAMPAK CUACA & MUSIM ---
with tab2:
    st.header("2. Dampak Musim dan Kondisi Cuaca")
    st.markdown("**Pertanyaan Bisnis 2:** *Seberapa besar dampak perubahan kondisi cuaca (weathersit) dan musim (season) terhadap persentase penurunan rata-rata total penyewaan sepeda harian (cnt) sepanjang tahun 2011-2012?*")
    st.markdown("---")

    fig2, ax2 = plt.subplots(figsize=(14, 7))
    custom_palette = ['#445480', '#30837b', '#6dbe6e'] 
    season_weather_agg = filtered_daily.groupby(['season_day', 'weathersit_day'])['cnt_day'].mean().reset_index()
    
    sns.barplot(data=season_weather_agg, x='season_day', y='cnt_day', hue='weathersit_day', palette=custom_palette, ax=ax2)
    ax2.set_title('Dampak Musim dan Kondisi Cuaca terhadap Rata-rata Penyewaan Harian', fontsize=16, fontweight='bold', pad=20)
    ax2.set_xlabel('Kategori Musim', fontsize=12, labelpad=10)
    ax2.set_ylabel('Rata-rata Penyewaan Harian', fontsize=12, labelpad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.6)
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%.0f', padding=5)
    ax2.legend(title='Kondisi Cuaca', bbox_to_anchor=(1.01, 1), loc='upper left')
    st.pyplot(fig2)
    
    # INSIGHTS TAB 2
    st.info("""
    💡 **Insights:**
- **Titik Puncak (Peak Performance):** Rata-rata penyewaan tertinggi terjadi pada musim gugur (Fall) saat cuaca cerah (Clear/Partly Cloudy), mencapai angka **5.878** penyewaan per hari. Suhu yang sejuk dipadu langit cerah menjadi kondisi paling ideal bagi pesepeda.

- **Titik Terendah (Lowest Performance):** Rata-rata penyewaan terendah tercatat pada musim semi (Springer) ketika terjadi hujan/salju ringan (Light Snow/Rain), yang hanya menyentuh angka **935** penyewaan per hari.

- **Persentase Penurunan Ekstrem:** Terjadi penurunan drastis sekitar **84%** dari titik performa terbaik (5.878) ke titik terburuknya (935). Hal ini membuktikan bahwa faktor presipitasi (hujan/salju) dan suhu dingin ekstrem adalah variabel friksi terkuat yang mampu mematikan hampir seluruh minat sewa pelanggan.    """)


# --- TAB 3: TREN PERTUMBUHAN BULANAN ---
with tab3:
    st.header("3. Tren Pertumbuhan Bulanan")
    st.markdown("**Pertanyaan Bisnis 3:** *Bagaimana tingkat pertumbuhan rata-rata penyewaan sepeda bulanan (Month-over-Month) pada tahun 2012 dibandingkan dengan tahun 2011, dan di bulan apakah lonjakan tertinggi terjadi?*")
    st.markdown("---")

    monthly_trend = filtered_daily.groupby(['yr_day', 'mnth_day'])['cnt_day'].sum().reset_index()
    fig3, ax3 = plt.subplots(figsize=(16, 6))
    sns.lineplot(data=monthly_trend, x='mnth_day', y='cnt_day', hue='yr_day', marker='o', markersize=7, linewidth=2.5, palette=['tab:orange', 'tab:blue'], ax=ax3)
    ax3.set_title('Tren Pertumbuhan Penyewaan Sepeda Bulanan (2011 vs 2012)', fontsize=16, fontweight='bold', pad=20)
    ax3.set_xlabel('Bulan', fontsize=12, labelpad=10)
    ax3.set_ylabel('Total Penyewaan Bulanan', fontsize=12, labelpad=10)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax3.set_xticks(range(1, 13))
    ax3.set_xticklabels(months)
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.legend(title='Tahun')
    st.pyplot(fig3)
    
    # INSIGHTS TAB 3
    st.info("""
    💡 **Insights:**
- **Pertumbuhan Positif Berkelanjutan:** Terdapat margin pertumbuhan yang sangat signifikan antara garis biru (2012) dan garis oranye (2011). Sepanjang tahun 2012, total volume penyewaan di setiap bulannya secara konsisten selalu berada di atas performa bulan yang sama pada tahun 2011. Hal ini merepresentasikan tingkat retensi dan akuisisi (growth) bisnis yang berkinerja sangat prima pada tahun keduanya.

- **Pola Siklus Puncak (Peak Season):** Kedua garis membentuk kurva parabola yang identik, membuktikan adanya pola musiman (seasonality) yang kuat. Lonjakan tertinggi (peak season) terjadi secara konsisten pada kuartal ketiga (Q3). Pada tahun 2011, puncak transaksi terjadi pada bulan Juni. Sedangkan pada tahun 2012, momentum memuncak pada bulan September dengan mencatatkan rekor penyewaan bulanan tertinggi sepanjang periode observasi (menembus angka di atas 200.000 transaksi).    """)


# --- TAB 4: ANALISIS RENTANG SUHU ---
with tab4:
    st.header("4. Pengaruh Suhu (Temperature)")
    st.markdown("**Pertanyaan Bisnis 4:** *Pada rentang suhu (temp) berapakah penyewaan sepeda mencapai volume rata-rata tertingginya, dan seberapa drastis tingkat penurunannya ketika suhu mencapai titik ekstrem dingin atau panas?*")
    st.markdown("---")

    fig4, ax4 = plt.subplots(figsize=(14, 6))
    sns.regplot(data=filtered_daily, x='temp_day', y='cnt_day', scatter_kws={'alpha':0.5, 'color': 'tab:blue'}, line_kws={'color': 'tab:orange', 'linewidth': 3}, order=2, ax=ax4)
    ax4.set_title('Pengaruh Suhu terhadap Total Penyewaan Sepeda', fontsize=16, fontweight='bold', pad=20)
    ax4.set_xlabel('Suhu / Temperature (Normalized)', fontsize=12, labelpad=10)
    ax4.set_ylabel('Total Penyewaan Harian', fontsize=12, labelpad=10)
    ax4.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig4)
    
    # INSIGHTS TAB 4
    st.info("""
    💡 **Insights:**
- **Titik Puncak (Sweet Spot):** Volume penyewaan tidak berbanding lurus terus-menerus dengan kenaikan suhu. Penyewaan sepeda mencapai volume rata-rata tertingginya pada rentang suhu hangat hingga agak panas (berada di sekitar nilai normalisasi 0.6 hingga 0.7). Pada rentang suhu ideal ini, penyewaan sering kali menembus angka di atas 7.000 hingga 8.000 transaksi per hari.

- **Penurunan di Titik Ekstrem:** Terjadi pola penurunan yang sangat drastis di kedua ujung ekstrem. Saat suhu bergeser ke arah ekstrem dingin (kiri bawah, mendekati 0.1), volume penyewaan menurun secara signifikan hingga di bawah 2.000 transaksi karena cuaca yang membekukan. Menariknya, saat suhu melewati batas sweet spot dan menjadi ekstrem panas (ujung kanan atas, di atas 0.8), garis tren mulai melengkung turun secara moderat. Hal ini memvalidasi bahwa udara yang terlalu panas menyengat juga menjadi faktor friksi yang mengurangi kenyamanan fisik pesepeda.    """)


# --- TAB 5: PREFERENSI HARI PENGGUNA KASUAL ---
with tab5:
    st.header("5. Preferensi Hari Pengguna Kasual")
    st.markdown("**Pertanyaan Bisnis 5:** *Hari apa dalam seminggu (weekday) yang menyumbang total penyewaan tertinggi khusus untuk pelanggan kasual (casual), dan apakah ada pola penurunan yang signifikan di hari-hari tertentu?*")
    st.markdown("---")

    day_mapping = {
        0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu',
        'Sunday': 'Minggu', 'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu', 
        'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu'
    }
    df_tab5 = filtered_daily.copy()
    df_tab5['weekday_day'] = df_tab5['weekday_day'].replace(day_mapping)
    day_order = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    custom_colors = ['#e67e22' if x in ['Sabtu', 'Minggu'] else '#2980b9' for x in day_order]
    
    daily_casual = df_tab5.groupby('weekday_day')['casual_day'].sum().reset_index()
    
    fig5, ax5 = plt.subplots(figsize=(14, 6))
    sns.barplot(data=daily_casual, x='weekday_day', y='casual_day', order=day_order, palette=custom_colors, ax=ax5)
    ax5.set_title('Total Penyewaan Pengguna Kasual (Casual) Berdasarkan Hari', fontsize=16, fontweight='bold', pad=20)
    ax5.set_xlabel('Hari dalam Seminggu', fontsize=12, labelpad=10)
    ax5.set_ylabel('Total Penyewaan Kasual', fontsize=12, labelpad=10)
    ax5.grid(axis='y', linestyle='--', alpha=0.6)
    for container in ax5.containers:
        ax5.bar_label(container, fmt='%.0f', padding=5, fontsize=11)
    st.pyplot(fig5)
    
    # INSIGHTS TAB 5
    st.info("""
    💡 **Insights:**
- **Dominasi Akhir Pekan (Weekend):** Hari **Sabtu** dan **Minggu** (bar berwarna oranye) menyumbang total penyewaan tertinggi secara absolut bagi pelanggan kasual. Hari Sabtu memimpin puncak transaksi dengan total menembus 153.852 penyewaan, disusul ketat oleh hari Minggu dengan 140.521 penyewaan. Ini mengonfirmasi bahwa pelanggan kasual memprioritaskan waktu luang di akhir pekan untuk menyewa sepeda.

- **Penurunan Drastis di Hari Kerja (Drop-off Pattern):** Terdapat pola penurunan yang sangat signifikan dan instan ketika memasuki hari kerja (Senin hingga Jumat, bar berwarna biru). Angka total penyewaan langsung menurun ke rentang 57.000 hingga 78.000 transaksi. Hari **Selasa** dan **Rabu** menjadi titik terendah bagi aktivitas penyewaan pelanggan kasual.    """)


# --- TAB 6: KECEPATAN ANGIN ---
with tab6:
    st.header("6. Dampak Kecepatan Angin (Windspeed)")
    st.markdown("**Pertanyaan Bisnis 6:** *Pada level kecepatan angin (windspeed) berapakah rata-rata penyewaan sepeda harian mulai mengalami penurunan drastis, dan apakah dampaknya lebih signifikan terhadap pengguna kasual dibandingkan pengguna terdaftar?*")
    st.markdown("---")

    filtered_daily['windspeed_bin'] = filtered_daily['windspeed_day'].round(1)
    wind_agg = filtered_daily.groupby('windspeed_bin').agg({'registered_day':'mean', 'casual_day':'mean'}).reset_index()
    
    fig6, ax6 = plt.subplots(figsize=(14, 6))
    ax6.plot(wind_agg['windspeed_bin'], wind_agg['registered_day'], marker='s', markersize=5, linewidth=2, label='Registered (Member)', color='tab:blue')
    ax6.plot(wind_agg['windspeed_bin'], wind_agg['casual_day'], marker='o', markersize=5, linewidth=2, label='Casual (Biasa)', color='tab:orange')
    ax6.axvline(x=0.3, color='#ff4c4c', linestyle='--', label='Critical Drop-off Point')
    ax6.set_title('Dampak Kecepatan Angin terhadap Rata-rata Penyewaan', fontsize=16, fontweight='bold', pad=20)
    ax6.set_xlabel('Kecepatan Angin (Normalized Windspeed)', fontsize=12, labelpad=10)
    ax6.set_ylabel('Rata-rata Penyewaan', fontsize=12, labelpad=10)
    ax6.grid(True, linestyle='--', alpha=0.5)
    ax6.legend()
    st.pyplot(fig6)
    
    # INSIGHTS TAB 6
    st.info("""
    💡 **Insights:**
- **Titik Penurunan Drastis (*Critical Drop-off*):** Rata-rata penyewaan sepeda (baik casual maupun registered) mulai mengalami penurunan yang sangat signifikan secara konsisten ketika kecepatan angin melewati angka normalisasi **0.3**. Di atas level ini, angin dianggap sudah terlalu kencang sehingga menambah beban fisik saat mengayuh.

- **Dampak Relatif terhadap Tipe Pengguna:** Dampak kecepatan angin secara volume terasa lebih signifikan terhadap pengguna **Registered**. Hal ini dikarenakan pengguna terdaftar adalah komuter yang memiliki ekspektasi efisiensi waktu; angin kencang akan memperlambat perjalanan mereka sehingga mereka cenderung beralih ke moda transportasi lain. Namun, secara persentase, pengguna **Casual** juga menunjukkan sensitivitas yang sama, di mana minat rekreasi mereka hilang hampir sepenuhnya saat angin mencapai level ekstrem (di atas 0.5).    """)

st.markdown("---")
st.caption("Project Analisis Data - Bike Sharing Dataset (2011-2012)")