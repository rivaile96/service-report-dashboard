# app/pages/6_Dashboard_Stats.py
# This page implements a statistics dashboard for the service data.
# It visualizes key metrics such as total units, trends over time,
# distribution by model, and distribution by company.

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from app.utils.data_handler import DataHandler

# Configure page settings
st.set_page_config(layout="wide", page_title="Dashboard Statistik Layanan")

st.title("📊 Dashboard Statistik Layanan")

# Initialize DataHandler and fetch statistics
data_handler = DataHandler()
stats = data_handler.get_dashboard_statistics()

if not stats or stats.get("total_units_in", 0) == 0 : # Check if stats is None/empty or no units
    st.warning("Tidak ada data layanan yang ditemukan untuk ditampilkan di dashboard. Silakan tambahkan data terlebih dahulu.")
    st.stop()

# --- Row 1: Key Metrics ---
st.subheader("Ringkasan Umum")
col1, col2, col3 = st.columns(3) # Adjust number of columns if more metrics are added

with col1:
    st.metric(label="Total Unit Masuk", value=f"{stats.get('total_units_in', 0):,}")

with col2:
    unique_companies = len(stats.get('units_by_company', {}))
    st.metric(label="Pelanggan Unik", value=f"{unique_companies:,}")

with col3:
    unique_models = len(stats.get('units_by_model', {}))
    st.metric(label="Model Unik", value=f"{unique_models:,}")


# --- Row 2: Units In Trend ---
st.subheader("📈 Tren Unit Masuk")

trend_data = stats.get("units_in_trend", {})
daily_trend = trend_data.get("daily", {})
weekly_trend = trend_data.get("weekly", {})
monthly_trend = trend_data.get("monthly", {})

tab_daily, tab_weekly, tab_monthly = st.tabs(["Harian (30 Hari Terakhir)", "Mingguan (12 Minggu Terakhir)", "Bulanan (12 Bulan Terakhir)"])

with tab_daily:
    if daily_trend:
        df_daily = pd.DataFrame(list(daily_trend.items()), columns=['Tanggal', 'Jumlah']).sort_values(by="Tanggal")
        fig_daily = px.line(df_daily, x='Tanggal', y='Jumlah', title="Tren Harian", markers=True)
        fig_daily.update_layout(xaxis_title="Tanggal", yaxis_title="Jumlah Unit Masuk")
        st.plotly_chart(fig_daily, use_container_width=True)
    else:
        st.info("Data tren harian tidak tersedia.")

with tab_weekly:
    if weekly_trend:
        df_weekly = pd.DataFrame(list(weekly_trend.items()), columns=['Minggu Ke-', 'Jumlah']).sort_values(by="Minggu Ke-")
        fig_weekly = px.line(df_weekly, x='Minggu Ke-', y='Jumlah', title="Tren Mingguan", markers=True)
        fig_weekly.update_layout(xaxis_title="Minggu Ke-", yaxis_title="Jumlah Unit Masuk")
        st.plotly_chart(fig_weekly, use_container_width=True)
    else:
        st.info("Data tren mingguan tidak tersedia.")

with tab_monthly:
    if monthly_trend:
        df_monthly = pd.DataFrame(list(monthly_trend.items()), columns=['Bulan', 'Jumlah']).sort_values(by="Bulan")
        fig_monthly = px.line(df_monthly, x='Bulan', y='Jumlah', title="Tren Bulanan", markers=True)
        fig_monthly.update_layout(xaxis_title="Bulan", yaxis_title="Jumlah Unit Masuk")
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        st.info("Data tren bulanan tidak tersedia.")

# --- Row 3: Model and Company Distributions ---
st.subheader("Analisis Model dan Perusahaan")
col_model, col_company = st.columns(2)

with col_model:
    st.markdown("#### 📦 Distribusi Unit berdasarkan Model")
    units_by_model = stats.get("units_by_model", {})
    top_models_data = stats.get("top_n_models", [])
    if units_by_model:
        # Bar chart for overall distribution (top N for clarity)
        df_model_dist = pd.DataFrame(list(units_by_model.items()), columns=['Model', 'Jumlah']).sort_values(by="Jumlah", ascending=False)
        fig_model_bar = px.bar(df_model_dist.head(10), x='Model', y='Jumlah', title="Top 10 Model berdasarkan Jumlah Unit")
        fig_model_bar.update_layout(xaxis_title="Model", yaxis_title="Jumlah Unit")
        st.plotly_chart(fig_model_bar, use_container_width=True)

        # Table for Top N Models
        st.markdown("##### 🏆 Top Model")
        if top_models_data:
            df_top_models = pd.DataFrame(top_models_data)
            st.dataframe(df_top_models.rename(columns={'model': 'Model', 'count': 'Jumlah'}), use_container_width=True)
        else:
            st.info("Data top model tidak tersedia.")
    else:
        st.info("Data distribusi model tidak tersedia.")

with col_company:
    st.markdown("#### 🏢 Distribusi Unit oleh Perusahaan")
    units_by_company = stats.get("units_by_company", {})
    top_companies_data = stats.get("top_n_companies", [])
    if units_by_company:
        # Bar chart for overall distribution (top N for clarity)
        df_company_dist = pd.DataFrame(list(units_by_company.items()), columns=['Perusahaan', 'Jumlah']).sort_values(by="Jumlah", ascending=False)
        fig_company_bar = px.bar(df_company_dist.head(10), x='Perusahaan', y='Jumlah', title="Top 10 Perusahaan berdasarkan Jumlah Unit")
        fig_company_bar.update_layout(xaxis_title="Perusahaan", yaxis_title="Jumlah Unit")
        st.plotly_chart(fig_company_bar, use_container_width=True)

        # Table for Top N Companies
        st.markdown("##### 🏆 Top Perusahaan")
        if top_companies_data:
            df_top_companies = pd.DataFrame(top_companies_data)
            st.dataframe(df_top_companies.rename(columns={'company': 'Perusahaan', 'count': 'Jumlah'}), use_container_width=True)
        else:
            st.info("Data top perusahaan tidak tersedia.")
    else:
        st.info("Data distribusi perusahaan tidak tersedia.")

st.markdown("---")
st.caption(f"Dashboard Statistik Layanan v1.0 | Data terakhir diambil: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
