import os
import shutil
import time
import logging
import argparse
import hashlib

def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def setup_logging(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Function to synchronize folders (including subdirectories)
def sync_folders(source, replica, logger):
    # Walk through the source directory recursively
    for dirpath, dirnames, filenames in os.walk(source):
        # Calculate the relative path from the source to maintain structure in replica
        relative_path = os.path.relpath(dirpath, source)
        replica_dirpath = os.path.join(replica, relative_path)

        # If the directory does not exist in the replica, create it
        if not os.path.exists(replica_dirpath):
            os.makedirs(replica_dirpath)
            logger.info(f"Created directory: {replica_dirpath}")

        # Copy or update files from the source to the replica
        for file_name in filenames:
            source_file = os.path.join(dirpath, file_name)
            replica_file = os.path.join(replica_dirpath, file_name)

            if not os.path.exists(replica_file):
                shutil.copy2(source_file, replica_file)
                logger.info(f"Copied file: {source_file} to {replica_file}")
            else:
                if calculate_md5(source_file) != calculate_md5(replica_file):
                    shutil.copy2(source_file, replica_file)
                    logger.info(f"Updated file: {replica_file} to match {source_file}")

    # Walk through the replica directory to remove files or directories that no longer exist in the source
    for dirpath, dirnames, filenames in os.walk(replica):
        relative_path = os.path.relpath(dirpath, replica)
        source_dirpath = os.path.join(source, relative_path)

        # Remove files in replica that no longer exist in the source
        for file_name in filenames:
            replica_file = os.path.join(dirpath, file_name)
            source_file = os.path.join(source_dirpath, file_name)

            if not os.path.exists(source_file):
                os.remove(replica_file)
                logger.info(f"Removed file: {replica_file}")

        # Remove directories in replica that no longer exist in the source
        for dirname in dirnames:
            replica_subdir = os.path.join(dirpath, dirname)
            source_subdir = os.path.join(source_dirpath, dirname)

            if not os.path.exists(source_subdir):
                shutil.rmtree(replica_subdir)
                logger.info(f"Removed directory: {replica_subdir}")


def main():
    parser = argparse.ArgumentParser(description="Folder Synchronization Script")
    parser.add_argument("-s", required=True, help="Path to the source folder")
    parser.add_argument("-r", required=True, help="Path to the replica folder")
    parser.add_argument("-l", required=True, help="Path to the log file")
    parser.add_argument("-i", type=int, required=True, help="Synchronization interval in seconds")
    args = parser.parse_args()

    logger = setup_logging(args.l)

    try:
        while True:
            logger.info("Starting folder synchronization...")
            sync_folders(args.s, args.r, logger)
            logger.info(f"Synchronization complete. Sleeping for {args.i} seconds.")
            time.sleep(args.i)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected. Exiting program gracefully.")
        print("\nProgram terminated by user.")


if __name__ == "__main__":
    main()
