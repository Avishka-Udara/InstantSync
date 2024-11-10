# InstantSync

InstantSync is a Python-based folder synchronization and backup utility with a user-friendly graphical interface. This tool monitors a specified source folder and automatically backs up modified files to a specified backup location, keeping the original folder structure intact. InstantSync includes a retry mechanism to handle file access issues and performs an initial folder sync to ensure the backup folder mirrors the source folder before monitoring begins.
Features


*Automated Folder Sync: Instantly syncs files from a source folder to a backup folder whenever changes are detected.
GUI Interface: Easy-to-use interface built with Tkinter, allowing users to select source and backup folders.
Retry Mechanism: Handles file access issues, such as permission errors, by retrying file copies up to 5 times.
Initial Sync: On the first run, mirrors the entire source folder structure in the backup location.
Real-Time Monitoring: Uses watchdog to monitor changes in real time, automatically backing up modified files.*

### Requirements

    Python 3.6 or higher
    Required Python packages (install via pip):
        watchdog
        tkinter (usually included with Python)
        psutil (optional, if additional file lock checking is needed)

### Installation

_Clone the repository:_

```git clone https://github.com/Avishka-Udara/InstantSync.git```
```cd InstantSync```


_Install dependencies:_

    pip install watchdog
  # Optional: if using psutil for file lock checks
    pip install psutil

### Usage

    Run InstantSync:

    python InstantSync.py

    Using the GUI:
        Source Folder: Click "Browse" to select the folder you want to back up.
        Backup Folder: Click "Browse" to choose the destination folder where the backup will be saved.
        Click Start Backup to initiate the backup process. An initial sync of the source folder is performed to ensure the backup folder matches the source folder structure.
        Monitoring: After the initial sync, InstantSync will monitor the source folder for changes and automatically copy modified files to the backup location.

    Stopping the Backup Process:
        To stop monitoring and close the app, simply close the window.

### Code Overview

The main components of InstantSync are:

    BackupHandler:
        Monitors file changes in the source folder using watchdog.
        Copies modified files to the backup folder with a retry mechanism.

    copy_with_retry:
        Helper function to handle file copying with retry logic.
        Attempts to copy files up to 5 times if a permission error occurs.

    BackupApp:
        Manages the GUI and folder selection.
        Starts the initial sync and sets up the observer to monitor changes.

### Optional Configuration

For additional reliability, InstantSync can use the psutil library to skip copying files if they are actively locked by another process. Uncomment the is_file_locked function and relevant parts of the code if file lock checking is required.
Example

    Select C:\Users\YourUser\Documents\Projects as the Source Folder.
    Select D:\Backups\ProjectBackups as the Backup Folder.
    Click Start Backup. InstantSync will first copy all files and subfolders from Projects to ProjectBackups.
    Modify or add files to the Projects folder. InstantSync will automatically back up the changes to ProjectBackups.

### Troubleshooting

    File Locked Errors: If a file is being used by another process and cannot be backed up, InstantSync will retry up to 5 times.
    Permission Errors: Ensure InstantSync has write permissions for the backup location.

### License

This project is licensed under the MIT License.

Replace https://github.com/Avishka-Udara/InstantSync.git with your actual GitHub repository link if you plan to publish this project on GitHub. Let me know if there are any specific customizations you’d like to add!
