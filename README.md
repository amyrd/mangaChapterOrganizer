# Manga to CBZ Converter

## Overview

This script organizes manga downloaded from **HakuNeko** into chapter-based CBZ files, making them easier to read on eReaders.

### Motivation
The script was developed to solve the inconvenience of downloading individual chapters from **HakuNeko**. After reading each chapter, you would need to close it and manually open the next one—this became tedious. With this tool, you can group multiple chapters into a single **CBZ** file, allowing for continuous reading without interruptions.

## Features

- Automatically detects volume and chapter numbers in folder names.
- Groups chapters into user-defined sizes.
- Creates **.cbz** (Comic Book Zip) files, commonly used for reading on eReaders.
- Cleans up temporary files after zipping.

## How It Works

1. **Input Folder Path**: The script takes the path of the folder where the manga chapters are stored.
2. **Chapter Sorting**: It sorts chapters based on the volume and chapter numbers found in the folder names.
3. **Grouping**: Chapters are grouped into batches based on the user-defined number.
4. **File Creation**: The grouped chapters are compressed into a CBZ file, which can be loaded onto an eReader.

## How to Use

1. **Install Dependencies**: The script uses Python’s built-in libraries (e.g., `os`, `shutil`, `re`), so no additional packages are required.
   
2. **Run the Script**: 
    - Input the manga folder path.
    - Input the number of chapters per CBZ file.
   
3. **Example**:
    ```
    Enter manga filepath: /path/to/manga
    Enter the number of chapters per CBZ file: 5
    ```

4. The script will generate grouped CBZ files and clean up any temporary directories used during the process.

## Notes

- Ensure folder names contain "volume" and "chapter" for accurate sorting.
- Compatible image formats include `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, and `.tiff`.
- This tool saves time by allowing continuous reading of multiple chapters without manual intervention.

Enjoy reading manga on your eReader!
