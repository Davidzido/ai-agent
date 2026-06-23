import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        return format_dir_contents(get_dir_info(target_dir))
    
    except Exception as e:
         return f"Error: {e}"
    
def get_dir_info(target_dir: str) -> list[tuple[str, str, str]]:
    list_dir: list[tuple[str, str, str]] = []
    for dir in os.listdir(target_dir):
        filepath = os.path.join(target_dir, dir)
        file_size: int = os.path.getsize(filepath)
        is_dir: bool = os.path.isdir(filepath)
        list_dir.append((dir, file_size, is_dir))
    return list_dir

def format_dir_contents(list_dir: list[tuple[str, str, str]]) -> str:
    results: list[str] = []
    for dir in list_dir:
        results.append(f"- {dir[0]}: file_size={dir[1]} bytes, is_dir={dir[2]}")
    return "\n".join(results)
