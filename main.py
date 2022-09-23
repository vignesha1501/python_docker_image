# import statements
import pdfplumber
import re

def scanResume(m):
    pdf = pdfplumber.open('Sample.pdf')    
    all_text=''
    for pdf_page in pdf.pages:
        single_page_text = pdf_page.extract_text()
        all_text = all_text + '\n' + single_page_text
    textList=all_text.split("\n")




