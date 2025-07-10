import streamlit as st
from utils.data_handler import DataHandler
from datetime import datetime

data_handler = DataHandler()

def show():
    st.title("➕ Add New Service Record")
    
    with st.form("add_record_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name*")
            item = st.text_input("Item Model*")
            serial_number = st.text_input("Serial Number*")
            
        with col2:
            warranty_status = st.selectbox("Warranty Status*", ["Ya", "Tidak", "Regis"])
            status = st.selectbox("Status*", ["Selesai", "Perbaikan", "Masuk"])
        
        problem = st.text_area("Problem Description*")
        service_location = st.text_input("Service Location")
        
        date_col1, date_col2, date_col3 = st.columns(3)
        with date_col1:
            date_in = st.date_input("Date In")
        with date_col2:
            service_date = st.date_input("Service Date")
        with date_col3:
            date_out = st.date_input("Date Out")
        
        submitted = st.form_submit_button("Add Record")
        
        if submitted:
            if not all([customer_name, item, serial_number, warranty_status, status, problem]):
                st.error("Please fill all required fields (*)")
            else:
                new_record = {
                    "Customer Name": customer_name,
                    "Item": item,
                    "Serial Number": serial_number,
                    "CN/PN": "",
                    "Warranty Status": warranty_status,
                    "Status": status,
                    "Date In": date_in,
                    "Service Date": service_date,
                    "Date Out": date_out,
                    "Problem": problem,
                    "Service Location": service_location
                }
                
                if data_handler.add_record(new_record):
                    st.success("Record added successfully!")
                else:
                    st.error("Failed to add record. Please try again.")

show()