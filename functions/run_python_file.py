import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ["python", abs_file_path] + args,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30
        )

        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        
        if result.stdout.strip() == "" and result.stderr.strip() == "":
            return "No output produced"
        
        return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'
    except Exception as e:
        return f'Error executing file "{file_path}": {str(e)}'