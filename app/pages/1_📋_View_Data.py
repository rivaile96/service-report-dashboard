import streamlit as st
from utils.data_handler import DataHandler

data_handler = DataHandler()

def show():
    st.title("📋 View Service Data")
    
    df = data_handler.load_data()
    if df is not None:
        st.dataframe(df, use_container_width=True)
        
        # Download button
        st.download_button(
            label="Download Current Data",
            data=data_handler.export_to_excel(df),
            file_name="service_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No data available. Please upload a file in the Add Data page.")

show()