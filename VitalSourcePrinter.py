try:
    import PyPDF2
    import pyautogui
    import os
    import sys
    import time
    import warnings
    from tkinter import *
    import tkinter.filedialog as filedialog
except ImportError:
    print("Please install PyPDF2 and pyautogui. Refer to video or documentation for help")
    sys.exit()
"""
ctrl+p
write page 
tab
write page 
enter 
wait environ 60 sec
3 flêche down # choix imprimante
4 tab 
enter
"""


def check_vital_open():
    """
    check if the vital window is open, if open it's activated
    :return: if not open, the program exit
    """
    if "VitalSource Bookshelf" in pyautogui.getAllTitles():
        pyautogui.getWindowsWithTitle("VitalSource Bookshelf")[0].activate()
    else:
        sys.exit()

def initiate_print():
    pyautogui.hotkey('ctrl', 'p', interval=0.25)
    pyautogui.press('tab', 2, interval=0.25)
    pyautogui.press('delete', 5, interval=0.25)

def main():
    start_time = time.time() # used to pace the program
    check_vital_open()
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write("1")
    pyautogui.hotkey("tab")
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write("2")
    pyautogui.hotkey("tab")
    pyautogui.hotkey("enter")
    # warnings.filterwarnings("ignore")  # Gets rid of harmless warnings on the console for excess whitespace

    print("Welcome to the VitalSource Ebook Printer. \n")

    while (True):
        try:
            NumberStart = int(input("First page: "))
            NumberEnd = int(input("Last page: "))
            if (type(NumberStart) != int) or (type(NumberStart) != int):
                print("Please enter valid numbers.\n")
                continue
            elif (NumberStart > NumberEnd):
                print("First page must be less than last page.\n")
                continue
            else:
                break
        except:
            print("Please enter valid page numbers.\n")

    NumberList = []
    for i in range(int(NumberStart), int(NumberEnd) + 1):
        NumberList += [str(i)]

    root = Tk()
    root.withdraw()
    root.overrideredirect(True)
    root.geometry('0x0+0+0')
    # root.deiconify()
    root.lift()
    root.focus_force()
    # credits to http://stackoverflow.com/questions/3375227/how-to-give-tkinter-file-dialog-focus

    filedir = filedialog.askdirectory() + '//'

    if len(NumberList) % 2 != 0:
        NumberList += [NumberList[-1]]

        PageEntry1 = NumberList[0]
        PageEntry2 = NumberList[1]

        initiate_print()
        pyautogui.typewrite(PageEntry1)
        pyautogui.press('tab')
        pyautogui.press('delete', 5)
        pyautogui.typewrite(PageEntry2)
        pyautogui.typewrite(['tab', 'tab', 'enter', 'enter'], interval=0.25)
        pyautogui.typewrite("Ebook", interval=0.50)
        pyautogui.press('enter', interval=0.5)
        time.sleep(0.25)

    def NumberProcess(start):
        for page in range(start, len(NumberList), 2):
            initiate_print()
            pyautogui.typewrite(NumberList[page], interval=0.25)
            pyautogui.press('tab', interval=0.25)
            pyautogui.press('delete', 5, interval=0.25)
            pyautogui.typewrite(NumberList[page + 1])
            pyautogui.typewrite(['tab', 'tab', 'enter', 'enter'], interval=0.75)
            pyautogui.typewrite("File2", interval=0.5)
            pyautogui.press('enter', interval=0.5)
            time.sleep(5)
            while not os.path.isfile(filedir + "Ebook.pdf"):
                time.sleep(2)
            while not os.path.isfile(filedir + "File2.pdf"):
                time.sleep(2)
            try:
                pdf1File = open(filedir + 'Ebook.pdf', 'rb')
                pdf2File = open(filedir + 'File2.pdf', 'rb')
            except:
                while not os.path.isfile(filedir + Ebook.pdf):
                    time.sleep(10)
                while not os.path.isfile(filedir + File2.pdf):
                    time.sleep(10)
            try:
                pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
            except:
                time.sleep(5)
                pdf1Reader = PyPDF2.PdfFileReader(pdf1File)

            try:
                pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
            except:
                time.sleep(5)
                pdf2Reader = PyPDF2.PdfFileReader(pdf2File)

            pdfWriter = PyPDF2.PdfFileWriter()
            for pageNum in range(pdf1Reader.numPages):
                pageObj = pdf1Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            for pageNum in range(pdf2Reader.numPages):
                pageObj = pdf2Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            pdfOutputFile = open(filedir + 'Ebook1.pdf', 'wb')
            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()
            pdf1File.close()
            pdf2File.close()
            try:
                os.remove(filedir + 'Ebook.pdf')
            except:
                time.sleep(10)
                os.remove(filedir + 'Ebook.pdf')

            try:
                os.remove(filedir + 'File2.pdf')
            except:
                time.sleep(10)
                os.remove(filedir + 'File2.pdf')

            try:
                os.rename(filedir + 'Ebook1.pdf', filedir + 'Ebook.pdf')
            except:
                time.sleep(10)
                os.rename(filedir + 'Ebook1.pdf', filedir + 'Ebook.pdf')

            print("Page: " + str(page + 2) + ' of ' + str(len(NumberList)))

    elapsed_time = time.time() - start_time
    print("\nDone!")
    print("This took " + "%.2f" % (elapsed_time / 3600) + " hours.")


if __name__ == "__main__": main()
