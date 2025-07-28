# Advance-Key-Logger
# Advance Key Logger With C2 server 

**Project Title:** Advanced Python-Based (Educational) Keylogger

**Developer:** Vaibhav (For Educational Purposes Only)

---

## 📄 Project Overview

This project demonstrates how a Python-based keylogger can:

1. Stealthily capture keystrokes from a target machine.
2. Transmit them to a remote server if available.
3. Store them locally and send via email when offline.
4. Run stealthily on startup through Windows Registry persistence.

> ⚠️ **DISCLAIMER:** This project is strictly for **educational and ethical testing** purposes. Unauthorized use of keyloggers is illegal and unethical.

---

## 💻 Components

- **Keylogger Client (winupdater.exe):** Stealthy executable compiled from Python
- **Server:** Python socket-based receiver to log keystrokes

---

## 📁 Folder Structure

```
advanced-keylogger/
├── keylogger.py
├── server.py

```

---

## 🔧 Setup Instructions

### ✅ 1. Keylogger (Client)

- Location: `keylogger.py`
- Convert to EXE:

```bash
pyinstaller --onefile --noconsole --name winupdater keylogger.py
```

- Output: `dist/winupdater.exe`

### 🔌 2. Server (Receiver)

- Location: `server.py`
- Run on attacker machine:

```bash
python server.py
```

- Listens for keystroke data on port `12345`

---

## 🚪 Persistence

The keylogger adds itself to startup via the Windows Registry:

```reg
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

Key: `WindowsUpdater` Value: Path to copied executable inside `AppData\Roaming\WindowsApp\`

---

## 🚫 Cleanup

1. Open `regedit` → Delete the key:

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\WindowsUpdater
```

2. Delete the copied file from:

```
C:\Users\<User>\AppData\Roaming\WindowsApp\
```

---

## ✉️ Offline Logs via Email (Optional Extension)

- When server connection fails, logs are stored locally in `log.txt`
- Periodically sent to your email using SMTP

---

## 📅 Use Cases (Educational)

- Ethical hacking demo
- Malware analysis & defense labs
- Penetration testing toolkit (with consent)
- Building awareness about cyber threats

---

## 🚀 Future Enhancements

- Add GUI log viewer (Python + Tkinter)
- Encrypted keystroke transmission
- Include screenshot capture
- Anti-detection techniques simulation

---

## 🙏 Credits & Thanks

 Vaibhav Dhonde 

> For queries or demos, contact: [vaibhavdhonde78@gmail.com]

