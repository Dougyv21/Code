# LIBS #
import pandas
import getpass
import os
import shutil
import tkinter
import glob
import datetime
import functools
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Utility #
Username = getpass.getuser()
Date = datetime.date.today()
FileDate = format(Date, '%m.%d.%y')

# File Paths #
UserFolder = rf'C:\Users\{Username}\OneDrive - RSM\JF\Misc'

EmailPath = rf'C:\Users\{Username}\ALDI-HOFER\Network Planning - Documents\Team Folders\Data Team\Projects\3PW Projects\3PW Inventory\Inputs\Email List.xlsx'
InventoryOutputFolder = rf'C:\Users\{Username}\ALDI-HOFER\Network Planning - Documents\Team Folders\Data Team\Projects\3PW Projects\3PW Inventory\Inventory Sheets'
POOutputFolder = f'C:\\Users\\{Username}\\ALDI-HOFER\\Network Planning - Documents\\Team Folders\\3PW Team\\PO Reporting\\Inputs'
Inbox = 'NSCMMonitoring'
NewInbox = r'\\NSCMMonitoring\Inbox\3PW'
DownloadsFolder = rf'C:\Users\{Username}\Downloads'
DATFolder = rf'C:\Users\{Username}\ALDI-HOFER\Network Planning - Documents\Team Folders\Data Team\Projects\3PW Projects\3PW Network Analysis\Inputs'

# Web Automation Utility #
CD = rf'C:\Users\{Username}\ALDI-HOFER\Network Planning - Documents\Team Folders\Data Team\Data Tools\Python\Additional Libraries\chromedriver.exe'
AMCURL = r'https://www.i-3pl.com/login?ReturnUrl=%2fDefault.aspx#/'
WoodsURL = r'https://global.secure-wms.com/webui/login?callbackUri=https://global.secure-wms.com/smartui/&tplguid=%7bad6ed8de-a0a4-4065-8fa3-a37b2eddd949%7d'
DATURL = r'https://rateview.dat.com/app/login.html#/'

# Web Credentials #

# Create Folder #
def create_folder():  
    
    # Placing Root on top of everything #
    StatusWindow = tkinter.Toplevel(Canvas)
    StatusWindow.lift()
    StatusWindow.attributes('-topmost', True)
    
    # Header Label #
    Header = tkinter.Label(StatusWindow, text = 'Creating folder..')
    Header.pack()
    
    # Creating folder #
    NewFolder = os.path.join(UserFolder, f'{Username} - {Date}')
    os.mkdir(NewFolder)
    
    # Close status window when finshed #       
    StatusWindow.destroy()

# Copy file from download folder #
def copy_file(current_file_name, new_file_name, output_folder):
    
    # Validating file is current #
    Files = glob.glob(os.path.join(DownloadsFolder, current_file_name))
    for File in Files:
        FileDate = datetime.datetime.fromtimestamp(os.path.getmtime(File))
        FileDate = format(FileDate, '%Y-%m-%d')
        if FileDate == str(Date):
            break
    
    # Copying File #
    print(f'\nCopying file from {os.path.join(DownloadsFolder, File)} to {os.path.join(output_folder, new_file_name)}')
    shutil.copy(os.path.join(DownloadsFolder, File), os.path.join(output_folder, new_file_name))
    print('File copied successfully.')

# Open Folder #    
def open_folder():
    
    PathObj = os.path.realpath(os.path.join(UserFolder, f'{getpass.getuser()} - {Date}'))
    os.startfile(PathObj)
    
# Woods Inventory #
def woods_inventory():
    
    # Close Browser #
    def close_browser():
        print('\nClosing browser..')
        Browser.close()
        print('Browser closed without issues.')
            
    # Placing Root on top of everything #
    CloseWindow = tkinter.Toplevel(Canvas)
    CloseWindow.lift()
    CloseWindow.attributes('-topmost', True)
    
    # App Title #
    CloseWindow.title('Woods Inventory')
    
    # Copy Inventory File Button #
    CopyFile = tkinter.Button(CloseWindow, text = 'Copy Inventory File', command = functools.partial(copy_file, current_file_name = 'Pallets per SKU*.xlsx', new_file_name = 'Woods Inventory.xlsx', output_folder = InventoryOutputFolder), bg = 'brown', fg = 'white', font = ('arial', 9, 'bold'))
    CopyFile.pack()
    
    # Copy Upcoming POs File Button #
    CopyFile = tkinter.Button(CloseWindow, text = 'Copy PO File', command = functools.partial(copy_file, current_file_name = 'OpenOrders*.xlsx', new_file_name = 'Woods Planned POs.xlsx', output_folder = POOutputFolder), bg = 'brown', fg = 'white', font = ('arial', 9, 'bold'))
    CopyFile.pack()
    
    # Close Browser Button #
    CloseBrowser = tkinter.Button(CloseWindow, text = 'Close Browser', command = close_browser, bg = 'brown', fg = 'white', font = ('arial', 9, 'bold'))
    CloseBrowser.pack()
    
    # Open Browser #
    print('\nStarting browser..')
    Browser = webdriver.Chrome(CD)
    Browser.maximize_window()
    
    # Open Login Page #
    print('Logging into Woods System..')
    if Browser.title == '':
        Browser.get(WoodsURL)
    else:
        Browser.execute_script(f'window.open("{WoodsURL}");')
    
    # Logging into Woods 3PL Central #

    # Logging In #
    Browser.find_element_by_class_name('wms-btn').click()
    
    # Navigate to Report Page #
    Browser.find_element_by_id('wms_Report').click()

# DAT Data Upload #    
def DAT_upload():
    
    # Close Browser #
    def close_browser():
        print('\nClosing browser..')
        Browser.close()
        print('Browser closed without issues.')

    # Placing Root on top of everything #
    CloseWindow = tkinter.Toplevel(Canvas)
    CloseWindow.lift()
    CloseWindow.attributes('-topmost', True)
    
    # App Title #
    CloseWindow.title('DAT Upload')
    
    # Copy DAT Data to folder #
    CopyFile = tkinter.Button(CloseWindow, text = 'Copy DAT File', command = functools.partial(copy_file, current_file_name = 'DAT Data Request*.csv', new_file_name = f'NWP DAT Rates {FileDate}.csv', output_folder = DATFolder), bg = 'brown', fg = 'white', font = ('arial', 9, 'bold'))
    CopyFile.pack()
        
    # Close Browser Button #
    CloseBrowser = tkinter.Button(CloseWindow, text = 'Close Browser', command = close_browser, bg = 'brown', fg = 'white', font = ('arial', 9, 'bold'))
    CloseBrowser.pack()    
    
    # Open Browser #
    print('\nStarting browser..')
    Browser = webdriver.Chrome(CD)
    Browser.maximize_window()
    
    # Open Login Page #
    print('Logging into DAT system..')
    if Browser.title == '':
        Browser.get(DATURL)
    else:
        Browser.execute_script(f'window.open("{DATURL}");')
    
    # Logging into DAT System #
   
    # Logging In #
    Browser.find_element_by_class_name('mat-button-wrapper').click()
    
    # Selecting Multi Lane #
    try:
        Browser.find_element_by_class_name(r'multilane product-tab').click()
    except NoSuchElementException:
        print('Multi-lane tab already selected..')
    
    # Clicking upload button #
    Browser.find_element_by_id('uploadBtn').click()
        
# Creating Root #
Root = tkinter.Tk()

# Placing Root on top of everything #
Root.lift()
Root.attributes('-topmost', True)

# App Title #
Root.title('Testing')

# Creating Canvas #
Canvas = tkinter.Canvas(Root, width = 300, height = 100,  relief = 'raised')
Canvas.pack()

# Header Label #
Header = tkinter.Label(Root, text = 'Select a Process to Run')
Header.config(font = ('arial', 10, 'bold'))
Canvas.create_window(150, 20, window = Header)

# Create Folder Button #    
CreateFolder = tkinter.Button(text = 'Create Input Folder', command = create_folder, bg = 'brown', fg = 'white', font = ('arial', 9, 'bold'))
Canvas.create_window(75, 50, window = CreateFolder)

# Open Folder Button #
OpenFolder = tkinter.Button(text = 'Open Folder', command = open_folder, bg = 'brown', fg = 'white', font = ('arial', 9, 'bold'))
Canvas.create_window(225, 50, window = OpenFolder)

# Woods Inventory Button #    
WoodsInventory = tkinter.Button(text = 'Coming Soon', command = woods_inventory, bg = 'brown', fg = 'white', font = ('arial', 9, 'bold'))
Canvas.create_window(75, 85, window = WoodsInventory)

# DAT Upload Button #
DATUpload = tkinter.Button(text = 'Coming Soon', command = DAT_upload, bg = 'brown', fg = 'white', font = ('arial', 9, 'bold'))
Canvas.create_window(225, 85, window = DATUpload)

# Actually Start Window #
Root.mainloop()