import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
  name="get_files_info",
  description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "directory": types.Schema(
        type=types.Type.STRING,
        description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
      )
    }
  )
)

def get_files_info(working_directory, directory='.'):
  try:
    full_path = os.path.join(working_directory, directory)
    
    abs_directory_path = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    
    result_message = ''
    if directory == '.':
      result_message = f'Result for current directory:'
    else:
      result_message = f"Result for '{directory}' directory:"
    
    if not abs_full_path.startswith(abs_directory_path):
      return f'{result_message}\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_full_path):
      return f'{result_message}\n    Error: "{directory}" is not a directory'
    
    contents = os.listdir(abs_full_path)
    formatted_message = ''
    
    for name in contents:
      abs_name_path = os.path.join(abs_full_path, name)
      formatted_message += f'\n - {name}: file_size={os.path.getsize(abs_name_path)} bytes, is_dir={os.path.isdir(abs_name_path)}'
      
    if directory == '.':
      return f'{result_message}{formatted_message}'
    else:
      return f'{result_message}{formatted_message}'
  except Exception as e:
    return f'Error: An error occurred when trying to get files info: {e}'