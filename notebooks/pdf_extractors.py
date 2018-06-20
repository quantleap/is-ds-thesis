
# coding: utf-8

# # PDF Extractors
# 
# There are a variety of PDF text extractors and most are based on a limited number of underlying engines:
# 
# The engines:
# -	PDF Box https://pdfbox.apache.org/ used by Tika
# -	xPDF http://www.xpdfreader.com/ used by command line utilities **pdftotext** and **pdftohtml**
# -	PDF Miner http://www.unixuser.org/~euske/python/pdfminer/pure python 20x slower than xPDF
# -	Poppler https://poppler.freedesktop.org/  Poppler is a fork of Xpdf-3.0
# -   PyPDF2 https://github.com/mstamy2/PyPDF2 
# 
# Other Python libraries:
# - pdftotext https://github.com/jalan/pdftotext wrapper for the command line utility (no options)
# - PyPDF http://pyfpdf.readthedocs.io/en/latest/#support   
# - pyPoppler https://launchpad.net/poppler-python
# - pdfrw https://github.com/pmaupin/pdfrw
# - PyPDF2 fix for endless loop sekrause:fast-inline-images - PR: https://github.com/mstamy2/PyPDF2/pull/331
# 

# In[1]:


import os
report_path = os.path.join(os.getcwd(), '../data/report_met_issues/01_obr_13_293_F_V_09.pdf')
os.path.isfile(report_path)


# ## classification of PDF: scanned or converted
# To classify a PDF file 

# In[2]:


def is_scanned_pdf(file_path):
    """
    classify if pdf is ocr-ed (consists of scanned pages) or non-ocr-ed (converted to pdf from text editor)
    @return true for ocr-ed, false otherwise
    """
    # with PyPDF2: pdf is classified as ocr when first page does not contain any text
    fp = open(file_path, 'rb')
    document = PdfFileReader(fp)
    page1 = document.getPage(1)
    is_ocr = (page1.extractText() == '')
    return is_ocr


# results: Classification should result in three classes:
# 1. only pictures (TIFFs)
# 2. only text
# 3. both pictures and overlayed text
# 
# The latter category poses some difficulties as the text might deviate from the pictures as it is OCR-ed with some errors. Re-OCR-ing with Tesseract will help with some errors but is not without newly introduced errors itself. By storing the classification an optimal processing choice can be made.

# ## PDFMiner

# In[3]:


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage

from io import StringIO

def pdf_to_txt_pdfminer(file_path):
    """
    uses pdf miner to convert a non-ocr-ed pdf into text
    """
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(file_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    as_string = retstr.getvalue()
    retstr.close()
    return as_string


# In[4]:


print(pdf_to_txt_pdfminer(report_path))


# Results: 
# - good: line breaks
# - bad: misinterpreting table structure for two column structure, important for extracting parameters. THIS STRUCTURE / TEXT FLOW IS ALSO APPARENT WHEN SELECTING TEXT
# - bad: slashes in 'C/01/13/293' F become clo'v131293F - SAME HAPPENS WHEN I COPY AND PASTE FROM PDF
# - bad: 'tekst vetged ru kt weergegeven' - SAME COPY&PASTE
# 
# quote from documentation on the text extract function:
# 
# "Locate all text drawing commands, in the order they are provided in the content stream, and extract the text. This works well for some PDF files, but poorly for others, depending on the generator used. This will be refined in the future. Do not rely on the order of text coming out of this function, as it will change if this function is made more sophisticated."
# 
# De misgeinterpreteerde tekst wordt veroorzaakt door een verkeerde of slechte OCR. In dit geval Canon iR-ADV C5235  PDF. DIT PROCES RESULTEERT IN EEN PDF DIE BESTAAT UIT PLAATJES MET DAAROVER ONZICHTBARE TEKST. Je ziet het plaatje en selecteert de onzichtbare tekst, dit leidt tot de copy&paste fouten.
# 
# Indicatie hiervan zit in de meta informatie die met pdftotext te extraheren is. Dit veld, voorbeeld <meta name="Creator" content="Canon iR-ADV C5235  PDF"/> kunnen we meenemen en opslaan voor latere optimalisatie van OCR methode.
# 
# Ook opslaan is de pdf classificatie: [image only/text only/text and images] - de derde optie is er nu nog niet en deze klasse zou opnieuw ge-OCR-ed kunnen worden.
# 
# 
# 
# source: https://pythonhosted.org/PyPDF2/PageObject.html

# ## PyPDF2

# In[5]:


import PyPDF2
pdfFileObj = open(report_path, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
content = ''
for i in range(pdfReader.numPages):
    pageObj = pdfReader.getPage(i)
    content += pageObj.extractText()
print(content)


# Results:
# - bad: no linebreaks, missing structure

# ## pdftotext
# ### command-line using popen - with layout and htmlmeta options enabled

# In[6]:


# convert pdf
exec_path = r'/usr/local/bin/pdftotext'
options = '-layout -htmlmeta'
to_stdout = '-'
command = ' '.join([exec_path, options, report_path, to_stdout])
report_content = os.popen(command).read()
print(report_content)


# Results:
# - very good: keeps the proper column format (only when using the -layout option)
# - bad: same text issues - reason below 
# - good: additional meta data, but not very important
# 
# "Fonts in PDF files are stored with two tables, one contains the glyphs (the character shapes) and one contains a "toUnicode" map, which says what character each glyph represents. Acrobat uses the first table to draw the page, so it doesn't actually know what the text "says", only which patterns of shapes to draw. When you copy or search the file, the second lookup table is used to work out what the text says"
# 
# use pdffonts

# ### using pdftotext pyton package

# In[7]:


import pdftotext
with open(report_path, "rb") as f:
    pdf = pdftotext.PDF(f)

print('\n\n'.join(pdf))


# ## pdftohtml

# In[8]:


# convert pdf
exec_path = r'/usr/local/bin/pdftohtml'
options = ''
os.system(' '.join([exec_path, options, report_path]))


# # pdfrw

# In[9]:


import pdfrw
from pdfrw import PdfReader
pdf = PdfReader(report_path)
#pdf.keys()
pdf.Info
#pdf.Root.keys()


# result: not text extract and tags not user friendly

# In[ ]:





# In[ ]:




