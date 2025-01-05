# The Invisible Man Challenge

## Overview

The **"Invisible Man"** challenge tests participants' skills in navigating files with non-printable (invisible) characters in their names and decoding encoded content. Participants will be tasked with extracting a ZIP file, locating a specific hidden file, decoding its contents, and determining the total number of characters in the decoded content to find the flag.

## Challenge Description

Participants will be provided with a ZIP file that contains multiple files and directories. Your task is to locate target file whose name is provided in the question, decode its Base64-encoded content, and find the flag hidden within the decoded text. The flag is structured as `ENIGMA{RandomValue_COUNT}`, where:
- `RandomValue` is the value extracted from the decoded content.
- `COUNT` is the total number of characters in the decoded content.

### Process Overview

1. **Extract the ZIP File**: Unzip the provided file to a directory.
2. **Locate the Target File**: The target file's name will be provided in the challenge. It will contain invisible characters, so use file browsing tools or scripts to locate it.
3. **Decode the File Content**: The content of the target file will be Base64 encoded. Decode the content.
4. **Search for the Flag**: In the decoded content, find the hidden flag in the format `ENIGMA{RandomValue}`.
5. **Count the Decoded Content**: Determine the total number of characters in the decoded content (including invisible characters).
6. **Submit the Flag**: The final flag is in the format `ENIGMA{RandomValue_COUNT}`, where `COUNT` is the length of the decoded content.

## Example Code

Below is an example Python script that demonstrates how to extract the ZIP file, locate the file with invisible characters, decode its Base64 content, and find the flag.

```python
import base64
import shutil
from zipfile import ZipFile
from os import makedirs, walk
from os.path import abspath, dirname, splitext, basename, join, exists

def extract_zip_file(zip_path):
    """
    Extracts the contents of a ZIP file to a specified directory.

    Parameters:
        zip_path (str): Path to the ZIP file.

    Returns:
        str: The path to the extracted folder.
    """
    try:
        # Define the directory location and target folder for extraction
        directory_location = abspath(dirname(zip_path))
        folder_name = splitext(basename(zip_path))[0]
        extract_to = join(directory_location, folder_name)
        
        # Create the target directory if it doesn't exist
        makedirs(extract_to, exist_ok=True)

        # Extract the ZIP file contents
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)

        return extract_to

    except Exception as e:
        print(f"Error extracting ZIP file: {e}")
        return None

def find_flag(folder, target_filename):
    """
    Searches for the flag in a file within the extracted folder. The flag is hidden in Base64 and follows the format ENIGMA{RandomValue_COUNT}.
    
    Parameters:
        folder (str): Path to the folder containing extracted files.
        target_filename (str): The name of the target file to search for.
    
    Returns:
        str: The final flag if found, else an error message.
    """
    try:
        # Search for the target file in the directory and its subdirectories
        for root, _, files in walk(folder):
            if target_filename in files:
                file_location = join(root, target_filename)
                
                # Read the file content and decode it from Base64
                with open(file_location, "r", encoding="utf-8") as file:
                    content = file.read()
                    print("File Content: ", content)
                    
                    # Decode the Base64 encoded content
                    base64_decoded = base64.b64decode(content).decode("utf-8")
                    print("Decoded File Content: ", base64_decoded)

                    # Extract the flag and calculate the length of decoded content
                    if "ENIGMA{" in base64_decoded:
                        flag = base64_decoded.split("ENIGMA{")[1].split("}")[0]
                        final_flag = f"ENIGMA{{{flag}_{len(base64_decoded)}}}"
                        print("Flag:", final_flag)
                        return final_flag

                    # If flag pattern is not found
                    print("Flag not found in the decoded content.")
                    return "Flag not found."

    except Exception as e:
        print(f"Error while searching for the flag: {e}")
        return "An error occurred during flag extraction."

    finally:
        # Clean up the extracted folder after processing
        if exists(folder):
            shutil.rmtree(folder)

# Example usage
zip_path = "TheInvisibleMen_123.zip"
target_filename = "\ufeff"  # Target file name with invisible characters

# Extract the ZIP file
folder_path = extract_zip_file(zip_path)

if folder_path:
    # Get the flag if the folder was successfully extracted
    find_flag(folder_path, target_filename)
else:
    print("Failed to extract the ZIP file.")
```

## Instructions

1. **Download the ZIP File**: Download the provided ZIP file from the challenge page.
2. **Extract the ZIP File**: Extract the contents of the ZIP file to a local folder.
3. **Locate the Target File**: The file with the invisible characters in its name will be specified in the challenge. Use your coding skills or tools to identify it.
4. **Decode the File**: Once located, decode the file content from Base64 to reveal the hidden message.
5. **Submit the Flag**: Once you've decoded the content and found the flag, submit it in the format `ENIGMA{RandomValue_COUNT}`, where `RandomValue` is the decoded flag and `COUNT` is the length of the decoded content.

## Conclusion

The **"Invisible Man"** challenge is a great way to test your skills in file manipulation, Base64 decoding, and handling non-printable characters in file names. By combining file extraction, character handling, and decoding techniques, participants will gain valuable experience in navigating complex file systems and encoding formats.

Good luck, and happy decoding!
