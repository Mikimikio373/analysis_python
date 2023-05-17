import os
import pypdf

base_path = '/Users/minamihideyuki/data/univercity_document'
file_name = 'IMAGE.pdf'
path = os.path.join(base_path, file_name)
if not os.path.exists(path):
    exit('there is no file: {}'.format(path))
src_pdf = pypdf.PdfReader(path)
for i, page in enumerate(src_pdf.pages):
    dst_pdf = pypdf.PdfWriter()
    dst_pdf.add_page(page)
    dst_path = os.path.join(base_path, file_name[:-4] + '_{}.pdf'.format(i))
    dst_pdf.write(dst_path)