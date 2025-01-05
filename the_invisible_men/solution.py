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

def main():
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
        
if __name__ == "__main__":
    main()