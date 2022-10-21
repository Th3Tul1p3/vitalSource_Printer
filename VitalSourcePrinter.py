from tkinter import filedialog, simpledialog
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
        print("VitalSource is not open...")
        sys.exit()


def print_and_save(start: str, end: str, tmp_file: str):
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
    pyautogui.write(start)
    sleep(1.5)
    pyautogui.press('tab', interval=0.1)
    pyautogui.hotkey('ctrl', 'a', interval=0.1)
    pyautogui.write(end)
    sleep(1.5)
    pyautogui.press('tab', interval=0.1)
    pyautogui.press('enter', interval=0.1)
    # wait until the printer window appear
    while 'Printing - Print' not in pyautogui.getAllTitles():
        sleep(3)
    sleep(1)
    pyautogui.press('tab', 4, interval=0.1)
    pyautogui.press('enter', interval=0.1)
    sleep(1)
    pyautogui.write(tmp_file, interval=0.05)
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


def str_input(title, prompt, default='_cfi.pdf'):
    """
    Ask the name of printed files
    :param title: Name of window
    :param prompt: The question
    :param default: default filename
    :return: the filename
    """
    return simpledialog.askstring(title, prompt, initialvalue=default)


if __name__ == "__main__":
    start_time = time()  # used to pace the program
    test = str_input("Target file", "Enter a target file for pdf: ")
    # directory where we are doing all operations
    base_directory = (filedialog.askdirectory() + '/').replace('/', '\\')
    tmp_pdf_file = base_directory + "tmp.pdf"
    final_pdf_file = base_directory + "_cfi.pdf"

    if not os.path.isdir(base_directory):
        os.mkdir(base_directory)

    NumberStart = 1455
    NumberEnd = 2670
    counter = 0

    for page in range(NumberStart, NumberEnd, 2):
        # print to pages, except for the last one if odd
        if page + 1 > NumberEnd:
            print_and_save(str(page), str(page), tmp_pdf_file)
        else:
            print_and_save(str(page), str(page + 1), tmp_pdf_file)

        sleep(4)  # let vitalSource breath a bit between 2 print
        pdf_processor(tmp_pdf_file, final_pdf_file)
        # remove the tmp file
        os.remove(tmp_pdf_file)
        counter += 1
        print("Average by print: " + "%.2f" % ((time() - start_time) / counter) + " sec")
        print("Pages: ", str(page), str(page + 1), "Successfully printed.")

    print("\nDone!")
    print("This took " + "%.2f" % (time() - start_time / 3600) + " hours.")
