import os
import shutil
import math
from os.path import isdir
import re

def extract_volume_chapter(s):
    s = s.lower()
    volume = 0
    chapter = float('inf')
    volume_match = re.search(r'volume\s*([\d\.]+)', s)
    if volume_match:
        try:
            volume = float(volume_match.group(1))
        except ValueError:
            volume = 0  # Default to 0 if parsing fails
    # Find chapter number
    chapter_match = re.search(r'chapter\s*([\d\.]+[a-zA-Z]?)', s)
    if chapter_match:
        chapter_str = chapter_match.group(1)
        try:
            # Remove any trailing letters (e.g., '1a' becomes '1')
            chapter_float = float(re.match(r'([\d\.]+)', chapter_str).group(1))
            chapter = chapter_float
        except ValueError:
            chapter = float('inf')
    else:
        # If 'chapter' not found, try to find any numbers in the string
        numbers = re.findall(r'[\d\.]+', s)
        if numbers:
            try:
                chapter = float(numbers[-1])  # Take last num found
            except ValueError:
                chapter = float('inf')
        else:
            chapter = float('inf')  # If no number found, sort in the end
    return (volume, chapter)

def iterateThrough(filepath, group_size):
    imgNum = 0
    folder_name = os.path.basename(filepath.rstrip('/'))  # Get the folder name
    chapters = [d for d in os.listdir(filepath) if isdir(os.path.join(filepath, d))]
    
    chapters.sort(key=extract_volume_chapter)
    print(f"Sorted chapters: {chapters}")  # Debug line
    
    num_groups = math.ceil(len(chapters) / group_size)
    
    summary = []  # Initialize summary list

    for group in range(num_groups):
        tempDirectory = f"zipMe_group_{group + 1}"
        path = os.path.join(filepath, tempDirectory)
        os.makedirs(path, exist_ok=True)
        print(f"Directory {tempDirectory} created for group {group + 1}\n")  # Debug line
        
        start = group * group_size
        end = start + group_size
        group_chapters = chapters[start:end]
        
        if not group_chapters:
            print(f"No chapters to process in group {group + 1}.")  # Debug line
            continue

        # Get chapter numbers of first and last chapter in group
        start_volume, start_chapter = extract_volume_chapter(group_chapters[0])
        end_volume, end_chapter = extract_volume_chapter(group_chapters[-1])

        # Format the zip file name accordingly
        if start_volume == end_volume and start_volume != 0:
            zipFileName = f"{folder_name} Vol{int(start_volume)} Ch{start_chapter}-{end_chapter}.zip"
        else:
            zipFileName = f"{folder_name} Ch{start_chapter}-{end_chapter}.zip"

        zipFile = os.path.join(filepath, zipFileName)
        
        files_added = 0
        for chapter_name in group_chapters:
            tempChapterPath = os.path.join(filepath, chapter_name)
            print(f"Checking if {tempChapterPath} is a directory.")  # Debug line
            if isdir(tempChapterPath):
                print(f"{tempChapterPath} is a directory.")  # Debug line
                tempImages = os.listdir(tempChapterPath)
                tempImages.sort()
                for image in tempImages:
                    if image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                        tempImagePath = os.path.join(tempChapterPath, image)
                        dest = os.path.join(path, f"{imgNum}.jpg")
                        print(f"Copying {tempImagePath} to {dest}") # For debugging
                        shutil.copy2(tempImagePath, dest)
                        imgNum += 1
                        files_added += 1
                    else:
                        print(f"Skipping non-image file {image}")  # For debugging
                    else:
                print(f"{tempChapterPath} is not a directory, skipping")  # For debugging
                print(f"Done copying Chapter {chapter_name}'s images into the group {group + 1} folder\n")  # Debug line
        
        print(f"Zipping files in {path} to {zipFile}")  # Debug
        shutil.make_archive(path, 'zip', path)

        # Rename the .zip file to .cbz
        cbzFile = zipFile.replace('.zip', '.cbz')
        shutil.move(f"{path}.zip", cbzFile)
        print(f"Renamed {zipFile} to {cbzFile}")  # Debug..
        shutil.rmtree(path)
        print(f"Temporary directory {tempDirectory} cleaned up\n")  # Debug line

        # Add to summary
        summary.append({
            'cbz_file': os.path.basename(cbzFile),
            'chapters': group_chapters
        })

    # Print summary
    print("\nSummary of Processing:")
    for entry in summary:
        print(f"Created {entry['cbz_file']} with chapters:")
        for chapter in entry['chapters']:
            print(f" - {chapter}")
        print()  # Add an empty line for readability

# Get file path, strip leading and ending white spaces
filepath = input("Enter manga filepath: \n").strip()

# Replace escaped spaces with actual spaces
filepath = filepath.replace('\\ ', ' ').replace('\\\'', '\'')  # Fix escape characters
print(f"Processed file path: {filepath}")  # Debug line

group_size = int(input("Enter the number of chapters per CBZ file: \n").strip())

if os.path.isdir(filepath):
    iterateThrough(filepath, group_size)
else:
    print(f"Hey, the filepath isn't valid... you gave me this: {filepath}\n")
