import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import filedialog, messagebox

# Helper function to attempt file copy with retries
def copy_with_retry(src, dst, retries=5, delay=1):
    for _ in range(retries):
        try:
            shutil.copy2(src, dst)
            print(f"Backed up: {src} to {dst}")
            return
        except PermissionError:
            time.sleep(delay)
        except Exception as e:
            print(f"Error copying {src}: {e}")
            break

class BackupHandler(FileSystemEventHandler):
    def __init__(self, source_folder, backup_location):
        self.source_folder = source_folder
        self.backup_location = backup_location

    def on_modified(self, event):
        if not event.is_directory:
            src = event.src_path
            dst = os.path.join(self.backup_location, os.path.relpath(src, self.source_folder))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            copy_with_retry(src, dst)

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.source_folder = tk.StringVar()
        self.backup_folder = tk.StringVar()

        # GUI setup
        self.create_gui()

    def create_gui(self):
        tk.Label(self.root, text="Source Folder:").pack()
        tk.Entry(self.root, textvariable=self.source_folder, width=40).pack()
        tk.Button(self.root, text="Browse", command=lambda: self.select_folder(self.source_folder)).pack()
        tk.Label(self.root, text="Backup Folder:").pack()
        tk.Entry(self.root, textvariable=self.backup_folder, width=40).pack()
        tk.Button(self.root, text="Browse", command=lambda: self.select_folder(self.backup_folder)).pack()
        tk.Button(self.root, text="Start Backup", command=self.start_backup).pack()

    def select_folder(self, var):
        folder = filedialog.askdirectory()
        if folder:
            var.set(folder)

    def start_backup(self):
        source, backup = self.source_folder.get(), self.backup_folder.get()
        if not os.path.isdir(source) or not os.path.isdir(backup):
            messagebox.showerror("Error", "Please select valid folders")
            return

        # Initial sync
        for root_dir, _, files in os.walk(source):
            for file in files:
                src = os.path.join(root_dir, file)
                dst = os.path.join(backup, os.path.relpath(src, source))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                    copy_with_retry(src, dst)

        # Start monitoring for changes
        self.observer = Observer()
        self.observer.schedule(BackupHandler(source, backup), source, recursive=True)
        self.observer.start()
        messagebox.showinfo("Backup Started", "Folder backup has started!")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()
        self.root.destroy()

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.title("InstantSync")
    app = BackupApp(root)
    root.mainloop()
