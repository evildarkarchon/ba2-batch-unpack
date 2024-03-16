"""
unpack.py Helper script to batch unpack small ba2 files
version: 1.0
author: Kazumakuun
"""

import os
import re
import shutil
import subprocess
import tkinter
from tkinter import filedialog

from tqdm import tqdm

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

ignored = []
ignored_txt = './ignore.txt'

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
# Hide empty tkinter window
tkinter.Tk().withdraw()

units = {'B': 1, 'KB': 2 ** 10, 'MB': 2 ** 20, 'GB': 2 ** 30, 'TB': 2 ** 40}
auto_threshold = False

all_ba2_sorted = []


def parse_size(size):
    size = size.upper()
    if not re.match(r' ', size):
        size = re.sub(r'([KMGT]?B)', r' \1', size)
    number, unit = [string.strip() for string in size.split()]
    return int(float(number) * units[unit])


def end():
    print('All done! You can now close this window.')
    input()
    exit(0)


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


def populate_targets(max_size):
    global all_ba2_sorted
    all_ba2 = []
    for d in os.listdir(mod_path):
        full_path = os.path.join(mod_path, d)
        if not os.path.isdir(full_path):
            continue
        # List all files under the mod
        for ba2 in os.listdir(full_path):
            fpath = os.path.join(full_path, ba2)
            # Add only *.ba2 archives and those smaller than the threshold (if supplied),
            # and that the archive is not ignored
            if not max_size:
                if (not ba2.lower() in ignored and
                        any([postfix in ba2.lower() for postfix in postfixes])):
                    all_ba2.append(fpath)
            else:
                if (not ba2.lower() in ignored and
                        any([postfix in ba2.lower() for postfix in postfixes]) and
                        os.stat(fpath).st_size <= threshold):
                    all_ba2.append(fpath)

    all_ba2_sorted = sorted(all_ba2, key=lambda f: os.stat(f).st_size).reverse()


def determine_threshold():
    return os.stat(all_ba2_sorted[235]).st_size


# Interactive prompts
def choose_mod_folder():
    global threshold
    print('Please choose your mod folder.\n')
    folder = filedialog.askdirectory(initialdir=os.getcwd(), mustexist=True, title='Please choose your mod folder')
    # Update the threshold accordingly after the folder change
    if auto_threshold:
        populate_targets(None)
        threshold = determine_threshold()
    return folder


def set_threshold():
    global auto_threshold
    print('What is the maximum size of ba2 file to extract? (e.g. 500kb, 3MB)\n'
          'Type \"auto\" if you want to let the program automatically determine that for you\n'
          '(i.e. extract just enough archives to get below the ba2 limit).')
    thr = input('Threshold: ')

    if thr == 'auto' or thr == '\"auto\"':
        auto_threshold = True
        populate_targets(None)
        return determine_threshold()
    auto_threshold = False
    return parse_size(thr)


def confirm_postfixes():
    global postfixes
    post_ok = input(f'Is are these file postfix ok? (Y/n)\n'
                    f'{postfixes}')
    if not (post_ok == '' or post_ok == 'y' or post_ok == 'Y'):
        has_error = False
        while True:
            user_postfixes = input('Please enter file postfixes to extract, separated by commas.\n'
                                   'E.g.: main.ba2,scripts.ba2\n').split()
            for postfix in user_postfixes:
                postfix = postfix.lower().strip()
                if postfix[-4:] is not '.ba2':
                    print(f'{postfix} does not end with .ba2. Please correct the entry.')
                    has_error = True
            if not has_error:
                return user_postfixes
            else:
                has_error = False


def correct_setting():
    global mod_path, threshold, postfixes
    print('\nWhich setting would you like to correct? Enter the corresponding number to continue.\n'
          '1. Mod folder path\n'
          '2. Extraction threshold\n'
          '3. File postfixes to extract\n'
          '0. It\'s all good actually...\n')

    while True:
        response = input()

        if response == '1':
            mod_path = choose_mod_folder()
            break
        elif response == '2':
            threshold = set_threshold()
            break
        elif response == '3':
            postfixes = confirm_postfixes()
            break
        elif response == '0':
            break
        else:
            print('Invalid response. Please try again: ')


def review_settings():
    while True:
        print(f'Setup complete. Please review the following settings.\n'
              f'Mod folder path: {mod_path}\n'
              f'Extraction threshold: {threshold} bytes\n'
              f'File postfixes to extract: {postfixes}\n'
              f'Ignored files: {ignored}\n'
              f'bsab.exe path: {bsab_exe_path}\n')

        response = input('Is the above settings correct?\n'
                         '(Y)es, (n)o, (d)ry run, or (e)xit: ')
        if response == 'Y' or response == 'y' or response == '':
            return 'y'
        elif response == 'N' or response == 'n':
            correct_setting()
        elif response == 'D' or response == 'd':
            return 'd'
        elif response == 'E' or response == 'e':
            end()
        else:
            print('Invalid response. Please try again.')


def do_processing():
    total_files = 0

    populate_targets(threshold)
    for file in tqdm(all_ba2_sorted[235:]):
        base_path = os.path.dirname(file)
        backup_path = os.path.join(base_path, 'backup')
        args = [
            bsab_exe_path,
            '-e',
            file,
            base_path
        ]
        subprocess.run(args)

        print(f'Extracted {file}')

        # Make a backup of the extracted file. Create the backup folder if not already existing
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        shutil.move(file, os.path.join(backup_path, file))
        total_files += 1
    print(f'\nDone! Processed {total_files} ba2 files.')


def dry_run():
    try:
        with open('./preview.txt', 'w') as preview_file:
            preview_file.write(f'Preview of ba2 files to be extracted.\n'
                               f'Total files to extract: {max(len(all_ba2_sorted) - 235, 0)}'
                               f'File Name\t\t\t\t\tSize\n')
            for file in all_ba2_sorted[235:]:
                preview_file.write(f'{file}\t\t\t\t\t{os.stat(file).st_size}\n')
            preview_file.flush()
            preview_file.close()
    except (OSError, PermissionError, IOError) as err:
        print(f'Warning: error creating preview.txt: {err}.\n')
        return

    print('A file named \"preview.txt\" has been created in the folder where this script is.\n'
          'You can proceed to extraction if you like, or change some settings.\n')
    response = input('Would you like to proceed with the extraction? (Y)es or (n)o: ')

    if response == 'Y' or response == 'y':
        return True
    else:
        return False


print('===========================================================================')
print('Welcome to Batch BA2 Unpacker by KazumaKuun')
print('===========================================================================')

# Main CLI loop
mod_path = choose_mod_folder()
threshold = set_threshold()
postfixes = confirm_postfixes()

while True:
    user_response = review_settings()

    if user_response == 'y':
        do_processing()
        end()
    elif user_response == 'd':
        if dry_run():
            do_processing()
            end()
