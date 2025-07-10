import streamlit as st
import pandas as pd
from utils.data_handler import DataHandler
from datetime import datetime

data_handler = DataHandler()

def show():
    st.title("✏️ Edit Service Records")
    
    df = data_handler.load_data()
    if df is None:
        st.warning("No data available. Please upload a file in the Add Data page.")
        return
    
    # Select record to edit
    record_to_edit = st.selectbox(
        "Select record to edit",
        df.index,
        format_func=lambda x: f"Record {x+1} - {df.loc[x, 'Customer Name']}"
    )
    
    if record_to_edit is not None:
        record = df.loc[record_to_edit].to_dict()
        
        with st.form("edit_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                customer_name = st.text_input("Customer Name", value=record['Customer Name'])
                item = st.text_input("Item Model", value=record['Item'])
                serial_number = st.text_input("Serial Number", value=record['Serial Number'])
                
            with col2:
                warranty_status = st.selectbox(
                    "Warranty Status",
                    ["Ya", "Tidak", "Regis"],
                    index=["Ya", "Tidak", "Regis"].index(record['Warranty Status'])
                )
                status = st.selectbox(
                    "Status",
                    ["Selesai", "Perbaikan", "Masuk"],
                    index=["Selesai", "Perbaikan", "Masuk"].index(record['Status'])
                )
            
            problem = st.text_area("Problem Description", value=record['Problem'])
            service_location = st.text_input("Service Location", value=record.get('Service Location', ''))
            
            date_col1, date_col2, date_col3 = st.columns(3)
            with date_col1:
                date_in = st.date_input("Date In", value=record['Date In'].date() if pd.notna(record['Date In']) else None)
            with date_col2:
                service_date = st.date_input("Service Date", value=record['Service Date'].date() if pd.notna(record['Service Date']) else None)
            with date_col3:
                date_out = st.date_input("Date Out", value=record['Date Out'].date() if pd.notna(record['Date Out']) else None)
            
            submitted = st.form_submit_button("Update Record")
            
            if submitted:
                updated_record = {
                    "Customer Name": customer_name,
                    "Item": item,
                    "Serial Number": serial_number,
                    "CN/PN": record.get('CN/PN', ''),
                    "Warranty Status": warranty_status,
                    "Status": status,
                    "Date In": date_in,
                    "Service Date": service_date,
                    "Date Out": date_out,
                    "Problem": problem,
                    "Service Location": service_location
                }
                
                if data_handler.update_record(record_to_edit, updated_record):
                    st.success("Record updated successfully!")
                else:
                    st.error("Failed to update record. Please try again.")

show()