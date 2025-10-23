import os
import subprocess
import sys


def run_python_file(working_directory: str, file_path: str, args=[]):
  try:
    full_file_path = os.path.join(working_directory, file_path)
    abs_directory_path = os.path.abspath(working_directory)
    abs_full_file_path = os.path.abspath(full_file_path)
    
    if not abs_full_file_path.startswith(abs_directory_path):
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_full_file_path):
      return f'Error: File "{file_path}" not found.'
      
    if not file_path.endswith('.py'):
      return f'Error: "{file_path}" is not a Python file.'
      
    command = [sys.executable, abs_full_file_path, *args]
    process_result = subprocess.run(command, timeout=30_000, capture_output=True)
    
    stdout = process_result.stdout
    stderr = process_result.stderr
    
    response = ''
    
    
    if not stdout:
      return 'No output produced'
    else:
      if process_result.returncode != 0:
        response = f'Process exited with code {process_result.returncode}\n'
      return f'STDOUT: {stdout}\nSTDERR: {stderr}\n{response}'
  except Exception as e:
    return f"Error: executing Python file: {e}"