from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.image(os.path.join("app", "assets", "logo.png"), 10, 8, 25)
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'Service Report', 0, 0, 'C')
        self.ln(20)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def generate_pdf_report(df, report_type):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Report header
    pdf.cell(0, 10, f"Report Type: {report_type}", 0, 1)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
    pdf.ln(10)
    
    if report_type == "Summary Report":
        generate_summary_report(pdf, df)
    elif report_type == "Detailed Report":
        generate_detailed_report(pdf, df)
    else:
        generate_warranty_report(pdf, df)
    
    # Save to exports folder
    os.makedirs(os.path.join("app", "data", "exports"), exist_ok=True)
    pdf_path = os.path.join("app", "data", "exports", f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    pdf.output(pdf_path)
    return pdf_path

def generate_summary_report(pdf, df):
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Summary Statistics", 0, 1)
    pdf.set_font("Arial", size=10)
    
    # Basic stats
    stats = {
        "Total Records": len(df),
        "By Status": df['Status'].value_counts().to_dict(),
        "By Warranty": df['Warranty Status'].value_counts().to_dict()
    }
    
    for stat, value in stats.items():
        if isinstance(value, dict):
            pdf.cell(0, 10, f"{stat}:", 0, 1)
            for k, v in value.items():
                pdf.cell(20)
                pdf.cell(0, 10, f"- {k}: {v}", 0, 1)
        else:
            pdf.cell(0, 10, f"{stat}: {value}", 0, 1)
    
    pdf.ln(10)
    pdf.cell(0, 10, "Top 10 Customers by Service Requests:", 0, 1)
    top_customers = df['Customer Name'].value_counts().head(10)
    for i, (customer, count) in enumerate(top_customers.items(), 1):
        pdf.cell(0, 10, f"{i}. {customer}: {count}", 0, 1)

def generate_detailed_report(pdf, df):
    # Table header
    pdf.set_font("Arial", 'B', 10)
    col_widths = [40, 30, 30, 20, 20, 40]
    headers = ["Customer", "Item", "Serial", "Status", "Warranty", "Problem"]
    
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
    pdf.ln()
    
    # Table content
    pdf.set_font("Arial", size=8)
    for _, row in df.iterrows():
        for i, col in enumerate(headers):
            key = "Customer Name" if col == "Customer" else col
            pdf.cell(col_widths[i], 10, str(row[key]), 1, 0, 'L')
        pdf.ln()
        if pdf.get_y() > 260:  # Add new page if near bottom
            pdf.add_page()
            # Repeat header
            pdf.set_font("Arial", 'B', 10)
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
            pdf.ln()
            pdf.set_font("Arial", size=8)

def generate_warranty_report(pdf, df):
    warranty_df = df[df['Warranty Status'] == 'Ya']
    pdf.cell(0, 10, f"Warranty Items: {len(warranty_df)}", 0, 1)
    
    # Group by customer
    grouped = warranty_df.groupby('Customer Name')
    for customer, group in grouped:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 10, f"Customer: {customer}", 0, 1)
        pdf.set_font("Arial", size=8)
        
        for _, row in group.iterrows():
            pdf.cell(20)
            pdf.multi_cell(0, 10, 
                f"Item: {row['Item']} | Serial: {row['Serial Number']}\n"
                f"Problem: {row['Problem']}\n"
                f"Service Date: {row['Service Date'].strftime('%Y-%m-%d') if pd.notna(row['Service Date']) else 'N/A'}"
            )
            pdf.ln(5)