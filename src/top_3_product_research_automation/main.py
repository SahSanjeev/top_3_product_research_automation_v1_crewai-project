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
    """Convert markdown text to PDF with UTF-8 support"""
    try:
        # Convert markdown to HTML
        html = markdown(markdown_text)
        
        # Create PDF with UTF-8 support
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Add a title with UTF-8 support
        pdf.add_font('Arial', '', 'c:/windows/fonts/arial.ttf', uni=True)
        pdf.add_font('Arial', 'B', 'c:/windows/fonts/arialbd.ttf', uni=True)
        pdf.add_font('Arial', 'I', 'c:/windows/fonts/ariali.ttf', uni=True)
        
        # Add a title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Top 3 Products Research Report', 0, 1, 'C')
        pdf.ln(10)
        
        # Set font for content
        pdf.set_font('Arial', '', 12)
        
        # Parse HTML and add to PDF
        soup = BeautifulSoup(html, 'html.parser')
        
        def clean_text(text):
            # Replace common problematic characters
            text = text.replace('—', '-')  # Replace em dash with regular dash
            text = text.replace('–', '-')  # Replace en dash with regular dash
            text = text.replace('“', '"').replace('”', '"')  # Replace smart quotes
            text = text.replace('‘', "'").replace('’', "'")  # Replace smart single quotes
            return text
        
        for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'li']):
            try:
                if element.name in ['h1', 'h2', 'h3']:
                    size = {'h1': 16, 'h2': 14, 'h3': 12}[element.name]
                    pdf.set_font('Arial', 'B', size)
                    pdf.cell(0, 10, clean_text(element.get_text()), 0, 1)
                    pdf.set_font('Arial', '', 12)
                elif element.name == 'p':
                    pdf.multi_cell(0, 10, clean_text(element.get_text()))
                    pdf.ln(5)
                elif element.name == 'ul':
                    for li in element.find_all('li'):
                        pdf.cell(10)  # Add indentation
                        pdf.cell(0, 10, '- ' + clean_text(li.get_text()), 0, 1)
                    pdf.ln(2)
            except Exception as e:
                print(f"Warning: Could not process element {element.name}: {str(e)}")
                continue
        
        # Add footer
        pdf.set_y(-15)
        pdf.set_font('Arial', 'I', 8)
        pdf.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 0, 'C')
        
        # Save the PDF with UTF-8 support
        pdf.output(output_path, 'F')
        print(f"PDF successfully generated at: {output_path}")
        
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
        raise

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
