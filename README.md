# Folder Synchronization Script

This Python script synchronizes two folders, ensuring that the replica folder is an exact copy of the source folder. It handles file updates based on MD5 checksums and can work with nested directories.

## Features

- **One-way Synchronization**: Ensures the replica folder matches the source folder.
- **Recursive Traversal**: Supports synchronization of nested directories.
- **MD5 Checksum Verification**: Uses MD5 checksums to verify file integrity instead of relying on modification times.
- **Periodic Synchronization**: Runs at specified intervals.
- **Logging**: Logs all actions to both the console and a specified log file.
- **Graceful Shutdown**: Handles keyboard interrupts for safe termination.

## Requirements

- Python 3.8 or higher
- No additional libraries are required beyond the Python standard library.

## Usage

1. **Clone this repository** or download the script.

2. **Open a terminal** and navigate to the directory containing the script.

3. **Run the script** using the following command:

   ```
   python sync_folders.py -s <source_folder> -r <replica_folder> -i <interval_seconds> -l <log_file_path> 
   ```
- `-s`: Path to the source folder to be synchronized.
- `-r`: Path to the replica folder that will be updated to have the contents of the source folder.
- `-l`: Path to the log file.
- `-i`: Synchronization interval in seconds.