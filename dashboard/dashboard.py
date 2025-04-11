import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('dashboard/day.csv')
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_name'] = df['season'].map(season_map)
df['date'] = pd.to_datetime(df['dteday'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month_name()
bins = [0, df['cnt'].quantile(0.33), df['cnt'].quantile(0.66), df['cnt'].max()]
labels = ['Low', 'Medium', 'High']
df['usage_level'] = pd.cut(df['cnt'], bins=bins, labels=labels, include_lowest=True)

st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect("Pilih Tahun", options=df['year'].unique(), default=df['year'].unique())
selected_season = st.sidebar.multiselect("Pilih Musim", options=df['season_name'].unique(), default=df['season_name'].unique())
filtered_df = df[(df['year'].isin(selected_year)) & (df['season_name'].isin(selected_season))]

st.title("📊 Bike Sharing Dashboard - Mochammad Ikhsan")
st.markdown("Dashboard interaktif ini menampilkan analisis dari Bike Sharing Dataset (Washington DC, 2011-2012).")

st.metric("Total Penyewaan Sepeda", f"{int(filtered_df['cnt'].sum()):,}")
st.metric("Pengguna Casual", f"{int(filtered_df['casual'].sum()):,}")
st.metric("Pengguna Registered", f"{int(filtered_df['registered'].sum()):,}")

st.subheader("Total Penyewaan Sepeda per Musim")
season_summary = filtered_df.groupby('season_name')['cnt'].sum().reset_index()
fig1, ax1 = plt.subplots()
sns.barplot(data=season_summary, x='season_name', y='cnt', palette='viridis', ax=ax1)
ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Penyewaan")
ax1.set_title("Penyewaan Sepeda per Musim")
st.pyplot(fig1)

st.subheader("Tren Pengguna Casual vs Registered per Bulan")
year_month = filtered_df.groupby(['year', 'month'])[['casual', 'registered']].sum().reset_index()
fig2, ax2 = plt.subplots()
for user_type in ['casual', 'registered']:
    sns.lineplot(data=year_month, x='month', y=user_type, label=user_type.capitalize(), marker='o', ax=ax2)
ax2.set_xlabel("Bulan")
ax2.set_ylabel("Jumlah Pengguna")
ax2.legend()
ax2.set_title("Tren Pengguna Casual dan Registered")
st.pyplot(fig2)

st.subheader("Distribusi Tingkat Penggunaan Sepeda")
fig3, ax3 = plt.subplots()
sns.countplot(data=filtered_df, x='usage_level', palette='pastel', order=labels, ax=ax3)
ax3.set_xlabel("Tingkat Penggunaan")
ax3.set_ylabel("Jumlah Hari")
ax3.set_title("Distribusi Tingkat Penggunaan Sepeda")
st.pyplot(fig3)

st.markdown("---")
st.caption("© 2025 Mochammad Ikhsan - Bike Sharing Dataset Analysis")