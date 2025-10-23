import os

def write_file(working_directory: str, file_path: str, content: str):
  abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
  
  full_file_path = os.path.join(working_directory, file_path)
  abs_directory_path = os.path.abspath(working_directory)
  abs_full_path = os.path.abspath(full_file_path)
  
  if not abs_full_path.startswith(abs_directory_path):
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.exists(abs_file_path):
    with open(abs_file_path, 'w') as file:
      new_file = file.write(content)
      if new_file:
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'