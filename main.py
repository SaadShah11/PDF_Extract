from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError, PDFInfoNotInstalledError, PDFSyntaxError
from PIL import Image

# Disable PIL's decompression‐bomb protection
Image.MAX_IMAGE_PIXELS = None

pdf_path = './BK-000054.pdf'
output_folder = './output_images'

import os
os.makedirs(output_folder, exist_ok=True)

try:
    from pdf2image.pdf2image import pdfinfo_from_path
    info = pdfinfo_from_path(pdf_path, poppler_path='./poppler-24.08.0/Library/bin')
    max_pages = info["Pages"]
except (PDFPageCountError, PDFInfoNotInstalledError, PDFSyntaxError) as e:
    print("Error getting page count:", e)
    exit(1)

for page_num in range(1, max_pages + 1):
    print(f"Processing page {page_num}/{max_pages}")
    # Lower DPI if you hit memory limits
    page_image = convert_from_path(
        pdf_path,
        dpi=300,  # try 300 instead of 600
        first_page=page_num,
        last_page=page_num,
        poppler_path='./poppler-24.08.0/Library/bin'
    )[0]

    output_path = os.path.join(output_folder, f'page_{page_num}.png')
    page_image.save(output_path, 'PNG')

print("Conversion completed successfully.")
