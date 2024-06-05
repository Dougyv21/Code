# PDF to Text Converter #
def pdf_to_text(pdf_path, tesseract = None, poppler = None):
    
    # Libs #
    import pytesseract
    import pandas
    from pdf2image import convert_from_path
    
    # Deps #
    if tesseract is not None:  
        pytesseract.pytesseract.tesseract_cmd = tesseract
    if poppler is not None:
        pop_bin = poppler
    
    # Convert pdf path to list if needed #   
    if isinstance(pdf_path, str):
        list(pdf_path)
    
    # Init blank DF #
    df = pandas.DataFrame()
    
    # Loop for all pdfs in folder path #
    for pdf in pdf_path:
    
        # Convert PDF to images using pdf2image
        images = convert_from_path(pdf, poppler_path = pop_bin)
        
        # Create an empty list to store extracted data
        data = []
        
        # Iterate through images and perform OCR
        for page_num, img in enumerate(images, start=1):
            text = pytesseract.image_to_string(img, lang='eng')  # 'eng' specifies the English language
            
            # Split 'text' into lines (rows) and filter out empty rows
            rows = [row for row in text.split('\n') if row.strip()]
            
            for row_num, row in enumerate(rows, start=1):
                
                # Append data to the list
                data.append({'FilePath': pdf, 'PageNumber': page_num, 'RowNumber': row_num, 'Text': row})
                
        
        # Add df for each pdf before end of file loop #
        df = pandas.concat([df, pandas.DataFrame(data)], ignore_index = True)
    
    # return df of all files #
    return df

# Dep paths #
TesseractPath = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
PopplerPath = r'C:\Program Files\poppler\bin'

# PDF Paths #
PDFs = [r'C:\Users\E097052\RSM\Audit Innovation - Documents\Software\Python\Testing\Example FRB Report.pdf']

# Convert PDFs #
DF = pdf_to_text(PDFs, tesseract = TesseractPath, poppler = PopplerPath)