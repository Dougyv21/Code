import zipfile
import os


FilesToExclude = ['COGS Other Jan-21 Purchase Invoices 338320 5.pdf']

with zipfile.ZipFile(os.path.join(Folder, 'PDFs.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
    for File in FilesToExclude:
        zipf.write(os.path.join(Folder, File), arcname = os.path.join('Unprocessed', File))


Folder = r'\\AZDEVALTYXENT01\AlteryxDevShare\Reversals\Output\Jason Sub Folder TEST'
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

with zipfile.ZipFile('Python Test 2.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(Folder, zipf)



import shutil
shutil.make_archive(os.path.join(Folder, 'ZipFolder'), 'zip', base_dir = Folder)
