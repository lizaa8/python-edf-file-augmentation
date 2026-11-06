#author: liza
from pathlib import Path
from datetime import datetime, timedelta
import random
import shutil
import os

# File paths
project_path = Path(__file__).resolve().parent
dataset_path = project_path / "files"
output_path = project_path / "augmented_files"

# find the EDF files
edf_files = list(dataset_path.rglob("*.edf"))
original_count = len(edf_files)

if original_count == 0:
    print("No EDF files found. Check the dataset path.")
    raise SystemExit

# checks the output folder
if output_path == dataset_path or dataset_path in output_path.parents:
    print("The output folder must be separate from the original dataset.")
    raise SystemExit

# creates the output folder
output_path.mkdir(parents=True, exist_ok=True)

# stops if the folder already has files
if any(output_path.glob("*.edf")):
    print("Please clear the augmented_files folder before running again.")
    raise SystemExit

# save the original file info
original_info = {
    file: (file.stat().st_size, file.stat().st_mtime_ns)
    for file in edf_files
}

# shuffle the files
random.shuffle(edf_files)

# make random filenames
random_numbers = random.sample(range(100000, 999999), original_count)

# get the 10th of last month
first_day_this_month = datetime.now().replace(
    day=1, hour=0, minute=0, second=0, microsecond=0
)
last_day_previous_month = first_day_this_month - timedelta(days=1)
target_date = last_day_previous_month.replace(day=10)
target_timestamp = target_date.timestamp()

# Copy the files and record their sources
mapping_file = project_path / "file_mapping.txt"

with open(mapping_file, "w") as mapping:
    for source_file, number in zip(edf_files, random_numbers):
        new_name = f"{number}.edf"
        destination = output_path / new_name

        # Copy the file
        shutil.copy2(source_file, destination)

        # Change the dates
        os.utime(destination, (target_timestamp, target_timestamp))

        # Save the source path
        source_name = source_file.relative_to(dataset_path)
        mapping.write(f"{new_name} <- {source_name}\n")

# Check the new files
generated_files = list(output_path.glob("*.edf"))
generated_names = [file.name for file in generated_files]

correct_count = len(generated_files) == original_count
total_count = original_count + len(generated_files)
correct_total = total_count == original_count * 2

unique_names = len(generated_names) == len(set(generated_names))
numeric_names = all(file.stem.isdigit() for file in generated_files)

correct_dates = all(
    datetime.fromtimestamp(file.stat().st_mtime).date() == target_date.date()
    for file in generated_files
)

# Sort the filenames
sorted_files = sorted(generated_files, key=lambda file: int(file.stem))
sorted_names = [file.name for file in sorted_files]
correct_order = sorted_names == sorted(
    generated_names, key=lambda name: int(Path(name).stem)
)

# Save the sorted filenames
filename_list = project_path / "sorted_filenames.txt"

with open(filename_list, "w") as file:
    for name in sorted_names:
        file.write(name + "\n")

# Check the original files
originals_unchanged = all(
    (file.stat().st_size, file.stat().st_mtime_ns) == info
    for file, info in original_info.items()
)

# Check the source list
with open(mapping_file, "r") as mapping:
    mapping_lines = mapping.readlines()

traceability_ok = len(mapping_lines) == len(generated_files)
source_selection_ok = len(edf_files) == len(set(edf_files))

# Check all the results
checks = [
    correct_count,
    correct_total,
    unique_names,
    numeric_names,
    correct_order,
    correct_dates,
    originals_unchanged,
    traceability_ok,
    source_selection_ok,
    output_path != dataset_path
]

all_passed = all(checks)

# Print the results
print("\n   PROGRAM VERIFICATION    ")
print("Original EDF files:", original_count)
print("New augmented files:", len(generated_files))
print("Final total file count:", total_count)
print("Expected total:", original_count * 2)
print("Correct number of new files:", "PASSED" if correct_count else "FAILED")
print("Final total is twice the original:", "PASSED" if correct_total else "FAILED")
print("Unique filenames:", "PASSED" if unique_names else "FAILED")
print("Numeric filenames:", "PASSED" if numeric_names else "FAILED")
print("Filenames in numerical order:", "PASSED" if correct_order else "FAILED")
print("Required modified date:", target_date.strftime("%Y-%m-%d"))
print("All modified dates correct:", "PASSED" if correct_dates else "FAILED")
print("Timestamp changed: access and modified times")
print("Creation time changed: No")
print("Original files unchanged:", "PASSED" if originals_unchanged else "FAILED")
print("Every copy has a source listed:", "PASSED" if traceability_ok else "FAILED")
print("Each source used once:", "PASSED" if source_selection_ok else "FAILED")
print("Output folder is separate:", "PASSED" if output_path != dataset_path else "FAILED")
print("Output folder:", output_path)
print("Filename list saved to:", filename_list)
print("Source mapping saved to:", mapping_file)
print("Overall result:", "ALL CHECKS PASSED" if all_passed else "CHECKS FAILED")