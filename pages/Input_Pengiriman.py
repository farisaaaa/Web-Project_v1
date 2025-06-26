import streamlit as st
import pandas as pd
import numpy as np
import pickle
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
import mysql.connector

# ---------------------------- SETUP ----------------------------
st.set_page_config(page_title="📦 Input Pengiriman", layout="wide")

# ---------------------------- KONEKSI DB ----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="logistics_db"
)
c = conn.cursor()

# ---------------------------- LOAD DATASET ----------------------------
df = pd.read_csv("Data1st.csv")

# ---------------------------- LOGIC KATEGORI & BERAT ----------------------------
category_size_mapping = {
    'Snacks': 'kecil', 'Books': 'kecil', 'Cosmetics': 'kecil', 'Grocery': 'kecil',
    'Sports': 'sedang', 'Clothing': 'sedang', 'Shoes': 'sedang', 'Toys': 'sedang',
    'Electronics': 'besar', 'Home': 'besar'
}

def get_weight_range(category):
    size = category_size_mapping.get(category)
    if size == 'kecil':
        return (1.0, 5.0)
    elif size == 'sedang':
        return (5.1, 10.0)
    elif size == 'besar':
        return (10.1, 15.0)
    else:
        return None

def recommend_vehicle(weight):
    if weight <= 5.0:
        return 'pick up truck'
    elif weight <= 10.0:
        return 'van'
    elif weight <= 15.0:
        return 'cargo truck'
    else:
        return None

# ---------------------------- FORM INPUT ----------------------------
st.title("📦 Form Pengiriman Barang")

with st.form("input_form"):
    category = st.selectbox("Pilih Kategori Barang", list(category_size_mapping.keys()))

    weight_range = get_weight_range(category)
    weight = st.number_input("Masukkan Berat Barang (kg)", min_value=1.0, max_value=15.0, step=0.1, format="%.1f")

    branch_start = st.selectbox("Pilih Titik Awal", df["Branch_Start"].dropna().unique())
    branch_drop = st.selectbox("Pilih Titik Tujuan", df["Branch_Start"].dropna().unique())

    submitted = st.form_submit_button("Proses dan Simpan")

    if submitted:
        if not weight_range:
            st.error("❌ Kategori tidak dikenali!")
        elif not (weight_range[0] <= weight <= weight_range[1]):
            st.error(f"❌ Berat {weight} kg tidak sesuai dengan kategori '{category}' ({weight_range[0]}–{weight_range[1]} kg).")
        elif branch_start == branch_drop:
            st.error("❌ Titik awal dan akhir tidak boleh sama!")
        else:
            # Rekomendasi kendaraan
            recommended_vehicle = recommend_vehicle(weight)
            st.success(f"✅ Rekomendasi kendaraan: {recommended_vehicle}")

            # Simpan ke database
            sql = """
                INSERT INTO data_logistics (Category, Weight, Vehicle_Type_Assigned, Branch_Start, Branch_Drop)
                VALUES (%s, %s, %s, %s, %s)
            """
            val = (category, weight, recommended_vehicle, branch_start, branch_drop)
            c.execute(sql, val)
            conn.commit()
            st.success("📥 Data berhasil disimpan ke MySQL!")

            # Visualisasi Rute
            df_branch = df[['Branch_Start', 'Start_Latitude', 'Start_Longitude']].drop_duplicates()
            coords = []
            for branch in [branch_start, branch_drop]:
                row = df_branch[df_branch['Branch_Start'] == branch].iloc[0]
                coords.append((row['Start_Latitude'], row['Start_Longitude']))

            st.subheader("🗺️ Visualisasi Rute Pengiriman")
            center_lat = np.mean([coords[0][0], coords[1][0]])
            center_lon = np.mean([coords[0][1], coords[1][1]])
            m = folium.Map(location=[center_lat, center_lon], zoom_start=6)
            folium.Marker(location=coords[0], popup=f"Start: {branch_start}", icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(location=coords[1], popup=f"Tujuan: {branch_drop}", icon=folium.Icon(color='red')).add_to(m)
            folium.PolyLine(coords, color='blue', weight=3).add_to(m)
            folium_static(m)

            # Estimasi Jarak
            est_dist = round(geodesic(coords[0], coords[1]).km, 2)
            st.info(f"📏 Estimasi jarak pengiriman: {est_dist} km")
