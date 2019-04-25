#-----------------------------------------------------------#
# Project Name: NDS Rom Checker                             #
# Filename:     NDSRomChecker.py                                     #
# Author:       Dorian Pilorge                              #
#-----------------------------------------------------------#


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
        LoadedROM = filedialog.askopenfilename(initialdir='/', title='Select a ROM', filetypes=(('NDS Roms', '*.nds'), ('All', '*')))

    with open(LoadedROM, 'rb') as f:
        #loading(1)
        ROM = f.read()
        f.seek(0)
        ROMFilename = os.path.basename(LoadedROM)
        ROMExtension = os.path.splitext(LoadedROM)[1]
        #loading(0)

        # Get ROM Informations #
        try:
            ROMFiletype = checkROMType(ROM, ROMExtension)
            ROMSize = checkROMSize(LoadedROM)
            ROMName = checkROMName(LoadedROM, ROMExtension)
            ROMCartID = checkROMCartID(ROM, ROMExtension)
            ROMRegion = checkROMRegion(ROM, ROMExtension)
            ROMVersion = checkROMVersion(ROM, ROMExtension)
            ROMManufacturer = checkROMManufacturer(ROM, ROMExtension)
            ROMHeaderCRC = checkROMCRC(LoadedROM)
        except:
            ROMFiletype = 'Unsupported (not a NDS ROM!)'
            ROMSize = ''
            ROMName = ''
            ROMCartID = ''
            ROMRegion = ''
            ROMVersion = ''
            ROMManufacturer = ''
            ROMHeaderCRC = ''

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
    HeaderCRC['text'] = ROMHeaderCRC

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
    print('ROM Header CRC: ', ROMHeaderCRC)


def checkROMType(ROM, ROMExtension):
    if ROMExtension == '.nds':
        x = 18

    ROMFiletype = ROM[x]

    if ROMFiletype == 0:
        ROMFiletype = 'Nintendo DS'
    elif ROMFiletype == 1:
        ROMFiletype = 'Nintendo DSi Only'
    elif ROMFiletype == 2:
        ROMFiletype = 'Nintendo DSi Enhanced'
    elif ROMFiletype == 3:
        ROMFiletype = 'Nintendo DSi Only'
    else:
        ROMFiletype = 'Unknown'

    return ROMFiletype


def checkROMSize(LoadedROM):
    ROMSize = os.path.getsize(LoadedROM)
    if ROMSize <= 8388608:
        ROMSize = '8 MB'
    elif ROMSize <= 16777216:
        ROMSize = '16 MB'
    elif ROMSize <= 33554432:
        ROMSize = '32 MB'
    elif ROMSize <= 67108864:
        ROMSize = '64 MB'
    elif ROMSize <= 134217728:
        ROMSize = '128 MB'
    elif ROMSize <= 268435456:
        ROMSize = '256 MB'
    elif ROMSize <= 536870912:
        ROMSize = '512 MB'
    else:
        ROMSize = '> 512 MB (ROM size is too big!)'

    return ROMSize


def checkROMName(LoadedROM, ROMExtension):
    with open(LoadedROM, 'rb') as f:
        f.seek(0)
        ROMName = f.read(12)

    if ROMExtension == '.nds':
        pass
    else:
        ROMName = 'Unknown'

    ROMName = ROMName.decode()

    return ROMName.rstrip()


def checkROMCartID(ROM, ROMExtension):
    if ROMExtension == '.nds':
        ROMCartID = chr(ROM[12]), chr(ROM[13]), chr(ROM[14]), chr(ROM[15])
    else:
        ROMCartID = 'Unknown'

    ROMCartID = re.sub('[^A-Za-z0-9]+', '', str(ROMCartID))

    return ROMCartID


def checkROMRegion(ROM, ROMExtension):
    if ROMExtension == '.nds':
        x = 15

    if chr(ROM[x]) == 'E':
        ROMRegion = 'American (NTSC-U) / English (Layton & Pokémon)'
    elif chr(ROM[x]) == 'F':
        ROMRegion = 'French (Layton & Pokémon)'
    elif chr(ROM[x]) == 'J':
        ROMRegion = 'Japanese (NTSC-J)'
    elif chr(ROM[x]) == 'K':
        ROMRegion = 'Korean (NTSC-K)'
    elif chr(ROM[x]) == 'O':
        ROMRegion = 'English (Pokémon)'
    elif chr(ROM[x]) == 'P':
        ROMRegion = 'European (PAL)'
    else:
        ROMRegion = 'Unknown'

    return ROMRegion


def checkROMManufacturer(ROM, ROMExtension):
    if ROMExtension == '.nds':
        ROMManufacturer = chr(ROM[16]), chr(ROM[17])
    else:
        ROMManufacturer = 'Unknown'

    ROMManufacturer = re.sub('[^A-Za-z0-9]+', '', str(ROMManufacturer))

    if ROMManufacturer == '01':
        ROMManufacturer = 'Nintendo'
    elif ROMManufacturer == 'MV' or '99':
        ROMManufacturer = 'Rising Star Games'
    else:
        ROMManufacturer = 'Unknown'

    return ROMManufacturer


def checkROMVersion(ROM, ROMExtension):
    if ROMExtension == '.nds':
        x = 30

    ROMVersion = ROM[x]
    ROMVersion = str(ROMVersion).zfill(2)
    ROMVersion = 'v1.', ROMVersion
    ROMVersion = re.sub('[^A-Za-z0-9.]+', '', str(ROMVersion))

    return ROMVersion


def checkROMCRC(LoadedROM):
    with open(LoadedROM, 'rb') as f:
        f.seek(350)
        ROMHeaderCRC = f.read(2)

    ROMHeaderCRC = binascii.hexlify(ROMHeaderCRC).upper()
    ROMHeaderCRC = ' '.join(re.findall('([0-9A-F]{2}|[0-9A-F])', str(ROMHeaderCRC)[1:]))

    return ROMHeaderCRC


def openTools(tool):
    try:
        os.startfile('..\\' + tool + '\\' + tool + '.exe')
        MainWindow.destroy()
    except:
        messagebox.showerror('Error', '\nCan\'t find "' + tool + '" folder!')
        print('\n[MessageBox]Can\'t find "' + tool + '" folder!')


def showOffsets(flag):
    if flag:
        TitleOffset['text'] = ' Start '
        NameOffset['text'] = '  0x00  '
        CartIDOffset['text'] = '  0x0C  '
        RegionOffset['text'] = '  0x0F  '
        ManufacturerOffset['text'] = '  0x10  '
        VersionOffset['text'] = '  0x1E  '
        HeaderCRCOffset['text'] = '  0x15E  '

        TitleLength['text'] = ' Length '
        NameLength['text'] = '  0x0C  '
        CartIDLength['text'] = '  0x04  '
        RegionLength['text'] = '  0x01  '
        ManufacturerLength['text'] = '  0x02  '
        VersionLength['text'] = '  0x01  '
        HeaderCRCLength['text'] = '  0x02  '
    else:
        TitleOffset['text'] = ''
        NameOffset['text'] = ''
        CartIDOffset['text'] = ''
        RegionOffset['text'] = ''
        ManufacturerOffset['text'] = ''
        VersionOffset['text'] = ''
        HeaderCRCOffset['text'] = ''

        TitleLength['text'] = ''
        NameLength['text'] = ''
        CartIDLength['text'] = ''
        RegionLength['text'] = ''
        ManufacturerLength['text'] = ''
        VersionLength['text'] = ''
        HeaderCRCLength['text'] = ''


def about():
    AboutWindow = Toplevel(MainWindow)
    AboutWindow.title('About')
    AboutWindow.geometry('240x200')
    AboutWindow.iconbitmap('./icons/nds.ico')
    AboutWindow.resizable(width=False, height=False)

    Image = PhotoImage(file='./images/about.ppm')
    Image = Image.subsample(4)
    AboutImage = Label(AboutWindow, anchor='n', image=Image)
    AboutImage.pack(padx=5, pady=5)
    AboutImage.image = Image

    AboutText = Label(AboutWindow, text='NDS Rom Checker\nVanilla Edition (v1.0)\nMade by Natsu235')
    AboutText.pack(padx=5, pady=5)


def loading(flag):
    global LoadingWindow

    if flag:
        MainWindow.attributes("-disabled", True)
        LoadingWindow = Toplevel(MainWindow)
        LoadingWindow.title('Loading ROM')
        LoadingWindow.geometry('280x120')
        LoadingWindow.iconbitmap('./icons/nds.ico')
        LoadingWindow.resizable(width=False, height=False)

        LoadingText = Label(LoadingWindow, text='Loading NDS ROM... Please wait.')
        LoadingText.pack(padx=10, pady=10)

        ProgressBar = ttk.Progressbar(LoadingWindow, mode='indeterminate', length='200')
        ProgressBar.pack(padx=10, pady=10)
        ProgressBar.start()
    else:
        MainWindow.attributes("-disabled", False)
        LoadingWindow.destroy()


# Main Window #
MainWindow = Tk()
MainWindow.title('NDS Rom Checker (Vanilla Edition 1.0)')
MainWindow.geometry('700x640')
MainWindow.iconbitmap('./icons/nds.ico')
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
ROMHeaderCRCLabel = Label(InfoFrame, text='Rom Header CRC: ')
ROMFilenameLabel.grid(row=1, column=0, sticky='nw')
ROMFiletypeLabel.grid(row=2, column=0, sticky='nw')
ROMSizeLabel.grid(row=3, column=0, sticky='nw')
ROMNameLabel.grid(row=4, column=0, sticky='nw')
ROMCartIDLabel.grid(row=5, column=0, sticky='nw')
ROMRegionLabel.grid(row=6, column=0, sticky='nw')
ROMManufacturerLabel.grid(row=7, column=0, sticky='nw')
ROMVersionLabel.grid(row=8, column=0, sticky='nw')
ROMHeaderCRCLabel.grid(row=9, column=0, sticky='nw')

TitleOffset = Label(InfoFrame, text='')
FilenameOffset = Label(InfoFrame, text='', fg='cyan2')
FiletypeOffset = Label(InfoFrame, text='', fg='cyan2')
SizeOffset = Label(InfoFrame, text='', fg='cyan2')
NameOffset = Label(InfoFrame, text='', fg='cyan2')
CartIDOffset = Label(InfoFrame, text='', fg='cyan2')
RegionOffset = Label(InfoFrame, text='', fg='cyan2')
ManufacturerOffset = Label(InfoFrame, text='', fg='cyan2')
VersionOffset = Label(InfoFrame, text='', fg='cyan2')
HeaderCRCOffset = Label(InfoFrame, text='', fg='cyan2')
TitleOffset.grid(row=0, column=1, sticky='nw')
FilenameOffset.grid(row=0, column=1, sticky='nw')
FiletypeOffset.grid(row=1, column=1, sticky='nw')
SizeOffset.grid(row=2, column=1, sticky='nw')
NameOffset.grid(row=3, column=1, sticky='nw')
CartIDOffset.grid(row=4, column=1, sticky='nw')
RegionOffset.grid(row=5, column=1, sticky='nw')
ManufacturerOffset.grid(row=6, column=1, sticky='nw')
VersionOffset.grid(row=7, column=1, sticky='nw')
HeaderCRCOffset.grid(row=8, column=1, sticky='nw')

TitleLength = Label(InfoFrame, text='')
FilenameLength = Label(InfoFrame, text='', fg='magenta2')
FiletypeLength = Label(InfoFrame, text='', fg='magenta2')
SizeLength = Label(InfoFrame, text='', fg='magenta2')
NameLength = Label(InfoFrame, text='', fg='magenta2')
CartIDLength = Label(InfoFrame, text='', fg='magenta2')
RegionLength = Label(InfoFrame, text='', fg='magenta2')
ManufacturerLength = Label(InfoFrame, text='', fg='magenta2')
VersionLength = Label(InfoFrame, text='', fg='magenta2')
HeaderCRCLength = Label(InfoFrame, text='', fg='magenta2')
TitleLength.grid(row=0, column=2, sticky='nw')
FilenameLength.grid(row=0, column=2, sticky='nw')
FiletypeLength.grid(row=1, column=2, sticky='nw')
SizeLength.grid(row=2, column=2, sticky='nw')
NameLength.grid(row=3, column=2, sticky='nw')
CartIDLength.grid(row=4, column=2, sticky='nw')
RegionLength.grid(row=5, column=2, sticky='nw')
ManufacturerLength.grid(row=6, column=2, sticky='nw')
VersionLength.grid(row=7, column=2, sticky='nw')
HeaderCRCLength.grid(row=8, column=2, sticky='nw')

Filename = Label(InfoFrame, text='', fg='gray15')
Filetype = Label(InfoFrame, text='', fg='gray15')
Size = Label(InfoFrame, text='', fg='gray15')
Name = Label(InfoFrame, text='', fg='gray15')
CartID = Label(InfoFrame, text='', fg='gray15')
Region = Label(InfoFrame, text='', fg='gray15')
Manufacturer = Label(InfoFrame, text='', fg='gray15')
Version = Label(InfoFrame, text='', fg='gray15')
HeaderCRC = Label(InfoFrame, text='', fg='gray15')
Filename.grid(row=1, column=3, sticky='nw')
Filetype.grid(row=2, column=3, sticky='nw')
Size.grid(row=3, column=3, sticky='nw')
Name.grid(row=4, column=3, sticky='nw')
CartID.grid(row=5, column=3, sticky='nw')
Region.grid(row=6, column=3, sticky='nw')
Manufacturer.grid(row=7, column=3, sticky='nw')
Version.grid(row=8, column=3, sticky='nw')
HeaderCRC.grid(row=9, column=3, sticky='nw')

TweakFrame = LabelFrame()
TweakFrame.pack(fill='x', expand='no')


# Main Window Navbar #
Navbar = Menu(MainWindow)

# Navbar "File" Tab #
FileMenu = Menu(Navbar, tearoff=0)
FileMenu.add_command(label='Open ROM', accelerator='Ctrl+O', command=lambda: openFile('new'))
FileMenu.add_separator()
FileMenu.add_command(label='N64 Rom Checker', command=lambda: openTools('N64RomChecker'))
FileMenu.add_command(label='GBA Rom Checker', command=lambda: openTools('GBARomChecker'))
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
