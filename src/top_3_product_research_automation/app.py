import streamlit as st
import os
from datetime import datetime
from pathlib import Path
import glob

def display_report(markdown_content):
    """Display markdown content in Streamlit with enhanced styling"""
    st.markdown("""
    <style>
        .main {
            max-width: 1200px;
            padding: 2rem;
        }
        .report-title {
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section {
            margin: 1.5rem 0;
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #F8FAFC;
        }
        .product-card {
            border-left: 4px solid #3B82F6;
            padding: 1rem;
            margin: 1rem 0;
            background: white;
            border-radius: 0.25rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Split markdown into sections
    sections = markdown_content.split('## ')
    
    # Display title
    if sections:
        title = sections[0].strip()
        st.markdown(f'<h1 class="report-title">{title}</h1>', unsafe_allow_html=True)
    
    # Display sections
    for section in sections[1:]:
        if not section.strip():
            continue
            
        section_parts = section.split('\n', 1)
        section_title = section_parts[0].strip()
        section_content = section_parts[1] if len(section_parts) > 1 else ''
        
        with st.container():
            st.markdown(f'<div class="section">', unsafe_allow_html=True)
            st.markdown(f'## {section_title}')
            
            # Handle product sections specially
            if section_title.lower().startswith(('product', 'app', 'tool')):
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.markdown(section_content)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown(section_content)
            
            st.markdown('</div>', unsafe_allow_html=True)

def get_latest_report():
    """Get the most recent report from the reports directory"""
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
    if not os.path.exists(reports_dir):
        return None
        
    # Find all markdown reports
    report_files = glob.glob(os.path.join(reports_dir, 'top_products_report_*.md'))
    if not report_files:
        return None
        
    # Get the most recent file
    latest_file = max(report_files, key=os.path.getmtime)
    with open(latest_file, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    st.set_page_config(
        page_title="Product Research Report",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Product Research Report Viewer")
    
    # Add a button to regenerate the report
    if st.button("🔄 Generate New Report"):
        st.info("Generating a new report. This may take a few minutes...")
        import subprocess
        import sys
        try:
            # Run the report generation
            subprocess.run([sys.executable, "main.py", "run"], check=True, cwd=os.path.dirname(__file__))
            st.success("Report generated successfully!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
    
    # Display the latest report
    report_content = get_latest_report()
    
    if report_content:
        display_report(report_content)
    else:
        st.warning("No reports found. Click the button above to generate a new report.")

if __name__ == "__main__":
    main()
