import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file specified by file path from directory relative to the working relative",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write contents to which is located relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents to write to the file",
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file_path: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
            
        if not os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        target_dir = os.path.dirname(target_file_path)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)

        with open(target_file_path, "w") as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
