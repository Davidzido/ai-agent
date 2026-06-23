import os
from google.genai import types

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file contents from specified directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read file contents from, relative to the working directory",
            )
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file_path: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
            
        if not os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS_TO_READ = 10000

        with open(target_file_path, "r") as file:
            content = file.read(MAX_CHARS_TO_READ)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS_TO_READ} characters]'
            return content

    except Exception as e:
        return f"Error: {e}"