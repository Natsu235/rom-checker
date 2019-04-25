#-----------------------------------------------------------#
# Project Name: N64 Rom Checker                             #
# Filename:     N64RomChecker.py                                     #
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
        LoadedROM = filedialog.askopenfilename(initialdir='/', title='Select a ROM', filetypes=(('N64 Roms', '*.n64;*.v64;*.z64'), ('All', '*')))

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
            ROMCRC = checkROMCRC(LoadedROM, ROMExtension)
            ROMCICVersion = checkROMCICVersion(LoadedROM, ROMExtension)
            ROMCRCStatus = checkROMCRCStatus(LoadedROM)
        except:
            ROMFiletype = 'Unsupported (not a N64 ROM!)'
            ROMSize = ''
            ROMName = ''
            ROMCartID = ''
            ROMRegion = ''
            ROMVersion = ''
            ROMManufacturer = ''
            ROMCRC = ''
            ROMCICVersion = ''
            ROMCRCStatus = ''

        # Display available "ROM Tweaks" for loaded ROM #
        global TweakFrame

        if TweakFrame.winfo_exists():
            TweakFrame.destroy()

        TweakFrame = LabelFrame(MainWindow, text='ROM Tweaks', padx=5, pady=5)
        TweakFrame.pack(fill='x', expand='no')

        if ROMCartID[:1] == 'C' and ROMName == 'THE LEGEND OF ZELDA':
            ManufacturerFix = Button(TweakFrame, text='Fix Manufacturer', command=lambda: fixManufacturer(LoadedROM, ROMExtension, ROMName))
            ManufacturerFix.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        if ROMCRC == '9F C3 85 E5 3E CC 05 C7' and ROMExtension == '.z64' and hex(ROM[33923632]) != '0xff':
            RemoveCredits = Button(TweakFrame, text='Remove Cen Credits', command=lambda: removeCredits(LoadedROM, ROMName))
            RemoveCredits.grid(row=0, column=1, padx=5, pady=5, sticky='nw')

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
    CICVersion['text'] = ROMCICVersion
    CRCStatus['text'] = ROMCRCStatus

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
    print('ROM CIC Version: ', ROMCICVersion)
    print('ROM CRC Status: ', ROMCRCStatus)


def checkROMType(ROMExtension):
    if ROMExtension == '.n64':
        ROMFiletype = 'Little Endian (N64 Format)'
    elif ROMExtension == '.v64':
        ROMFiletype = 'Byteswapped (Doctor V64 Format)'
    elif ROMExtension == '.z64':
        ROMFiletype = 'Big Endian (Mr. Backup Z64 Format)'
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
    elif ROMSize <= 41943040:
        ROMSize = '40 MB'
    elif ROMSize <= 67108864:
        ROMSize = '64 MB'
    else:
        ROMSize = '> 64 MB (ROM size is too big!)'

    return ROMSize


def checkROMName(LoadedROM, ROMExtension):
    with open(LoadedROM, 'rb') as f:
        f.seek(32)
        ROMName = f.read(20)

    if ROMExtension == '.n64':
        ROMName = ROMName[::-1]
        ROMName = ROMName[16:20]+ROMName[12:16]+ROMName[8:12]+ROMName[4:8]+ROMName[0:4]
    elif ROMExtension == '.v64':
        ROMName = ROMName[::-1]
        ROMName = ROMName[18:20]+ROMName[16:18]+ROMName[14:16]+ROMName[12:14]+ROMName[10:12]+ROMName[8:10]+ROMName[6:8]+ROMName[4:6]+ROMName[2:4]+ROMName[0:2]
    elif ROMExtension == '.z64':
        pass
    else:
        ROMName = 'Unknown'

    ROMName = ROMName.decode()

    return ROMName.rstrip()


def checkROMCartID(ROM, ROMExtension):
    if ROMExtension == '.n64':
        ROMCartID = chr(ROM[56]), chr(ROM[63]), chr(ROM[62]), chr(ROM[61])
    elif ROMExtension == '.v64':
        ROMCartID = chr(ROM[58]), chr(ROM[61]), chr(ROM[60]), chr(ROM[63])
    elif ROMExtension == '.z64':
        ROMCartID = chr(ROM[59]), chr(ROM[60]), chr(ROM[61]), chr(ROM[62])
    else:
        ROMCartID = 'Unknown'

    ROMCartID = re.sub('[^A-Za-z0-9]+', '', str(ROMCartID))

    return ROMCartID


def checkROMRegion(ROM, ROMExtension):
    if ROMExtension == '.n64':
        x = 61
    elif ROMExtension == '.v64':
        x = 63
    elif ROMExtension == '.z64':
        x = 62

    if chr(ROM[x]) == 'E':
        ROMRegion = 'American (NTSC-U)'
    elif chr(ROM[x]) == 'J':
        ROMRegion = 'Japanese (NTSC-J)'
    elif chr(ROM[x]) == 'P':
        ROMRegion = 'European (PAL)'
    else:
        ROMRegion = 'Unknown'

    return ROMRegion


def checkROMManufacturer(ROM, ROMExtension):
    if ROMExtension == '.n64':
        x = 56
    elif ROMExtension == '.v64':
        x = 58
    elif ROMExtension == '.z64':
        x = 59

    if chr(ROM[x]) == 'C':
        ROMManufacturer = 'Nintendo (Ocarina of Time)'
    elif chr(ROM[x]) == 'N':
        ROMManufacturer = 'Nintendo'
    else:
        ROMManufacturer = 'Unknown'

    return ROMManufacturer


def checkROMVersion(ROM, ROMExtension):
    if ROMExtension == '.n64':
        x = 60
    elif ROMExtension == '.v64':
        x = 62
    elif ROMExtension == '.z64':
        x = 63

    ROMVersion = ROM[x]
    ROMVersion = 'v1.', ROMVersion
    ROMVersion = re.sub('[^A-Za-z0-9.]+', '', str(ROMVersion))

    return ROMVersion


def checkROMCRC(LoadedROM, ROMExtension):
    with open(LoadedROM, 'rb') as f:
        f.seek(16)
        ROMCRC = f.read(8)

    if ROMExtension == '.n64':
        ROMCRC = ROMCRC[::-1]
        ROMCRC = ROMCRC[4:8]+ROMCRC[0:4]
    elif ROMExtension == '.v64':
        ROMCRC = ROMCRC[::-1]
        ROMCRC = ROMCRC[6:8]+ROMCRC[4:6]+ROMCRC[2:4]+ROMCRC[0:2]
    elif ROMExtension == '.z64':
        pass

    ROMCRC = binascii.hexlify(ROMCRC).upper()
    ROMCRC = ' '.join(re.findall('([0-9A-F]{2}|[0-9A-F])', str(ROMCRC)[1:]))

    return ROMCRC


def checkROMCICVersion(LoadedROM, ROMExtension):
    if ROMExtension == '.n64':
        ROMCICVersion = 'Only for ".z64" format!'
    elif ROMExtension == '.v64':
        ROMCICVersion = 'Only for ".z64" format!'
    elif ROMExtension == '.z64':
        with open(LoadedROM, 'rb') as f1:
            f1.seek(64)
            ROMCIC = f1.read(4032)
            f2 = open('files/6101CIC.bin', 'rb').read()
            f3 = open('files/6102CIC.bin', 'rb').read()
            f4 = open('files/6103CIC.bin', 'rb').read()
            f5 = open('files/6105CIC.bin', 'rb').read()
            f6 = open('files/6106CIC.bin', 'rb').read()

            if ROMCIC == f2:
                ROMCICVersion = 'CIC-NUS-6101'
            elif ROMCIC == f3:
                ROMCICVersion = 'CIC-NUS-6102'
            elif ROMCIC == f4:
                ROMCICVersion = 'CIC-NUS-6103'
            elif ROMCIC == f5:
                ROMCICVersion = 'CIC-NUS-6105'
            elif ROMCIC == f6:
                ROMCICVersion = 'CIC-NUS-6106'
            else:
                ROMCICVersion = 'Unknown'

    return ROMCICVersion


def checkROMCICVersion2(ROM, ROMExtension):
    if ROMExtension == '.n64':
        x = 368
    elif ROMExtension == '.v64':
        x = 370
    elif ROMExtension == '.z64':
        x = 371

    if hex(ROM[x]) == '0x0':
        ROMCICVersion = 'CIC-NUS-6101'
    elif hex(ROM[x]) == '0xde':
        ROMCICVersion = 'CIC-NUS-6102'
    elif hex(ROM[x]) == '0xdb':
        ROMCICVersion = 'CIC-NUS-6103'
    elif hex(ROM[x]) == '0x14':
        ROMCICVersion = 'CIC-NUS-6105'
    elif hex(ROM[x]) == '0xec':
        ROMCICVersion = 'CIC-NUS-6106'
    else:
        ROMCICVersion = 'Unknown'

    return ROMCICVersion


def checkROMCRCStatus(LoadedROM):
    with open(LoadedROM, 'rb') as f1:
        f1.seek(16)
        ROMCRC = f1.read(8)

    ROMCRC = binascii.hexlify(ROMCRC).upper()
    ROMCRC = ' '.join(re.findall('([0-9A-F]{2}|[0-9A-F])', str(ROMCRC)[1:]))

    try:
        f2 = open('files/N64-CRC-Database.txt', 'r').read()

        if ROMCRC in f2:
            ROMCRCStatus = 'Verified'
            CRCStatus['fg'] = 'green'
        else:
            ROMCRCStatus = 'Modified'
            CRCStatus['fg'] = 'red'
    except:
        ROMCRCStatus = 'File "files/N64-CRC-Database.txt" is missing!'
        CRCStatus['fg'] = 'orange'

    return ROMCRCStatus


def openTools(tool):
    try:
        os.startfile('..\\' + tool + '\\' + tool + '.exe')
        MainWindow.destroy()
    except:
        messagebox.showerror('Error', '\nCan\'t find "' + tool + '" folder!')
        print('\n[MessageBox]Can\'t find "' + tool + '" folder!')


def showOffsets(flag):
    if flag:
        TitleOffset['text'] = 'Start'
        NameOffset['text'] = ' 0x20 '
        CartIDOffset['text'] = ' 0x3B '
        RegionOffset['text'] = ' 0x3E '
        ManufacturerOffset['text'] = ' 0x3B '
        VersionOffset['text'] = ' 0x3F '
        CRCOffset['text'] = ' 0x10 '
        CICVersionOffset['text'] = ' 0x40 '

        TitleLength['text'] = 'Length'
        NameLength['text'] = ' 0x14 '
        CartIDLength['text'] = ' 0x04 '
        RegionLength['text'] = ' 0x01 '
        ManufacturerLength['text'] = ' 0x01 '
        VersionLength['text'] = ' 0x01 '
        CRCLength['text'] = ' 0x08 '
        CICVersionLength['text'] = ' 0xFC0 '
    else:
        TitleOffset['text'] = ''
        NameOffset['text'] = ''
        CartIDOffset['text'] = ''
        RegionOffset['text'] = ''
        ManufacturerOffset['text'] = ''
        VersionOffset['text'] = ''
        CRCOffset['text'] = ''
        CICVersionOffset['text'] = ''

        TitleLength['text'] = ''
        NameLength['text'] = ''
        CartIDLength['text'] = ''
        RegionLength['text'] = ''
        ManufacturerLength['text'] = ''
        VersionLength['text'] = ''
        CRCLength['text'] = ''
        CICVersionLength['text'] = ''


def fixManufacturer(LoadedROM, ROMExtension, ROMName):
    try:
        with open(LoadedROM, 'r+b') as f:
            if ROMExtension == '.n64':
                x = 56
            elif ROMExtension == '.v64':
                x = 58
            elif ROMExtension == '.z64':
                x = 59

            f.seek(x)
            f.write('N'.encode())
            f.seek(0)
            openFile(LoadedROM)
            messagebox.showinfo('Success', 'ROM Tweak Manufacturer Fix successfully applied to ' + ROMName + '!')
            print('\n[MessageBox]ROM Tweak Manufacturer Fix successfully applied to ' + ROMName + '!')
    except:
        messagebox.showerror('Error', 'An error occurred while applying ROM Tweak Manufacturer Fix to ' + ROMName + '!')
        print('\n[MessageBox]An error occurred while applying ROM Tweak Manufacturer Fix to ' + ROMName + '!')


def removeCredits(LoadedROM, ROMName):
    try:
        with open(LoadedROM, 'r+b') as f:
            x = 33923632
            f.seek(x)
            for i in range(1, 2311):
                f.write(b'\xFF')
                x = x + 1
                f.seek(x)
            openFile(LoadedROM)
            messagebox.showinfo('Success', 'ROM Tweak Remove Cen Credits successfully applied to ' + ROMName + '!')
            print('\n[MessageBox]ROM Tweak Remove Cen Credits successfully applied to ' + ROMName + '!')
    except:
        messagebox.showerror('Error', 'An error occurred while applying ROM Tweak Remove Cen Credits to ' + ROMName + '!')
        print('\n[MessageBox]An error occurred while applying ROM Tweak Remove Cen Credits to ' + ROMName + '!')


def about():
    AboutWindow = Toplevel(MainWindow)
    AboutWindow.title('About')
    AboutWindow.geometry('240x200')
    AboutWindow.iconbitmap('./icons/n64.ico')
    AboutWindow.resizable(width=False, height=False)

    Image = PhotoImage(file='./images/about.ppm')
    Image = Image.subsample(4)
    AboutImage = Label(AboutWindow, anchor='n', image=Image)
    AboutImage.pack(padx=5, pady=5)
    AboutImage.image = Image

    AboutText = Label(AboutWindow, text='N64 Rom Checker\nVanilla Edition (v1.0)\nMade by Natsu235')
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

        LoadingText = Label(LoadingWindow, text='Loading N64 ROM... Please wait.')
        LoadingText.pack(padx=10, pady=10)

        ProgressBar = ttk.Progressbar(LoadingWindow, mode='indeterminate', length='200')
        ProgressBar.pack(padx=10, pady=10)
        ProgressBar.start()
    else:
        MainWindow.attributes("-disabled", False)
        LoadingWindow.destroy()


# Main Window #
MainWindow = Tk()
MainWindow.title('N64 Rom Checker (Vanilla Edition 1.0)')
MainWindow.geometry('700x640')
MainWindow.iconbitmap('./icons/n64.ico')
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
ROMCICVersionLabel = Label(InfoFrame, text='Rom CIC Version: ')
ROMCRCStatusLabel = Label(InfoFrame, text='Rom CRC Status: ')
ROMFilenameLabel.grid(row=1, column=0, sticky='nw')
ROMFiletypeLabel.grid(row=2, column=0, sticky='nw')
ROMSizeLabel.grid(row=3, column=0, sticky='nw')
ROMNameLabel.grid(row=4, column=0, sticky='nw')
ROMCartIDLabel.grid(row=5, column=0, sticky='nw')
ROMRegionLabel.grid(row=6, column=0, sticky='nw')
ROMManufacturerLabel.grid(row=7, column=0, sticky='nw')
ROMVersionLabel.grid(row=8, column=0, sticky='nw')
ROMCRCLabel.grid(row=9, column=0, sticky='nw')
ROMCICVersionLabel.grid(row=10, column=0, sticky='nw')
ROMCRCStatusLabel.grid(row=11, column=0, sticky='nw')

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
CICVersionOffset = Label(InfoFrame, text='', fg='cyan2')
CRCStatusOffset = Label(InfoFrame, text='', fg='cyan2')
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
CICVersionOffset.grid(row=10, column=1, sticky='nw')
CRCStatusOffset.grid(row=11, column=1, sticky='nw')

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
CICVersionLength = Label(InfoFrame, text='', fg='magenta2')
CRCStatusLength = Label(InfoFrame, text='', fg='magenta2')
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
CICVersionLength.grid(row=10, column=2, sticky='nw')
CRCStatusLength.grid(row=11, column=2, sticky='nw')

Filename = Label(InfoFrame, text='', fg='gray15')
Filetype = Label(InfoFrame, text='', fg='gray15')
Size = Label(InfoFrame, text='', fg='gray15')
Name = Label(InfoFrame, text='', fg='gray15')
CartID = Label(InfoFrame, text='', fg='gray15')
Region = Label(InfoFrame, text='', fg='gray15')
Manufacturer = Label(InfoFrame, text='', fg='gray15')
Version = Label(InfoFrame, text='', fg='gray15')
CRC = Label(InfoFrame, text='', fg='gray15')
CICVersion = Label(InfoFrame, text='', fg='gray15')
CRCStatus = Label(InfoFrame, text='', fg='gray15')
Filename.grid(row=1, column=3, sticky='nw')
Filetype.grid(row=2, column=3, sticky='nw')
Size.grid(row=3, column=3, sticky='nw')
Name.grid(row=4, column=3, sticky='nw')
CartID.grid(row=5, column=3, sticky='nw')
Region.grid(row=6, column=3, sticky='nw')
Manufacturer.grid(row=7, column=3, sticky='nw')
Version.grid(row=8, column=3, sticky='nw')
CRC.grid(row=9, column=3, sticky='nw')
CICVersion.grid(row=10, column=3, sticky='nw')
CRCStatus.grid(row=11, column=3, sticky='nw')

TweakFrame = LabelFrame()
TweakFrame.pack(fill='x', expand='no')


# Main Window Navbar #
Navbar = Menu(MainWindow)

# Navbar "File" Tab #
FileMenu = Menu(Navbar, tearoff=0)
FileMenu.add_command(label='Open ROM', accelerator='Ctrl+O', command=lambda: openFile('new'))
FileMenu.add_separator()
FileMenu.add_command(label='GBA Rom Checker', command=lambda: openTools('GBARomChecker'))
FileMenu.add_command(label='NDS Rom Checker', command=lambda: openTools('NDSRomChecker'))
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
