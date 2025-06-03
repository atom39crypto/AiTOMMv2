import os
import re

from Mainframe.reader import read_text_from_file  # Ensure this import is correct and the module exists
from Mainframe.uploder import uploder  # Ensure this import is correct and the module exists

def extract_file_path_and_rest(text):
    pattern = (
        r'(?P<win_path>(?P<drive>[a-zA-Z]:)[\\/](?:[^\\/:*?"<>|\r\n]+[\\/])*[^\\/:*?"<>|\r\n]+\.\w+)'  # Windows
        r'|(?P<unix>/[^ \r\n\t]+(?:\.\w+)?)'  # Unix
    )

    match = re.search(pattern, text)

    if match:
        drive = match.group('drive') or ''

        if match.group('unix'):
            file_path = match.group('unix')
        else:
            file_path = match.group('win_path')

        # Remove matched path from text
        rest = text[:match.start()] + text[match.end():]

        # Strip any leftover drive letter if still floating
        if drive:
            rest = rest.replace(drive, '')

        return file_path, rest.strip()

    return None, text.strip()

def is_file_path(input_str):
    # Check if the input is a string and not empty
    if not isinstance(input_str, str) or not input_str.strip():
        return False
    
    # Check if the path exists and is a file (not a directory)
    return os.path.isfile(input_str)

def file_content(prompt):
    print('<=-------------------Read File----------------------=>')

    path, rest = extract_file_path_and_rest(prompt)
    if is_file_path(path):  # Check if the extracted path is valid
        text = read_text_from_file(path)
        prompt = path[-10] + " file Content: " + text + " User prompt: " + rest
        return prompt

    # print(prompt)
    return prompt

if __name__ == "__main__":
    print(file_content("C:/Users/offic/Downloads/ProjectReportDraft1.docx  what is this !!!!!!!"))
