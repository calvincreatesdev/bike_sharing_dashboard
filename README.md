## 1. Setup Environment - Anaconda
```
conda create --name main-ds python=3.12.2
conda activate main-ds
pip install -r requirements.txt
```

## 2. Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## 3. Run Streamlit App
```
streamlit run dashboard/dashboard.py
```



## 📌 Project Overview
Proyek ini merupakan **Data Analytics Dashboard** interaktif yang dibangun menggunakan **Streamlit** untuk menganalisis dataset *Bike Sharing*.
Tujuan utama dari proyek ini adalah menggali *business insights* dari pola perilaku pengguna (komuter vs kasual) dan memahami bagaimana faktor eksternal (cuaca, musim, suhu, kecepatan angin) memengaruhi tingkat konversi penyewaan sepeda harian.

## 📊 Business Questions Solved
Dashboard ini dirancang untuk menjawab 6 pertanyaan strategis bisnis berikut:
1. Bagaimana perbedaan pola jam sibuk penyewaan sepeda antara pengguna kasual (*casual*) dan pengguna terdaftar (*registered*) pada hari kerja dibandingkan hari libur?
2. Seberapa besar dampak perubahan musim dan kondisi cuaca harian terhadap rata-rata jumlah penyewaan sepeda?
3. Bagaimana tren pertumbuhan jumlah penyewaan sepeda secara bulanan saat membandingkan performa tahun 2011 dan 2012?
4. Sejauh mana pengaruh rentang suhu harian terhadap total volume penyewaan sepeda?
5. Pada hari apa saja pengguna kasual (*casual*) paling banyak melakukan penyewaan sepeda dalam seminggu?
6. Bagaimana dampak kecepatan angin terhadap rata-rata penyewaan sepeda, dan pada titik mana terjadi penurunan (*drop-off*) yang signifikan?

## 🛠️ Technology Stack
- **Data Manipulation:** `pandas`, `numpy`
- **Data Visualization:** `matplotlib`, `seaborn`
- **Web Dashboard:** `streamlit`
- **Environment:** `Jupyter Notebook` / `VSCode`

## 📂 Project Structure
```text
📦 Bike-Sharing-Analytics
 ┣ 📂 dashboard
 ┃ ┣ 📜 dashboard.py          # Streamlit script
 ┃ ┗ 📜 main_data.csv         # Dataset after cleaning
 ┣ 📂 data
 ┃ ┣ 📜 day.csv               # Raw dataset (harian)
 ┃ ┗ 📜 hour.csv              # Raw dataset (jam)
 ┣ 📜 notebook.ipynb          # Main assignment
 ┣ 📜 README.md               # Proyek dokumentasi
 ┣ 📜 requirements.txt        # library
 ┗ 📜 url.txt                 # Link live dashboard
