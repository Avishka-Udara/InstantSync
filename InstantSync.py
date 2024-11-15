import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from threading import Thread
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw


# Helper function to copy a file if it's missing or modified
def copy_if_needed(src, dst):
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied: {src} to {dst}")


# Watchdog event handler for real-time monitoring
class BackupHandler(FileSystemEventHandler):
    def __init__(self, source_folder, backup_folder):
        self.source_folder = source_folder
        self.backup_folder = backup_folder

    def on_modified(self, event):
        if not event.is_directory:
            src = event.src_path
            dst = os.path.join(self.backup_folder, os.path.relpath(src, self.source_folder))
            copy_if_needed(src, dst)


# Main backup application
class BackupApp:
    def __init__(self, root):
        self.root = root
        self.source_folder = tk.StringVar()
        self.backup_folder = tk.StringVar()
        self.is_running = False

        self.progress_var = tk.DoubleVar()
        self.observer = None
        self.tray_icon = None
        self.is_background = False

        # Setup GUI
        self.create_gui()

    def create_gui(self):
        self.root.title("InstantSync - Backup Application")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Source folder selection
        tk.Label(self.root, text="Source Folder:").pack(pady=5, anchor="w", padx=20)
        source_frame = tk.Frame(self.root)
        source_frame.pack(pady=5)
        tk.Entry(source_frame, textvariable=self.source_folder, width=40).pack(side=tk.LEFT)
        tk.Button(source_frame, text="Browse", command=lambda: self.select_folder(self.source_folder)).pack(side=tk.LEFT)

        # Backup folder selection
        tk.Label(self.root, text="Backup Folder:").pack(pady=5, anchor="w", padx=20)
        backup_frame = tk.Frame(self.root)
        backup_frame.pack(pady=5)
        tk.Entry(backup_frame, textvariable=self.backup_folder, width=40).pack(side=tk.LEFT)
        tk.Button(backup_frame, text="Browse", command=lambda: self.select_folder(self.backup_folder)).pack(side=tk.LEFT)

        # Progress bar
        tk.Label(self.root, text="Progress:").pack(pady=5, anchor="w", padx=20)
        self.progress_bar = Progressbar(self.root, variable=self.progress_var, mode="determinate", maximum=100)
        self.progress_bar.pack(pady=5, fill="x", padx=20)

        # Start/Stop buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        self.start_button = tk.Button(button_frame, text="Start Backup", command=self.start_backup)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.stop_button = tk.Button(button_frame, text="Stop Backup", command=self.stop_backup, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        self.background_button = tk.Button(button_frame, text="Run in Background", command=self.run_in_background)
        self.background_button.pack(side=tk.LEFT, padx=10)

        # Status label
        self.status_label = tk.Label(self.root, text="Idle")
        self.status_label.pack(pady=10)

    def select_folder(self, var):
        folder = filedialog.askdirectory()
        if folder:
            var.set(folder)

    def initial_sync(self, source, backup):
        total_files = sum(len(files) for _, _, files in os.walk(source))
        copied_files = 0

        for root_dir, _, files in os.walk(source):
            for file in files:
                src = os.path.join(root_dir, file)
                dst = os.path.join(backup, os.path.relpath(src, source))
                if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                    copy_if_needed(src, dst)
                    copied_files += 1
                    self.progress_var.set((copied_files / total_files) * 100)
                    self.status_label.config(text=f"Copied {copied_files}/{total_files} files")
                    self.root.update()

    def start_backup(self):
        source = self.source_folder.get()
        backup = self.backup_folder.get()

        if not os.path.isdir(source) or not os.path.isdir(backup):
            messagebox.showerror("Error", "Please select valid folders")
            return

        self.status_label.config(text="Starting initial sync...")
        self.root.update()

        # Initial synchronization
        Thread(target=self.initial_sync, args=(source, backup), daemon=True).start()

        # Start monitoring
        self.observer = Observer()
        self.observer.schedule(BackupHandler(source, backup), source, recursive=True)
        self.observer.start()
        self.is_running = True

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Backup running. Monitoring for changes...")
        self.progress_var.set(0)

    def stop_backup(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Backup stopped.")

    def run_in_background(self):
        if not self.is_background:
            # Minimize to system tray
            self.tray_icon = Icon(
                "InstantSync",
                self.create_tray_icon_image(),
                "InstantSync",
                menu=Menu(
                    MenuItem("Show", self.show_window),
                    MenuItem("Exit", self.exit_app)
                ),
            )
            Thread(target=self.tray_icon.run, daemon=True).start()
            self.root.withdraw()
            self.is_background = True

    def create_tray_icon_image(self):
        image = Image.new("RGB", (64, 64), color="blue")
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill="white")
        return image

    def show_window(self):
        self.tray_icon.stop()
        self.root.deiconify()
        self.is_background = False

    def exit_app(self):
        if self.is_running:
            self.stop_backup()
        self.root.destroy()
        if self.tray_icon:
            self.tray_icon.stop()

    def on_closing(self):
        if self.is_running:
            self.stop_backup()
        self.root.destroy()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
