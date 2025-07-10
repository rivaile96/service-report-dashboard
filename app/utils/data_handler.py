import pandas as pd
import os
from datetime import datetime
import streamlit as st
from io import BytesIO

class DataHandler:
    def __init__(self):
        self.data_dir = os.path.join("app", "data")
        self.data_file = os.path.join(self.data_dir, "service_data.xlsx")
        os.makedirs(self.data_dir, exist_ok=True)
        
    def load_data(self):
        """Load data from Excel file"""
        if os.path.exists(self.data_file):
            try:
                df = pd.read_excel(self.data_file)
                # Convert date columns
                date_cols = ['Date In', 'Service Date', 'Date Out']
                for col in date_cols:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                return df
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                return None
        return None
    
    def replace_data(self, new_df):
        """Replace all data with new DataFrame"""
        try:
            new_df.to_excel(self.data_file, index=False)
            return True
        except Exception as e:
            st.error(f"Error replacing data: {str(e)}")
            return False
    
    def add_record(self, new_record):
        """Add a new record to the data"""
        try:
            df = self.load_data() or pd.DataFrame(columns=[
                'No', 'Customer Name', 'Item', 'Serial Number', 'CN/PN',
                'Warranty Status', 'Status', 'Date In', 'Service Date',
                'Date Out', 'Problem', 'Service Location'
            ])
            
            # Auto-increment ID
            new_record['No'] = len(df) + 1 if not df.empty else 1
            
            # Add new record
            new_df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            new_df.to_excel(self.data_file, index=False)
            return True
        except Exception as e:
            st.error(f"Error adding record: {str(e)}")
            return False
    
    def update_record(self, index, updated_record):
        """Update an existing record"""
        try:
            df = self.load_data()
            if df is None:
                return False
                
            for key, value in updated_record.items():
                df.at[index, key] = value
                
            df.to_excel(self.data_file, index=False)
            return True
        except Exception as e:
            st.error(f"Error updating record: {str(e)}")
            return False
    
    def export_to_excel(self, df):
        """Export DataFrame to Excel bytes"""
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()
    
    def get_stats(self):
        """Get summary statistics"""
        df = self.load_data()
        if df is None or df.empty:
            return None
            
        return {
            "total_records": len(df),
            "by_status": df['Status'].value_counts().to_dict(),
            "by_warranty": df['Warranty Status'].value_counts().to_dict(),
            "top_customers": df['Customer Name'].value_counts().head(5).to_dict(),
            "common_problems": df['Problem'].value_counts().head(5).to_dict()
        }