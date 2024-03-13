"""
unpack.py Helper script to batch unpack small ba2 files
version: 1.0
author: Kazumakuun
"""

import os
import subprocess
import shutil

# CHANGE THE SETTINGS BELOW FOR YOUR SETUP
# This should be the path where the mods are installed. 
# Example: D:/Mods/Fallout 4/mods
mod_path = ''

# This should be a path to your bsab.exe
# Example: D:/Tools/BSA Browser/bsab.exe
bsab_exe_path = ''

# Threshold in bytes, any file larger than this will be ignored
# Example: 5 * 1024 * 1024 (= 5 MB)
threshold = 5 * 1024 * 1024

# Process only files with the specified postfixes (case-insensitive)
postfixes = ['main.ba2', 'materials.ba2', 'misc.ba2', 'scripts.ba2']

# Files to ignore (case-insensitive). Provide only file names without directories
ignored = []


#####################################################
counter = 0
ignored = [f.lower() for f in ignored]
# List all mods in mod_path
for d in os.listdir(mod_path):
    full_path = os.path.join(mod_path, d)
    if not os.path.isdir(full_path):
        continue
    # List all files under the mod
    for f in os.listdir(full_path):
        fpath = os.path.join(full_path, f)
        backup_path = os.path.join(full_path, 'backup')
        # Unpack only *.ba2 archives and those smaller than the threshold, and that the archive is not ignored
        if (not f.lower() in ignored and
                any([postfix in f.lower() for postfix in postfixes]) and
                os.stat(fpath).st_size < threshold):
            args = [
                bsab_exe_path,
                '-e',
                fpath,
                full_path
            ]
            subprocess.run(args)

            print(f'Extracted {fpath}')

            # Make a backup of the extracted file. Create the backup folder if not already existing
            if not os.path.exists(backup_path):
                os.mkdir(backup_path)
            shutil.move(fpath, os.path.join(backup_path, f))
            counter += 1

print(f'\nDone! Processed {counter} ba2 files.')
