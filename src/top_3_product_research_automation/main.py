#!/usr/bin/env python
import sys
import os
from datetime import datetime
from fpdf import FPDF
from markdown import markdown
from bs4 import BeautifulSoup
from top_3_product_research_automation.crew import Top3ProductResearchAutomationCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def markdown_to_pdf(markdown_text, output_path):
    """Convert markdown text to PDF with proper formatting and encoding"""
    try:
        from fpdf import FPDF
        import textwrap
        
        # Create PDF with proper encoding
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Add Unicode-compatible fonts (using DejaVu as it has good Unicode support)
        try:
            pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
            pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)
            pdf.add_font('DejaVu', 'I', 'DejaVuSans-Oblique.ttf', uni=True)
            font_family = 'DejaVu'
        except:
            # Fallback to Arial if DejaVu is not available
            try:
                pdf.add_font('Arial', '', 'c:/windows/fonts/arial.ttf', uni=True)
                pdf.add_font('Arial', 'B', 'c:/windows/fonts/arialbd.ttf', uni=True)
                pdf.add_font('Arial', 'I', 'c:/windows/fonts/ariali.ttf', uni=True)
                font_family = 'Arial'
            except:
                # If no custom fonts work, use the default
                font_family = 'Arial'
        
        # Set default font
        pdf.set_font(font_family, '', 12)
        
        # Add title
        pdf.set_font(font_family, 'B', 16)
        pdf.cell(0, 10, 'Top 3 Products Research Report', 0, 1, 'C')
        pdf.ln(10)
        
        # Process markdown content
        lines = markdown_text.split('\n')
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    in_list = False
                    pdf.ln(5)
                continue
                
            # Handle headers
            if line.startswith('###'):
                pdf.set_font(font_family, 'B', 12)
                pdf.cell(0, 10, line.lstrip('#').strip(), 0, 1)
                pdf.ln(2)
                pdf.set_font(font_family, '', 12)
            elif line.startswith('##'):
                pdf.set_font(font_family, 'B', 14)
                pdf.cell(0, 10, line.lstrip('#').strip(), 0, 1)
                pdf.ln(3)
                pdf.set_font(font_family, '', 12)
            elif line.startswith('#'):
                pdf.set_font(font_family, 'B', 16)
                pdf.cell(0, 10, line.lstrip('#').strip(), 0, 1)
                pdf.ln(5)
                pdf.set_font(font_family, '', 12)
            # Handle lists
            elif line.strip().startswith('- '):
                if not in_list:
                    in_list = True
                pdf.cell(10)  # Indent
                pdf.cell(0, 10, '• ' + line[1:].strip(), 0, 1)  # Use bullet point
            # Handle tables (simple implementation)
            elif '|' in line and '---' not in line:
                # Simple table handling - split by | and create columns
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                col_width = 190 / len(cells) if cells else 0
                for i, cell in enumerate(cells):
                    if i == len(cells) - 1:
                        ln = 1
                    else:
                        ln = 0
                    if '**' in cell:  # Bold for headers
                        pdf.set_font(font_family, 'B', 12)
                        pdf.cell(col_width, 10, cell.replace('**', ''), 0, ln, 'C')
                        pdf.set_font(font_family, '', 12)
                    else:
                        pdf.cell(col_width, 10, cell, 0, ln, 'L')
                pdf.ln(5)
            # Regular paragraph
            else:
                if in_list:
                    in_list = False
                    pdf.ln(5)
                # Handle long lines with textwrap
                for wrapped_line in textwrap.wrap(line, width=90):
                    pdf.cell(0, 10, wrapped_line, 0, 1)
                pdf.ln(2)
        
        # Add footer
        pdf.set_y(-15)
        pdf.set_font(font_family, 'I', 8)
        pdf.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 0, 'C')
        
        # Save the PDF
        pdf.output(output_path, 'F')
        print(f"PDF successfully generated at: {output_path}")
        
        # Verify the file was created
        if not os.path.exists(output_path):
            raise Exception("Failed to create PDF file")
            
        return True
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        # Save the markdown as a fallback
        try:
            fallback_path = output_path.replace('.pdf', '.txt')
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
            print(f"Saved text version to: {fallback_path}")
        except Exception as e2:
            print(f"Failed to save fallback text file: {str(e2)}")
        return False

def run():
    """
    Run the crew and save the report as a PDF.
    """
    inputs = {
        'category': 'web app makers'
    }
    
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate a timestamp for the report filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(reports_dir, f'top_products_report_{timestamp}.pdf')
    
    # Run the crew and get the result
    crew = Top3ProductResearchAutomationCrew().crew()
    result = crew.kickoff(inputs=inputs)
    
    # Convert CrewOutput to string
    result_str = str(result)
    
    # Save the markdown report
    markdown_path = os.path.join(reports_dir, f'top_products_report_{timestamp}.md')
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(result_str)

    # Convert markdown to PDF
    markdown_to_pdf(result_str, pdf_path)
    
    print(f"\nReport generated successfully!")
    print(f"Markdown report saved to: {os.path.abspath(markdown_path)}")
    print(f"PDF report saved to: {os.path.abspath(pdf_path)}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'category': 'web app makers'
    }
    try:
        Top3ProductResearchAutomationCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Top3ProductResearchAutomationCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'category': 'web app makers'
    }
    try:
        Top3ProductResearchAutomationCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
