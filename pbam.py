import pyautogui
import webbrowser
import time
import random
import json
import subprocess
import keyboard
import threading


with open('config.json', 'r') as config_file:
    config = json.load(config_file)

browser_addresses = config['browser_addresses']
prewritten_script = config['script']
write_interval = config['write_interval']
delete_interval = config['delete_interval']

def open_browser_and_search(addresses):
    global running
    for address in addresses:
        if not running:
            return
        webbrowser.open(address)
        time.sleep(random.uniform(3, 5)) 
        scroll_randomly()
        move_mouse_randomly()

def scroll_randomly():
    global running
    for _ in range(random.randint(5, 10)):
        if not running:
            return
        pyautogui.scroll(random.randint(-100, 100))

def move_mouse_randomly():
    global running
    screen_width, screen_height = pyautogui.size()
    for _ in range(random.randint(10, 20)):
        if not running:
            return
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5))

def write_and_delete_script(script, write_interval, delete_interval):
    global running
    if not running:
            return

    subprocess.Popen(['notepad.exe'])
    time.sleep(5)

    pyautogui.typewrite(script, interval=0.1)
    time.sleep(write_interval)

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    time.sleep(delete_interval)

def stop_bot():
    global running
    print("Stopping the bot.")
    running = False

def key_listener():
    global running
    while running:
        if keyboard.is_pressed('right arrow'):
            stop_bot()
            break
        time.sleep(0.1)

def main():
    hide_console_window()
    global running
    running = True

    key_thread = threading.Thread(target=key_listener)
    key_thread.start()

    while running:
        open_browser_and_search(browser_addresses)
        write_and_delete_script(prewritten_script, write_interval, delete_interval)
        time.sleep(1)
    key_thread.join()
def hide_console_window():
    import ctypes
    import platform
    
    if platform.system() == "Windows":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

if __name__ == "__main__":
    main()
