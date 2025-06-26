import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

st.title("📊 Visualisasi Data Pengiriman")

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="logistics_db"
)
c = conn.cursor()
c.execute("SELECT * FROM data_logistics")
rows = c.fetchall()
columns = [desc[0] for desc in c.description]
df = pd.DataFrame(rows, columns=columns)

# Distribusi Berat per Kendaraan
st.subheader("Distribusi Berat Barang per Jenis Kendaraan")
fig1 = px.box(df, x="Vehicle_Type_Assigned", y="Weight", color="Vehicle_Type_Assigned")
st.plotly_chart(fig1, use_container_width=True)

# Jumlah Pengiriman
st.subheader("Jumlah Pengiriman per Jenis Kendaraan")
st.bar_chart(df["Vehicle_Type_Assigned"].value_counts())

# Tabel data
st.subheader("📋 Tabel Data")
st.dataframe(df, use_container_width=True)
