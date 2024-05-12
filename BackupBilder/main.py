#Created by DY
#v1.0
import hashlib
import shutil
import os
import datetime
import logging
import configparser

def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    return hashlib.md5(content).hexdigest()

def create_default_config():
    config = configparser.ConfigParser()
    config['BackupSettings-dy'] = {
        'monitore_file' : 'monitoreme.txt',
        'backup_dir' : '',
        'log_file' : 'dybackup.log',
        'days_to_keep_backups' : '365'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def backup_file(source_file, dest_dir):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(dest_dir, f'backup_{os.path.basename(source_file)}_{timestamp}')
    shutil.copy2(source_file, backup_file)
    return backup_file

def remove_old_backups(backup_dir, days_to_keep):
    current_time = datetime.datetime.now()
    for backup_folder in os.listdir(backup_dir):
        backup_path = os.path.join(backup_dir, backup_folder)
        if os.path.isdir(backup_path):
            backup_time_str = backup_folder.replace("backup_", "")
            backup_time = datetime.datetime.strptime(backup_time_str, '%Y%m%d_%H%M%S')
            if (current_time - backup_time).days > days_to_keep:
                shutil.rmtree(backup_path)
                logging.info(f"Old backup '{backup_folder}' removed.")

def main():
    if not os.path.exists('config.ini'):
        create_default_config()
        print("Default config file 'config.ini' created. Please update it with the correct paths.")
        return
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    cron_file_path = config.get('BackupSettings-dy', 'monitore_file')
    backup_dir = config.get('BackupSettings-dy', 'backup_dir')
    days_to_keep_backups = config.getint('BackupSettings-dy', 'days_to_keep_backups')
    log_file = config.get('BackupSettings-dy', 'log_file')   
    if not log_file.strip():
        log_file='filebkp.log'
        
    if not log_file.strip():
        days_to_keep_backups=365
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    if not cron_file_path.strip() or not os.path.exists(cron_file_path.strip()):
        logging.error("Source directory is empty or does not exist. Skipping backup.")
        return

    if not backup_dir.strip():
        logging.error("Backup directory is empty. Skipping backup.")
        return
    
    if not os.path.exists(backup_dir):
        logging.error("Backup Dir not found.Creating Dir.")
        os.makedirs(backup_dir)

    if not os.path.exists(cron_file_path):
        logging.error("File not found. Please provide the correct path.")
        return

    if not os.path.isfile(cron_file_path) or os.stat(cron_file_path).st_size == 0:
        logging.error("File is empty or invalid. Skipping backup.")
        return
    
    current_hash = calculate_hash(cron_file_path)
    hash_file_path = 'hash_file.txt'
    previous_hash = None
    if os.path.exists(hash_file_path):
        with open(hash_file_path, 'r') as f:
            previous_hash = f.read().strip()

    if current_hash == previous_hash:
        logging.info("No change in the cron file. Skipping backup.")
    else:
        backup_dir_path = backup_file(cron_file_path, backup_dir)
        logging.info(f"Backup taken successfully at '{backup_dir_path}'. Hash:{current_hash}")
        with open(hash_file_path, 'w') as f:
            f.write(current_hash)
    remove_old_backups(backup_dir, days_to_keep_backups)

if __name__ == "__main__":
    main()
