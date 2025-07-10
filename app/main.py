import streamlit as st
from utils.data_handler import DataHandler
import os

# Initialize data handler
data_handler = DataHandler()

def main():
    st.set_page_config(
        page_title="Service Report Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    # Load custom CSS
    with open(os.path.join("app", "assets", "style.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    st.title("📊 Service Report Dashboard")
    st.markdown("---")
    
    st.info("""
    Welcome to the Service Report Dashboard. 
    Use the navigation menu to view, add, edit, or filter service records.
    """)

if __name__ == "__main__":
    main()