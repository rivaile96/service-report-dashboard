import streamlit as st
import pandas as pd
from utils.data_handler import DataHandler

data_handler = DataHandler()

def show():
    st.title("🔍 Filter Service Data")
    
    df = data_handler.load_data()
    if df is None:
        st.warning("No data available. Please upload a file in the Add Data page.")
        return
    
    with st.expander("Filter Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_filter = st.text_input("Filter by Customer Name")
            item_filter = st.text_input("Filter by Item Model")
            serial_filter = st.text_input("Filter by Serial Number")
            
        with col2:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Selesai", "Perbaikan", "Masuk"]
            )
            warranty_filter = st.selectbox(
                "Filter by Warranty Status",
                ["All", "Ya", "Tidak", "Regis"]
            )
        
        date_range = st.date_input(
            "Filter by Date Range",
            value=(df['Date In'].min(), df['Date In'].max()),
            min_value=df['Date In'].min(),
            max_value=df['Date In'].max()
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if customer_filter:
        filtered_df = filtered_df[filtered_df['Customer Name'].str.contains(customer_filter, case=False)]
    if item_filter:
        filtered_df = filtered_df[filtered_df['Item'].str.contains(item_filter, case=False)]
    if serial_filter:
        filtered_df = filtered_df[filtered_df['Serial Number'].str.contains(serial_filter, case=False)]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    if warranty_filter != "All":
        filtered_df = filtered_df[filtered_df['Warranty Status'] == warranty_filter]
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Date In'] >= pd.to_datetime(date_range[0])) & 
            (filtered_df['Date In'] <= pd.to_datetime(date_range[1]))
        ]
    
    st.dataframe(filtered_df, use_container_width=True)
    
    if not filtered_df.empty:
        st.download_button(
            label="Download Filtered Data",
            data=data_handler.export_to_excel(filtered_df),
            file_name="filtered_service_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

show()