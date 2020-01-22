#--------------------------------------------------#
# Project Name: GBA Rom Checker                    #
# Filename:     N64RomChecker.py                   #
# Author:       Dorian Pilorge                     #
#--------------------------------------------------#


# Libraries #
import binascii
import os.path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


# Fonctions #
def openFile(LoadedROM):
    if LoadedROM == 'new':
        LoadedROM = filedialog.askopenfilename(initialdir='/', title='Select a ROM', filetypes=(('GBA Roms', '*.gba'), ('All', '*')))

    with open(LoadedROM, 'rb') as f:
        #loading(1)
        ROM = f.read()
        f.seek(0)
        ROMFilename = os.path.basename(LoadedROM)
        ROMExtension = os.path.splitext(LoadedROM)[1]
        #loading(0)

        # Get ROM Informations #
        try:
            ROMFiletype = checkROMType(ROMExtension)
            ROMSize = checkROMSize(LoadedROM)
            ROMName = checkROMName(LoadedROM, ROMExtension)
            ROMCartID = checkROMCartID(ROM, ROMExtension)
            ROMRegion = checkROMRegion(ROM, ROMExtension)
            ROMVersion = checkROMVersion(ROM, ROMExtension)
            ROMManufacturer = checkROMManufacturer(ROM, ROMExtension)
            ROMCRC = checkROMCRC(ROM, ROMExtension)
        except:
            ROMFiletype = 'Unsupported (not a GBA ROM!)'
            ROMSize = ''
            ROMName = ''
            ROMCartID = ''
            ROMRegion = ''
            ROMVersion = ''
            ROMManufacturer = ''
            ROMCRC = ''

        # Display available "ROM Tweaks" for loaded ROM #
        global TweakFrame

        if TweakFrame.winfo_exists():
            TweakFrame.destroy()

        TweakFrame = LabelFrame(MainWindow, text='ROM Tweaks', padx=5, pady=5)
        TweakFrame.pack(fill='x', expand='no')


    # Fill "ROM Informations" with loaded ROM
    Filename['text'] = ROMFilename
    Filetype['text'] = ROMFiletype
    Size['text'] = ROMSize
    Name['text'] = ROMName
    CartID['text'] = ROMCartID
    Region['text'] = ROMRegion
    Version['text'] = ROMVersion
    Manufacturer['text'] = ROMManufacturer
    CRC['text'] = ROMCRC

    # Console Debug: Loaded ROM Infos #
    print('\nROM INFORMATIONS')
    print('Loaded file: ', ROMFilename)
    print('ROM Type: ', ROMFiletype)
    print('ROM Size: ', ROMSize)
    print('ROM Name: ', ROMName)
    print('ROM Cartridge ID: ', ROMCartID)
    print('ROM Region: ', ROMRegion)
    print('ROM Version: ', ROMVersion)
    print('ROM Manufacturer: ', ROMManufacturer)
    print('ROM CRC: ', ROMCRC)


def checkROMType(ROMExtension):
    if ROMExtension == '.gba':
        ROMFiletype = 'Game Boy Advance'
    else:
        ROMFiletype = 'Unknown'

    return ROMFiletype


def checkROMSize(LoadedROM):
    ROMSize = os.path.getsize(LoadedROM)
    if ROMSize <= 8388608:
        ROMSize = '8 MB'
    elif ROMSize <= 12582912:
        ROMSize = '12 MB'
    elif ROMSize <= 16777216:
        ROMSize = '16 MB'
    elif ROMSize <= 33554432:
        ROMSize = '32 MB'
    else:
        ROMSize = '> 32 MB (ROM size is too big!)'

    return ROMSize


def checkROMName(LoadedROM, ROMExtension):
    with open(LoadedROM, 'rb') as f:
        f.seek(160)
        ROMName = f.read(12)

    if ROMExtension == '.gba':
        pass
    else:
        ROMName = 'Unknown'

    ROMName = ROMName.decode()

    return ROMName.rstrip()


def checkROMCartID(ROM, ROMExtension):
    if ROMExtension == '.gba':
        ROMCartID = chr(ROM[172]), chr(ROM[173]), chr(ROM[174]), chr(ROM[175])
    else:
        ROMCartID = 'Unknown'

    ROMCartID = re.sub('[^A-Za-z0-9]+', '', str(ROMCartID))

    return ROMCartID


def checkROMRegion(ROM, ROMExtension):
    if ROMExtension == '.gba':
        x = 175

    if chr(ROM[x]) == 'D':
        ROMRegion = 'German (Pokémon)'
    elif chr(ROM[x]) == 'E':
        ROMRegion = 'American (NTSC-U) / English (Pokémon)'
    elif chr(ROM[x]) == 'F':
        ROMRegion = 'French (Pokémon)'
    elif chr(ROM[x]) == 'I':
        ROMRegion = 'Italian (Pokémon)'
    elif chr(ROM[x]) == 'J':
        ROMRegion = 'Japanese (NTSC-J)'
    elif chr(ROM[x]) == 'K':
        ROMRegion = 'Korean (NTSC-K)'
    elif chr(ROM[x]) == 'P':
        ROMRegion = 'European (PAL)'
    elif chr(ROM[x]) == 'S':
        ROMRegion = 'Spanish (Pokémon)'
    else:
        ROMRegion = 'Unknown'

    return ROMRegion


def checkROMManufacturer(ROM, ROMExtension):
    if ROMExtension == '.gba':
        ROMManufacturer = chr(ROM[176]), chr(ROM[177])
    else:
        ROMManufacturer = 'Unknown'

    ROMManufacturer = re.sub('[^A-Za-z0-9]+', '', str(ROMManufacturer))

    if ROMManufacturer == '01':
        ROMManufacturer = 'Nintendo'
    elif ROMManufacturer == '02':
        ROMManufacturer = 'Rocket Games'
    elif ROMManufacturer == '03':
        ROMManufacturer = 'Imagineer-Zoom'
    elif ROMManufacturer == '04':
        ROMManufacturer = 'Gray Matter'
    elif ROMManufacturer == '05':
        ROMManufacturer = 'Zamuse'
    elif ROMManufacturer == '06':
        ROMManufacturer = 'Falcom'
    else:
        ROMManufacturer = 'Unknown'

    return ROMManufacturer


def checkROMVersion(ROM, ROMExtension):
    if ROMExtension == '.gba':
        x = 188

    ROMVersion = ROM[x]
    ROMVersion = 'v1.', ROMVersion
    ROMVersion = re.sub('[^A-Za-z0-9.]+', '', str(ROMVersion))

    return ROMVersion


def checkROMCRC(ROM, ROMExtension):
    if ROMExtension == '.gba':
        x = 189

    ROMCRC = hex(ROM[x])[2:].upper()

    return ROMCRC


def openTools(tool):
    try:
        os.startfile('..\\' + tool + '\\' + tool + '.exe')
        MainWindow.destroy()
    except:
        messagebox.showerror('Error', '\nCan\'t find "' + tool + '" folder!')
        print('\n[MessageBox] Can\'t find "' + tool + '" folder!')


def showOffsets(flag):
    if flag:
        TitleOffset['text'] = 'Start'
        NameOffset['text'] = ' 0xA0 '
        CartIDOffset['text'] = ' 0xAC '
        RegionOffset['text'] = ' 0xAF '
        ManufacturerOffset['text'] = ' 0xB0 '
        VersionOffset['text'] = ' 0xBC '
        CRCOffset['text'] = ' 0xBD '

        TitleLength['text'] = 'Length'
        NameLength['text'] = ' 0x0C '
        CartIDLength['text'] = ' 0x04 '
        RegionLength['text'] = ' 0x01 '
        ManufacturerLength['text'] = ' 0x02 '
        VersionLength['text'] = ' 0x01 '
        CRCLength['text'] = ' 0x01 '
    else:
        TitleOffset['text'] = ''
        NameOffset['text'] = ''
        CartIDOffset['text'] = ''
        RegionOffset['text'] = ''
        ManufacturerOffset['text'] = ''
        VersionOffset['text'] = ''
        CRCOffset['text'] = ''

        TitleLength['text'] = ''
        NameLength['text'] = ''
        CartIDLength['text'] = ''
        RegionLength['text'] = ''
        ManufacturerLength['text'] = ''
        VersionLength['text'] = ''
        CRCLength['text'] = ''


def about():
    AboutWindow = Toplevel(MainWindow)
    AboutWindow.title('About')
    AboutWindow.geometry('240x200')
    AboutWindow.iconbitmap('./icons/gba.ico')
    AboutWindow.resizable(width=False, height=False)

    Image = PhotoImage(file='./images/about.ppm')
    Image = Image.subsample(4)
    AboutImage = Label(AboutWindow, anchor='n', image=Image)
    AboutImage.pack(padx=5, pady=5)
    AboutImage.image = Image

    AboutText = Label(AboutWindow, text='GBA Rom Checker\nVersion 1.0\nMade by Natsu235')
    AboutText.pack(padx=5, pady=5)


def loading(flag):
    global LoadingWindow

    if flag:
        MainWindow.attributes("-disabled", True)
        LoadingWindow = Toplevel(MainWindow)
        LoadingWindow.title('Loading ROM')
        LoadingWindow.geometry('280x120')
        LoadingWindow.iconbitmap('./icons/gba.ico')
        LoadingWindow.resizable(width=False, height=False)

        LoadingText = Label(LoadingWindow, text='Loading GBA ROM... Please wait.')
        LoadingText.pack(padx=10, pady=10)

        ProgressBar = ttk.Progressbar(LoadingWindow, mode='indeterminate', length='200')
        ProgressBar.pack(padx=10, pady=10)
        ProgressBar.start()
    else:
        MainWindow.attributes("-disabled", False)
        LoadingWindow.destroy()


# Main Window #
MainWindow = Tk()
MainWindow.title('GBA Rom Checker v1.0')
MainWindow.geometry('700x640')
MainWindow.iconbitmap('./icons/gba.ico')
MainWindow.resizable(width=False, height=False)
MainWindow.bind('<Control-o>', lambda event: openFile('new'))


# Main Window Elements #
InfoFrame = LabelFrame(MainWindow, text='ROM Informations', padx=5, pady=5)
InfoFrame.pack(fill='x', expand='no')

ROMFilenameLabel = Label(InfoFrame, text='Filename: ')
ROMFiletypeLabel = Label(InfoFrame, text='Filetype: ')
ROMSizeLabel = Label(InfoFrame, text='Rom Size: ')
ROMNameLabel = Label(InfoFrame, text='Rom Name: ')
ROMCartIDLabel = Label(InfoFrame, text='Rom Cartridge ID: ')
ROMRegionLabel = Label(InfoFrame, text='Rom Region: ')
ROMManufacturerLabel = Label(InfoFrame, text='Rom Manufacturer: ')
ROMVersionLabel = Label(InfoFrame, text='Rom Version: ')
ROMCRCLabel = Label(InfoFrame, text='Rom CRC: ')
ROMFilenameLabel.grid(row=1, column=0, sticky='nw')
ROMFiletypeLabel.grid(row=2, column=0, sticky='nw')
ROMSizeLabel.grid(row=3, column=0, sticky='nw')
ROMNameLabel.grid(row=4, column=0, sticky='nw')
ROMCartIDLabel.grid(row=5, column=0, sticky='nw')
ROMRegionLabel.grid(row=6, column=0, sticky='nw')
ROMManufacturerLabel.grid(row=7, column=0, sticky='nw')
ROMVersionLabel.grid(row=8, column=0, sticky='nw')
ROMCRCLabel.grid(row=9, column=0, sticky='nw')

TitleOffset = Label(InfoFrame, text='')
FilenameOffset = Label(InfoFrame, text='', fg='cyan2')
FiletypeOffset = Label(InfoFrame, text='', fg='cyan2')
SizeOffset = Label(InfoFrame, text='', fg='cyan2')
NameOffset = Label(InfoFrame, text='', fg='cyan2')
CartIDOffset = Label(InfoFrame, text='', fg='cyan2')
RegionOffset = Label(InfoFrame, text='', fg='cyan2')
ManufacturerOffset = Label(InfoFrame, text='', fg='cyan2')
VersionOffset = Label(InfoFrame, text='', fg='cyan2')
CRCOffset = Label(InfoFrame, text='', fg='cyan2')
TitleOffset.grid(row=0, column=1, sticky='nw')
FilenameOffset.grid(row=1, column=1, sticky='nw')
FiletypeOffset.grid(row=2, column=1, sticky='nw')
SizeOffset.grid(row=3, column=1, sticky='nw')
NameOffset.grid(row=4, column=1, sticky='nw')
CartIDOffset.grid(row=5, column=1, sticky='nw')
RegionOffset.grid(row=6, column=1, sticky='nw')
ManufacturerOffset.grid(row=7, column=1, sticky='nw')
VersionOffset.grid(row=8, column=1, sticky='nw')
CRCOffset.grid(row=9, column=1, sticky='nw')

TitleLength = Label(InfoFrame, text='')
FilenameLength = Label(InfoFrame, text='', fg='magenta2')
FiletypeLength = Label(InfoFrame, text='', fg='magenta2')
SizeLength = Label(InfoFrame, text='', fg='magenta2')
NameLength = Label(InfoFrame, text='', fg='magenta2')
CartIDLength = Label(InfoFrame, text='', fg='magenta2')
RegionLength = Label(InfoFrame, text='', fg='magenta2')
ManufacturerLength = Label(InfoFrame, text='', fg='magenta2')
VersionLength = Label(InfoFrame, text='', fg='magenta2')
CRCLength = Label(InfoFrame, text='', fg='magenta2')
TitleLength.grid(row=0, column=2, sticky='nw')
FilenameLength.grid(row=1, column=2, sticky='nw')
FiletypeLength.grid(row=2, column=2, sticky='nw')
SizeLength.grid(row=3, column=2, sticky='nw')
NameLength.grid(row=4, column=2, sticky='nw')
CartIDLength.grid(row=5, column=2, sticky='nw')
RegionLength.grid(row=6, column=2, sticky='nw')
ManufacturerLength.grid(row=7, column=2, sticky='nw')
VersionLength.grid(row=8, column=2, sticky='nw')
CRCLength.grid(row=9, column=2, sticky='nw')

Filename = Label(InfoFrame, text='', fg='gray15')
Filetype = Label(InfoFrame, text='', fg='gray15')
Size = Label(InfoFrame, text='', fg='gray15')
Name = Label(InfoFrame, text='', fg='gray15')
CartID = Label(InfoFrame, text='', fg='gray15')
Region = Label(InfoFrame, text='', fg='gray15')
Manufacturer = Label(InfoFrame, text='', fg='gray15')
Version = Label(InfoFrame, text='', fg='gray15')
CRC = Label(InfoFrame, text='', fg='gray15')
Filename.grid(row=1, column=3, sticky='nw')
Filetype.grid(row=2, column=3, sticky='nw')
Size.grid(row=3, column=3, sticky='nw')
Name.grid(row=4, column=3, sticky='nw')
CartID.grid(row=5, column=3, sticky='nw')
Region.grid(row=6, column=3, sticky='nw')
Manufacturer.grid(row=7, column=3, sticky='nw')
Version.grid(row=8, column=3, sticky='nw')
CRC.grid(row=9, column=3, sticky='nw')

TweakFrame = LabelFrame()
TweakFrame.pack(fill='x', expand='no')


# Main Window Navbar #
Navbar = Menu(MainWindow)

# Navbar "File" Tab #
FileMenu = Menu(Navbar, tearoff=0)
FileMenu.add_command(label='Open ROM', accelerator='Ctrl+O', command=lambda: openFile('new'))
FileMenu.add_separator()
FileMenu.add_command(label='NDS Rom Checker', command=lambda: openTools('NDSRomChecker'))
FileMenu.add_command(label='N64 Rom Checker', command=lambda: openTools('N64RomChecker'))
FileMenu.add_separator()
FileMenu.add_command(label='Exit', command=MainWindow.destroy)
Navbar.add_cascade(label='File', menu=FileMenu)

# Navbar "Options" Tab #
OptionsMenu = Menu(Navbar, tearoff=0)
OptionsMenu.flag1 = IntVar()
OptionsMenu.add_checkbutton(label='Show Offsets', variable=OptionsMenu.flag1, command=lambda: showOffsets(OptionsMenu.flag1.get()))
Navbar.add_cascade(label='Options', menu=OptionsMenu)

# Navbar "Help" Tab #
HelpMenu = Menu(Navbar, tearoff=0)
HelpMenu.add_command(label='About', command=about)
Navbar.add_cascade(label='Help', menu=HelpMenu)

MainWindow.config(menu=Navbar)


# Main Window Builder #
MainWindow.mainloop()
