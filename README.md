# InstantSync

InstantSync is a real-time folder synchronization tool designed to monitor a source folder and back up modified or new files to a destination folder. The tool is user-friendly, with a graphical interface and advanced features like a progress bar, background running mode, and more.

## Features

- **Real-time Monitoring**: Instantly detects and backs up new or modified files.
- **Selective Backup**: Copies only files that don't already exist in the backup folder or are newer.
- **User-friendly GUI**: Easy-to-use interface built with Python's Tkinter.
- **Progress Tracking**: Visual progress bar to track initial synchronization and backup status.
- **Background Mode**: Run the backup process in the background.
- **Start/Stop Backup**: Controls to manage the backup process manually.
- **Executable**: Includes a precompiled `InstantSync.exe` for direct use without Python installation.

## How to Use

### 1. Running the Application
If you want to use the precompiled executable:
1. Download the repository.
2. Navigate to the `InstantSync.exe` file in the repository.
3. Double-click the file to launch the application.

#### If you prefer running the Python script:
1. Ensure Python 3.12+ is installed.
2. Install the required dependencies:

       pip install -r requirements.txt

Run the application:

    python InstantSync.py

### 2. Usage Steps

Select the Source Folder (the folder to monitor).
Select the Backup Folder (the folder where backups are stored).
Click Start Backup to begin.
Optionally, use the Run in Background button to minimize the application and keep it running in the background.
Click Stop Backup to halt the backup process.

### 3. Requirements

Python 3.12 or later (if running the .py file).
The following Python packages:

    watchdog
    tkinter

## Building from Source

#### If you want to create your own executable:
Install PyInstaller:
    
    pip install pyinstaller

#### Build the executable:

    pyinstaller --onefile --windowed InstantSync.py

The compiled executable will be located in the dist folder.


## Contributing

Contributions are welcome! Feel free to fork the repository and create a pull request.

## Author
        https://github.com/Avishka-Udara/InstantSync.git
