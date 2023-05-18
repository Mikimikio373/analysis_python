import os
import sys

import pypdf
from pdf2image import convert_from_path

if not len(sys.argv) == 2:
    exit('please command pdf file name')
pdf_path = sys.argv[1]

if not os.path.exists(pdf_path):
    exit('there is no file: {}'.format(pdf_path))
src_pdf = pypdf.PdfReader(pdf_path)
for i, page in enumerate(src_pdf.pages):
    dst_pdf = pypdf.PdfWriter()
    dst_pdf.add_page(page)
    dst_path = pdf_path[:-4] + '_{}.pdf'.format(i)
    dst_pdf.write(dst_path)

for i in range(len(src_pdf.pages)):
    imgs = convert_from_path(pdf_path[:-4] + '_{}.pdf'.format(i))
    for img in imgs:
        img.save(pdf_path[:-4] + '_{}.png'.format(i), 'png', resolution=300)
    os.remove(pdf_path[:-4] + '_{}.pdf'.format(i))
