# 🎭 PHANTOM RAT v6.6 : The Invisible Observer
> **Advanced Discord-Based Command & Control (C2) Framework for Red Teaming Operations & Security Research.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![Build](https://img.shields.io/badge/Build-6.6--Stable-green?style=for-the-badge)
![Researcher](https://img.shields.io/badge/Researcher-R.Code-red?style=for-the-badge)

---

---

## 📸 Preview / Screenshots

<details>
<summary><b>🇺🇸 Click to expand Screenshots</b></summary>

### 🖥️ Phantom Builder Interface
<img width="1186" height="905" alt="Screenshot 2026-05-01 221918" src="https://github.com/user-attachments/assets/d004e62f-7152-4fa0-9cd9-a793dfb0ed29" />
*Interface for configuring Bot Token, Channel ID, and building the executable.*

### 🔒 Phantom Locker GUI (Default)
<img width="1920" height="1080" alt="background" src="https://github.com/user-attachments/assets/c0f84254-78c3-4c93-adc7-3dd10fad4979" />
<img width="1920" height="1080" alt="2" src="https://github.com/user-attachments/assets/2532ed8a-f429-46db-aa4d-82e5e483f1e9" />
<img width="1920" height="1080" alt="3" src="https://github.com/user-attachments/assets/17e2bd95-b966-4eac-a320-4cdf552c618b" />
*Custom screen locker interface with password protection and background rendering.*

### 🤖 Discord C2 Control
<img width="660" height="794" alt="Screenshot 2026-05-01 222410" src="https://github.com/user-attachments/assets/1fac2b98-9ef8-4e4f-b9a0-f754c2cc56e6" />
*Control center showing incoming logs, screenshots, and system alerts.*

</details>

<details>
<summary><b>🇮🇩 Klik untuk melihat Screenshot</b></summary>

### 🖥️ Antarmuka Phantom Builder
<img width="1186" height="905" alt="Screenshot 2026-05-01 221918" src="https://github.com/user-attachments/assets/d004e62f-7152-4fa0-9cd9-a793dfb0ed29" />
*Interface untuk konfigurasi Bot Token, Channel ID, dan proses building executable.*

### 🔒 Phantom Locker GUI
<img width="1920" height="1080" alt="background" src="https://github.com/user-attachments/assets/c0f84254-78c3-4c93-adc7-3dd10fad4979" />
<img width="1920" height="1080" alt="2" src="https://github.com/user-attachments/assets/2532ed8a-f429-46db-aa4d-82e5e483f1e9" />
<img width="1920" height="1080" alt="3" src="https://github.com/user-attachments/assets/17e2bd95-b966-4eac-a320-4cdf552c618b" />
*Tampilan pengunci layar kustom dengan proteksi password dan render background.*

### 🤖 Kontrol Discord C2
<img width="660" height="794" alt="Screenshot 2026-05-01 222410" src="https://github.com/user-attachments/assets/1fac2b98-9ef8-4e4f-b9a0-f754c2cc56e6" />
*Pusat kendali yang menampilkan log masuk, screenshot, dan peringatan sistem.*

</details>

---

---

## 🌐 Language / Bahasa
- [English Version](#-english-version)
- [Versi Bahasa Indonesia](#-versi-bahasa-indonesia)

---

## 🇺🇸 English Version

### 🛠️ Technical Features
*   **Discord C2 Gateway**: Stealthy communication using Discord API.
*   **Full Surveillance**: Real-time screenshots (`!ss`), camera captures (`!photo`), and audio recording (`!record`).
*   **Keylogger Engine**: Captures every keystroke and dumps logs directly to Discord.
*   **System Control**: Remote GUI Locker with safe unlock feature and pseudo-BSOD (`!bsod`).
*   **Stealth Persistence**: Automatic startup injection via Windows Registry.
*   **File Binder**: Execute decoy files (PDF/EXE) while the RAT runs in the background.

### 🎨 Customization (Builder)
*   **Custom Icon**: Support for `.ico` files to disguise the payload.
*   **Theming**: In-memory Base64 background rendering for the Locker GUI.
*   **Binder System**: Select any decoy file to be opened alongside the payload.

### 📦 Installation
1.  **Prerequisites**: Windows 10/11 and Python 3.10+.
2.  **Setup Environment**:
    ```bash
    git clone [https://github.com/username/PhantomRAT.git](https://github.com/username/PhantomRAT.git)
    cd PhantomRAT
    pip install discord.py customtkinter Pillow opencv-python pyautogui sounddevice scipy pynput pyttsx3 pyperclip requests
    ```
3.  **Build**: Run `builder.py`, enter your Bot Token & Channel ID, then click **Initialize Generation**.

### ⚠️ Crucial: Re-Building Instructions
If you wish to create a new `.exe` with a different configuration, you **MUST** clean the previous build environment:
1.  **Delete `dist/` folder**: Removes the previous executable.
2.  **Delete `build/` folder**: Clears compilation cache.
3.  **Delete all `.spec` files**: Removes temporary PyInstaller configurations.
*Failure to do this may cause the new payload to use old or corrupted settings.*

---

## 🇮🇩 Versi Bahasa Indonesia

### 🛠️ Fitur Teknis
*   **Discord C2 Gateway**: Komunikasi tersembunyi menggunakan API Discord.
*   **Surveilans Lengkap**: Screenshot real-time (`!ss`), tangkapan kamera (`!photo`), dan rekaman suara (`!record`).
*   **Keylogger Engine**: Mencatat setiap ketukan keyboard dan mengirim log langsung ke Discord.
*   **Kontrol Sistem**: Locker GUI jarak jauh dengan fitur *safe unlock* dan simulasi BSOD (`!bsod`).
*   **Persistensi**: Injeksi otomatis ke Windows Registry agar tetap aktif saat startup.
*   **File Binder**: Menjalankan file *decoy* (PDF/EXE) untuk mengelabui target.

### 🎨 Kustomisasi (Builder)
*   **Ikon Kustom**: Mendukung file `.ico` untuk menyamarkan payload.
*   **Tema Visual**: Render background Base64 secara *in-memory* untuk interface Locker.
*   **Sistem Binder**: Pilih file jebakan apa pun untuk dibuka bersamaan dengan payload.

### 📦 Petunjuk Penginstalan
1.  **Prasyarat**: Windows 10/11 dan Python 3.10+.
2.  **Persiapan Lingkungan**:
    ```bash
    git clone [https://github.com/username/PhantomRAT.git](https://github.com/username/PhantomRAT.git)
    cd PhantomRAT
    pip install discord.py customtkinter Pillow opencv-python pyautogui sounddevice scipy pynput pyttsx3 pyperclip requests
    ```
3.  **Pembuatan**: Jalankan `builder.py`, masukkan Bot Token & Channel ID, lalu klik **Initialize Generation**.

### ⚠️ Penting: Instruksi Pembuatan Ulang (Re-Build)
Jika Anda ingin membuat file `.exe` baru dengan konfigurasi berbeda, Anda **WAJIB** membersihkan sisa build sebelumnya:
1.  **Hapus folder `dist/`**: Menghapus file executable lama.
2.  **Hapus folder `build/`**: Membersihkan *cache* kompilasi untuk menghindari konflik.
3.  **Hapus semua file `.spec`**: Menghapus konfigurasi sementara PyInstaller.
*Jika tidak dihapus, payload baru mungkin tetap menggunakan pengaturan dari build yang lama.*

---

## 🎮 Command List Reference

| Command | Description (EN) | Deskripsi (ID) |
| :--- | :--- | :--- |
| `!lock` | Lock target's screen | Mengunci layar target |
| `!unlock` | Remotely unlock screen | Membuka kunci layar remote |
| `!ss` | Capture screenshot | Ambil screenshot layar |
| `!keylog` | Control keylogger | Kontrol modul keylogger |
| `!shell` | Execute CMD command | Eksekusi perintah CMD |
| `!clean` | Remove traces & uninstall| Hapus jejak dan uninstall |

---

## ⚖️ Disclaimer
**FOR EDUCATIONAL PURPOSES ONLY.** Created by **R.Code**. Using this tool on systems without explicit permission is illegal. The author is not responsible for any misuse.

**HANYA UNTUK TUJUAN EDUKASI.** Dibuat oleh **R.Code**. Penggunaan alat ini pada sistem tanpa izin adalah tindakan ilegal. Penulis tidak bertanggung jawab atas penyalahgunaan alat ini.
