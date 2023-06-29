import pyautogui
import keyboard

def print_coordinates():
    print(pyautogui.position())

keyboard.add_hotkey('g', print_coordinates)

keyboard.wait()
