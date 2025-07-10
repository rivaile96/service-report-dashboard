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

    def _calculate_units_in_trend(self, df, period_char, date_column='Date In', num_periods=None):
        """Helper function to calculate trends.
        period_char: 'D' for daily, 'W' for weekly, 'M' for monthly
        num_periods: number of past periods to include (e.g., 30 for last 30 days)
        """
        if df is None or df.empty or date_column not in df.columns:
            return {}

        # Ensure date_column is datetime
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        # Drop rows where date conversion failed
        df_filtered = df.dropna(subset=[date_column])
        if df_filtered.empty:
            return {}

        # Set date_column as index for resampling
        df_indexed = df_filtered.set_index(date_column)

        # Resample and count
        trend = df_indexed.resample(period_char).size()

        if num_periods:
            trend = trend.tail(num_periods)

        # Format for JSON (especially for weekly period objects)
        if period_char == 'W':
             # Convert Period objects to string for weekly data e.g. 2023-W34
            return {item.strftime('%Y-W%U'): count for item, count in trend.items()}
        else:
            return {item.strftime('%Y-%m-%d' if period_char == 'D' else '%Y-%m'): count for item, count in trend.items()}

    def _get_distribution_by_column(self, df, column_name):
        if df is None or df.empty or column_name not in df.columns:
            return {}
        return df[column_name].value_counts().to_dict()

    def _get_top_n_by_column(self, df, column_name, n=5):
        if df is None or df.empty or column_name not in df.columns:
            return []

        top_n = df[column_name].value_counts().nlargest(n)
        return [{"item": index, "count": value} for index, value in top_n.items()]

    def get_dashboard_statistics(self, top_n_count=5):
        """
        Calculates and returns a dictionary of statistics for the dashboard.

        Args:
            top_n_count (int): The number of top items (e.g., models, companies) to return.

        Returns:
            dict: A dictionary containing various statistics:
                - "total_units_in": Total number of records.
                - "units_in_trend": Dict with "daily", "weekly", "monthly" trends.
                    Each trend is a dict of {period_string: count}.
                - "units_by_model": Dict of {model_name: count}.
                - "top_n_models": List of dicts [{"model": name, "count": value}].
                - "units_by_company": Dict of {company_name: count}.
                - "top_n_companies": List of dicts [{"company": name, "count": value}].
        """
        df = self.load_data()

        if df is None or df.empty:
            return {
                "total_units_in": 0,
                "units_in_trend": {"daily": {}, "weekly": {}, "monthly": {}},
                "units_by_model": {},
                "top_n_models": [],
                "units_by_company": {},
                "top_n_companies": []
            }

        total_units_in = len(df)

        # Trends: Last 30 days, last 12 weeks, last 12 months
        daily_trend = self._calculate_units_in_trend(df.copy(), 'D', num_periods=30)
        weekly_trend = self._calculate_units_in_trend(df.copy(), 'W', num_periods=12)
        monthly_trend = self._calculate_units_in_trend(df.copy(), 'M', num_periods=12)

        units_by_model = self._get_distribution_by_column(df, 'Item')
        # In top_n_models, the key for item name should match the frontend design, e.g. 'model'
        top_n_models = [{'model': item['item'], 'count': item['count']}
                        for item in self._get_top_n_by_column(df, 'Item', n=top_n_count)]

        units_by_company = self._get_distribution_by_column(df, 'Customer Name')
        # In top_n_companies, the key for item name should match the frontend design, e.g. 'company'
        top_n_companies = [{'company': item['item'], 'count': item['count']}
                           for item in self._get_top_n_by_column(df, 'Customer Name', n=top_n_count)]

        return {
            "total_units_in": total_units_in,
            "units_in_trend": {
                "daily": daily_trend,
                "weekly": weekly_trend,
                "monthly": monthly_trend
            },
            "units_by_model": units_by_model,
            "top_n_models": top_n_models,
            "units_by_company": units_by_company,
            "top_n_companies": top_n_companies
        }