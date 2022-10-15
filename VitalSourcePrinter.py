import PyPDF4
import pyautogui
import os
import sys
from time import sleep, time
import tkinter.filedialog as filedialog


def make_vitalsource_active():
    """
    check if the vital window is open, if open it's activated
    :return: if not open, the program exit
    """
    if "VitalSource Bookshelf" in pyautogui.getAllTitles():
        print(pyautogui.getAllTitles())
        if not pyautogui.getWindowsWithTitle("VitalSource Bookshelf")[0].isActive:
            print("window must be activated")
            pyautogui.getWindowsWithTitle("VitalSource Bookshelf")[0].activate()
        pyautogui.getWindowsWithTitle("VitalSource Bookshelf")[0].maximize()
    else:
        sys.exit()


def print_and_save(start, end):
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
    sleep(20)
    pyautogui.press('tab', 4, interval=0.1)
    pyautogui.press('enter', interval=0.1)
    pyautogui.write("C:\\Users\\ARNJ\\Documents\\vitalSource\\test_" + str(start) + '_' + str(end), interval=0.15)
    sleep(0.5)
    pyautogui.press('enter', interval=0.1)
    sleep(0.5)
    pyautogui.press('escape', interval=0.1)


def pdf_processor():
    pass


if __name__ == "__main__":
    start_time = time()  # used to pace the program
    NumberStart = 15
    NumberEnd = 2670

    for page in range(NumberStart, NumberEnd, 2):
        print_and_save(page, page + 1)
        sleep(7)

    filedir = filedialog.askdirectory() + '//'

    # number_process()

    elapsed_time = time() - start_time
    print("\nDone!")
    print("This took " + "%.2f" % (elapsed_time / 3600) + " hours.")
