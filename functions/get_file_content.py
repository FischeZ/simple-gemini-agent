import os
from config import MAX_FILE_CONTENT_LENGTH

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file_path, 'r') as file:
            content = file.read()

        if len(content) > MAX_FILE_CONTENT_LENGTH:
            content = content[:MAX_FILE_CONTENT_LENGTH]
            content += f'\n[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {str(e)}'