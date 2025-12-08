import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_directory = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    try:
        items = os.listdir(full_path)
        files_info = ""
        for item in items:
            item_path = os.path.join(full_path, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path) 
            files_info += f"{item}: file_size={size} bytes, is_dir={is_dir}\n"
        return files_info
    except Exception as e:
        return f'Error accessing directory "{directory}": {str(e)}'

