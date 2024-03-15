'''
unpack.py Helper script to batch unpack small ba2 files
version: 1.0
author: Kazumakuun
'''

import os
import subprocess
import shutil
import tkinter
import re

from tkinter import filedialog

# CHANGE THE SETTINGS BELOW FOR YOUR SETUP
# Set interactive to false if you wish to manually input these settings
interactive = True

# This should be the path where the mods are installed
# Example: D:/Mods/Fallout 4/mods
mod_path = ''

# This should be a path to your bsab.exe
# Example: D:/Tools/BSA Browser/bsab.exe
bsab_exe_path = ''

# Threshold in bytes, any file larger than this will be ignored
# Example: 5 * 1024 * 1024 (= 5 MB)
threshold = 0

# Process only files with the specified postfixes (case-insensitive)
postfixes = ['main.ba2', 'materials.ba2', 'misc.ba2', 'scripts.ba2']

# Ignore list has been moved to an external file
# Please edit 'ignore.txt' to add ignored files


#####################################################

print('===========================================================================')
print('Welcome to Batch BA2 Unpacker by KazumaKuun')
print('===========================================================================')

ignored = []
ignored_txt = './ignore.txt'
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
# Hide empty tkinter window
tkinter.Tk().withdraw()

units = {'B': 1, 'KB': 2**10, 'MB': 2**20, 'GB': 2**30, 'TB': 2**40}


def parse_size(size):
    size = size.upper()
    if not re.match(r' ', size):
        size = re.sub(r'([KMGT]?B)', r' \1', size)
    number, unit = [string.strip() for string in size.split()]
    return int(float(number)*units[unit])


# Process the ignore file list
try:
    with open(ignored_txt, 'r') as f:
        count_ignored = 0
        for line in f:
            # Ignore lines that start with '#'
            if line[0] == '#':
                continue
            ignored.append(line.lower())
            count_ignored += 1
        print(f'Ignore file processed: {count_ignored} files added as ignored files.')
except (FileNotFoundError, PermissionError, OSError) as e:
    print(f'Warning: error opening {ignored_txt}: {e}')

# Interactive prompts
print('Please choose your mod folder.\n')
mod_path = filedialog.askdirectory(initialdir=os.getcwd(), mustexist=True, title='Please choose your mod folder')

threshold = input('What is the maximum size of ba2 file to extract? (e.g. 500kb, 3MB)\n')
threshold = parse_size(threshold)

post_ok = input(f'Is are these file postfix ok? (Y/n)\n'
                f'{postfixes}')
if not (post_ok == '' or post_ok == 'y' or post_ok == 'Y'):
    flag = True
    while flag:
        user_postfixes = input('Please enter file postfixes to extract, separated by commas.\n'
                               'E.g.: main.ba2,scripts.ba2\n').split()
        for postfix in user_postfixes:
            postfix = postfix.lower().strip()
            if postfix[-4:] is not '.ba2':
                print(f'{postfix} does not end with .ba2. Please correct the entry.')
                flag = False
        if flag:
            postfixes = user_postfixes
        flag = not flag

print()
print(f'Setup complete. Please review the following settings.\n'
      f'Mod folder path: {mod_path}\n'
      f'Extraction threshold: {threshold} bytes\n'
      f'File postfixes: {postfixes}\n'
      f'Ignored files: {ignored}\n'
      f'bsab.exe path: {bsab_exe_path}\n')

input('Is the above settings correct?\n'
      '(Y)es, (N)o, (D)ry run, or (E)xit: ')

total_files = 0
# List all mods in mod_path
for d in os.listdir(mod_path):
    print(f'Total files extracted: {total_files}')
    print(f'Checking {d}')
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
            total_files += 1
    print(LINE_UP, end=LINE_CLEAR)
    print(LINE_UP, end=LINE_CLEAR)

print(f'\nDone! Processed {total_files} ba2 files.')

