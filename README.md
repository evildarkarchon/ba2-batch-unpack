# ba2-batch-unpack

Nexus description: [Batch BA2 Unpacker - Avoid BA2 Limit](https://www.nexusmods.com/fallout4/mods/79593)

This is a simple Python script that extracts all small non-texture ba2 files so that you won't run over ba2 limit.

In case you don't know, Fallout 4 engine has a hard limit of 256 non-texture BA2 archives that can be loaded in your 
game [sauce](https://cdn.discordapp.com/attachments/901294918914412604/1115644969168945163/ba2_limit.png?ex=6602d858&is=65f06358&hm=b73ccf8ef517855638ccf2f0cfd9ca8305be8c14ff7783b77e4770963ec7398e&). 
If you have more, chances are your game will crash on load, behave erratically, and all kinds of fun stuff.

It has been suggested that Buffout users can use a ba2 limit bypass. However, while the trick allows the game to load, 
sometimes you get broken atlas (texture) regardless. The best solution is to reduce your ba2 count.

For me, that means to manually extract hundreds of small ba2 files and back them up in case something breaks. Yucks! 
This helper script hopefully frees you from all that manual work. Just 1 minute of easy configuration and it will take care of the rest :)


## AV False Positives

The AIO version is known to cause false positive on some antivirus software 
(MS defender, BitDefender, etc.). This is due to Nuitka that I use to pack the py file. Apparently it is also used in
some... less legal ways, which causes Nuitka-compiled files to be blacklisted in some heuristics. If you know any better 
way to pack py files please let me know!


## Usage - AIO Version

The AIO version has all dependencies packed in - no need for manual Python 3 or BSA Browser installs! :D

To run it, unzip the **entire** folder to a convenient place, like your Desktop.
Then, simply double click unpack.exe to get started.
The program will guide you through the entire unpacking process.

You can edit the ignore.txt in the folder to specify the files that you do not want to extract.

## Usage - Script Version

You will need the following dependencies:

- [Python 3](https://www.python.org/downloads)
  All recent Python 3 releases should work just fine.
- [BSA Browser](https://www.nexusmods.com/skyrimspecialedition/mods/1756)
  For your convenience, a CLI version is placed inside the release archive. If you download the source directly,
  you will need to put `bsab.exe` in `/bin/bsab/` folder.


First, unzip the **entire** folder to a convenient place, like your Desktop.

Then, run the following command in cmd/Windows Terminal/whatever terminal in the folder **where you extracted the files**, 
and enter:

`python3 ./unpack.py`

The extraction and backup will then proceed automatically.

You can edit the `ignore.txt` in the folder to specify the files that you do not want to extract.

By default, the script will proceed in interactive mode (like the exe version). However if you want to automate 
the process or wish to manually configure the settings, please read the "Manual Configuration" section.

## Special Considerations

Extracting small ba2 files should not impact your performance or destabilize your game in a significant way.

However, since loose files always wins conflicts against ba2 files, newly extracted loose files may cause overwriting
/conflict issues that did not exist before.

This is why it is recommended to carefully look at your load order and look out for conflicts. Mod managers such as MO2 
makes it easy to see file conflicts but it doesn't check against ba2 
(by default, you can turn on that option in Settings > Workarounds > Enable archives parsing) (thanks Mimicry for the tip!). 
You might need manual checks to make sure everything works as expected.

## Manual Configuration

You **do NOT** need to worry about it anymore, unless you specifically want manual configurations.

The following parameters can be configured to suit your needs. Parameters with an asterisk (*) next to it must be 
changed before running the script.

- **`interactive`***: you must set it to False for your manual configurations to be effective.
- **`mod_path`***: this should be the path to the mod folder in your mod manager. In MO2 it's Open > Open Mods folder. 
  In Vortex it's Open > Open Mod Staging Folder. You can technically supply your Fallout 4 root folder (if you don't use 
  any mod manager), but I haven't tested this approach.
- **`threshold`**: this is the maximum size of bsa to extract, in bytes. Thus 5 * 1024 * 1024 gives 5MB, while 200 * 1024 
  gives 200KB. Any file larger than this will not be touched.
- **`postfixes`**: this is the file postfixes (case-insensitive) that should be extracted. The default should be fine for most 
  cases. For example, "main.ba2" matches all files that ends with "main.ba2" (abcmod - main.ba2, xyzmod - main.ba2, etc.).
  Note: you do not need to extract texture BA2 files, they are exempt from the BSA limit.
- **`bsab_exe_path`**: this should point directly to your bsab.exe from your BSA Browser installation. A copy of bsab.exe 
  is already included in the download, and you can leave the default unchanged. 
- **`ignored`**: if you have any file that should not be extracted, you can list them here (case-insensitive). Use 
  standard Python string array format.
  
  Example: ['abcmod - main.ba2', 'xyzmod - main.ba2']

## Credits

AlexxEG for BSA Browser

## Licensing

The source code is released under GNU 