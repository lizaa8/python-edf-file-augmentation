# Python EDF File Augmentation

This project is a Python program that automates the process of copying, renaming, and organizing EDF files. It also includes verification checks to make sure the new files are created correctly without changing the originals.

## How It Works

- Searches through a folder to find all EDF files.
- Creates a copy of each file with a unique, randomly generated numerical filename.
- Updates the timestamps of the copied files to the 10th of the previous month.
- Saves a mapping file to keep track of which original file each copy came from.
- Sorts the new filenames numerically and saves them to a text file.
- Runs several verification checks to make sure the files were processed correctly.

## Technologies Used

- Python
- pathlib
- shutil
- os
- datetime
- random

## Verification Checks

The program checks that:
- The number of generated files matches the number of original files.
- All generated filenames are unique and numerical.
- The copied files have the correct modification dates.
- The original files remain unchanged.
- Each copied file can be traced back to its original.
- The input and output folders are separate.

## How to Run

Make sure Python 3 is installed.

Download the project and create a folder called `files` in the same directory as the Python script.

Place your EDF files inside the `files` folder.

Run the program:

```bash
python edf_file_augmentation.py
```

The program will create an `augmented_files` folder containing the copied files. It will also generate `file_mapping.txt` and `sorted_filenames.txt`.

## Demo

https://github.com/user-attachments/assets/96217b32-fabf-43c2-b622-2a8b55c80e18
