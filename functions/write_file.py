import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
  name="write_file",
  description="Writes to a file with the content. If the file does not already exist, creates the file from its file_path and content. Constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    required=['file_path', 'content'],
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The file path to list the contents of, relative to the working directory. If the path is not a regular file, returns an error."
      ),
      "content": types.Schema(
        type=types.Type.STRING,
        description="The content to be written to the file."
      )
    },
  )
)

def write_file(working_directory: str, file_path: str, content: str):
  full_file_path = os.path.join(working_directory, file_path)
  abs_directory_path = os.path.abspath(working_directory)
  abs_full_path = os.path.abspath(full_file_path)
  
  if not abs_full_path.startswith(abs_directory_path):
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
  
  try:
    os.makedirs(os.path.dirname(abs_full_path), exist_ok=True)
    
    with open(abs_full_path, 'w') as file:
      chars_written = file.write(content)
      
    return f'Successfully wrote to "{file_path}" ({chars_written} characters written)'
  except Exception as e:
    return f'Error: Failed to write to "{file_path}": {str(e)}'