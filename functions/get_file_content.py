import os
from helpers.config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str):
  try:
    full_file_path = os.path.join(working_directory, file_path)
    abs_directory_path = os.path.abspath(working_directory)
    abs_full_file_path = os.path.abspath(full_file_path)
    
    if not abs_full_file_path.startswith(abs_directory_path):
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
      
    if not os.path.isfile(abs_full_file_path):
      return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(full_file_path, 'r') as file:
      file_contents = file.read()
      
      if len(file_contents) > MAX_CHARS:
        file_contents = file_contents[:MAX_CHARS]
        file_contents += f'[...File "{file_path}" truncated at 10000 characters]'
    
    return file_contents
  except Exception as e:
    return f'Error: An error occurred when reading "{file_path}" contents: {e}'