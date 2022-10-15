from PyPDF4 import PdfFileMerger
import pyautogui
import os
import sys
from time import sleep, time


def make_vitalsource_active():
    """
    check if the vital window is open, if open it's activated
    :return: if not open, the program exit
    """
    if "VitalSource Bookshelf" in pyautogui.getAllTitles():
        if not pyautogui.getWindowsWithTitle("VitalSource Bookshelf")[0].isActive:
            pyautogui.getWindowsWithTitle("VitalSource Bookshelf")[0].activate()
        pyautogui.getWindowsWithTitle("VitalSource Bookshelf")[0].maximize()
    else:
        sys.exit()


def print_and_save(start: int, end: int, tmp_file: str):
    """
    make the keystrockes to print one or two pages with the given absolute path
    :param start: number of first page
    :param end: number of second page
    :param tmp_file: absolute file path of destination
    """
    make_vitalsource_active()
    pyautogui.hotkey('ctrl', 'p', interval=0.1)
    sleep(0.5)
    pyautogui.hotkey('ctrl', 'a', interval=0.1)
    pyautogui.write(str(start))
    sleep(0.5)
    pyautogui.press('tab', interval=0.1)
    pyautogui.hotkey('ctrl', 'a', interval=0.1)
    pyautogui.write(str(end))
    pyautogui.press('tab', interval=0.1)
    pyautogui.press('enter', interval=0.1)
    # wait until the printer window appear
    while 'Printing - Print' not in pyautogui.getAllTitles():
        sleep(3)
    pyautogui.press('tab', 4, interval=0.1)
    pyautogui.press('enter', interval=0.1)
    sleep(0.5)
    pyautogui.write(tmp_file)
    sleep(0.5)
    pyautogui.press('enter', interval=0.1)
    sleep(0.5)
    pyautogui.press('escape', interval=0.1)


def pdf_processor(input_file: str, output_file: str):
    """
    merge the final pdf file and the new printed file together
    :param input_file: the file to append
    :param output_file: final pdf file
    """
    # strict = False -> To ignore PdfReadError - Illegal Character error
    merger = PdfFileMerger(strict=False)
    # for the first run, the final pdf might not be created
    if os.path.isfile(output_file):
        merger.append(fileobj=open(output_file, 'rb'))
    merger.append(fileobj=open(input_file, 'rb'))
    merger.write(fileobj=open(output_file, 'wb'))
    merger.close()


if __name__ == "__main__":
    start_time = time()  # used to pace the program

    # directory where we are doing all operations
    # filedir = filedialog.askdirectory() + '//'
    base_directory = "C:\\Users\\ARNJ\\Documents\\vitalSource"
    tmp_pdf_file = base_directory + "\\tmp.pdf"
    final_pdf_file = base_directory + "\\_cfi.pdf"

    if not os.path.isdir(base_directory):
        os.mkdir(base_directory)

    NumberStart = 79
    NumberEnd = 2670
    old_time = time() - start_time

    for page in range(NumberStart, NumberEnd, 2):
        # print to pages, except for the last one if odd
        if page + 1 > NumberEnd:
            print_and_save(page, page, tmp_pdf_file)
        else:
            print_and_save(page, page + 1, tmp_pdf_file)

        sleep(4)  # let vitalSource breath a bit between 2 print
        pdf_processor(tmp_pdf_file, final_pdf_file)
        # remove the tmp file
        os.remove(tmp_pdf_file)
        print("for two pages: " + "%.2f" % (time() - start_time - old_time) + " sec")
        old_time = time() - start_time

    print("\nDone!")
    print("This took " + "%.2f" % (time() - start_time / 3600) + " hours.")
