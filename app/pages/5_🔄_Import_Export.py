import streamlit as st
import pandas as pd
import os
from utils.data_handler import DataHandler
from utils.pdf_generator import generate_pdf_report
from datetime import datetime

data_handler = DataHandler()

def show():
    st.title("🔄 Import/Export Data")
    
    # Import Section
    st.header("Import Data")
    uploaded_file = st.file_uploader(
        "Upload Excel File", 
        type=["xlsx", "xls"],
        help="Upload an Excel file to import data"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.success("File loaded successfully!")
            
            # Show preview
            with st.expander("Preview Data"):
                st.dataframe(df.head())
            
            if st.button("Confirm Import"):
                save_path = os.path.join("app", "data", "imports", f"import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                df.to_excel(save_path, index=False)
                data_handler.replace_data(df)
                st.success("Data imported successfully!")
        except Exception as e:
            st.error(f"Error importing file: {str(e)}")
    
    # Export Section
    st.header("Export Data")
    export_format = st.radio(
        "Select Export Format",
        ["Excel", "PDF Report"],
        horizontal=True
    )
    
    df = data_handler.load_data()
    if df is not None and not df.empty:
        if export_format == "Excel":
            st.download_button(
                label="📥 Download Excel",
                data=data_handler.export_to_excel(df),
                file_name=f"service_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("PDF Report Options")
            report_type = st.selectbox(
                "Report Type",
                ["Summary Report", "Detailed Report", "Warranty Report"]
            )
            
            if st.button("Generate PDF Report"):
                with st.spinner("Generating PDF..."):
                    pdf_path = generate_pdf_report(df, report_type)
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📥 Download PDF",
                            data=f,
                            file_name=f"service_report_{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf"
                        )
    else:
        st.warning("No data available to export")

show()