# from docx import Document

# def extract_pages(docx_file):
#     document = Document(docx_file)
#     page_content = []
#     current_page = []

#     for paragraph in document.paragraphs:
#         current_page.append(paragraph.text)
#         # Detect a page break (may require manual adjustment based on document structure)
#         if 'PAGE_BREAK' in paragraph.text or paragraph.text.strip() == '':
#             page_content.append("\n".join(current_page).strip())
#             current_page = []

#     # Add remaining content to the last page
#     if current_page:
#         page_content.append("\n".join(current_page).strip())

#     return page_content

# # Usage
# file_path = r"C:\Users\CVHS\Downloads\Prior_Auth_Process_Insights.docx"
# pages = extract_pages(file_path)

# for i, page in enumerate(pages, start=1):
#     print(f"PAGE {i}:\n{page}\n{'-' * 50}")

import pdfplumber

# Open the PDF file
file_path = r"C:\Users\CVHS\Downloads\JA-Salesforce Case Comments and Chatter Functionalities for Patient Support Center.pdf"
with pdfplumber.open(file_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"Page {i + 1} content:")
        print(page.extract_text())
        print("-" * 50)