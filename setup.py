from setuptools import setup, find_packages

setup(
    name="top_3_product_research_automation",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'fpdf',
        'markdown',
        'beautifulsoup4',
        'xhtml2pdf',
    ],
)
