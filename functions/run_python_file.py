import os
import subprocess
import sys
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
  name="run_python_file",
  description="Runs a Python file by its file path, along with optional arguments, constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    required=['file_path'],
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The file path to list the contents of, relative to the working directory. If the path is not a regular file, returns an error."
      ),
      "args": types.Schema(
        type=types.Type.ARRAY,
        description="Optional CLI args (default: none).",
        items=types.Schema(type=types.Type.STRING)
      )
    }
  )
)

def run_python_file(working_directory: str, file_path: str, args=['-v']):
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
    process_result = subprocess.run(
        command,
        timeout=30_000,
        cwd=working_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout = process_result.stdout or ''
    stderr = process_result.stderr or ''
    
    response = ''
    if process_result.returncode != 0:
      response = f'Process exited with code {process_result.returncode}\n'
      
    if not stdout.strip() and not stderr.strip():
      return 'No output produced'
      
    return f'STDOUT: {stdout}\nSTDERR: {stderr}\n{response}'
  except Exception as e:
    return f"Error: executing Python file: {e}"