import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file (specified by a file path) in a specified directory relative to the working directory and specified program arguments which are optional",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for the python file to run which is relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="List of string arguments passed by user when running the program"
            )
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try :
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file_path: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
            
        if not os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]

        if args is not None and len(args) > 0:
            command.extend(args)

        command_result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        output: str = ""

        if command_result.returncode != 0:
            output += f"Process exited with code {command_result.returncode}"
        
        if command_result.stdout == "" and command_result.stderr == "":
            output += "No output produced"
        else :
            output += f"STDOUT: {command_result.stdout}\nSTDERR: {command_result.stderr}"
        
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    