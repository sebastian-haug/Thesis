import re
import os
import time
import subprocess

import shutil

def concatenate_files(output_file):
    """Concatenate content from multiple files and write to the output file."""
    # Define the exact file paths
    file_paths = [
        'implementation/input/src/typedefs.h',
        'implementation/input/src/variables.h',
        'implementation/input/src/microcontroller_hal.h'
    ]
    
    # Store the concatenated content
    concatenated_content = ''
    
    for file_path in file_paths:
        with open(file_path, 'r') as infile:
            content = infile.read()
            # Remove all instances of #include <stdint.h> and #include "variables.h"
            content = content.replace('#include <stdint.h>', '')
            content = content.replace('#include "variables.h"', '')
            concatenated_content += content
            concatenated_content += '\n'  # Ensure each file's content is separated by a newline

    with open(output_file, 'w') as outfile:
        # Add a single #include <stdint.h> at the top
        outfile.write('#include <stdint.h>\n\n')
        # Write the concatenated content
        outfile.write(concatenated_content)

    return output_file

def log_to_file(message):
    """
    Writes a log message to the output/generation_log.txt file.
    """
    with open('output/generation_log.txt', 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def extract_includes(source_code):
    """
    Extracts the list of included header files from the C source code.
    """
    return re.findall(r'#include\s*[<"]([^>"]+)[>"]', source_code)

def read_file(file_path):
    """
    Reads the content of a file and returns it.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except (PermissionError, FileNotFoundError) as e:
        log_to_file(f"Error reading file {file_path}: {e}")
        return None

def scan_directory_for_headers(directory):
    """
    Scans a directory recursively for header files and returns their paths.
    """
    header_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.h'):
                header_files.append(os.path.join(root, file))
    return header_files

def insert_generated_code(func_code, file_path):
    """
    Inserts the generated function code into the appropriate header file.
    """
    cleaned_code = re.sub(r'```c?', '', func_code)
    with open(file_path, 'a') as file:
        file.write(f"\n{cleaned_code}\n")
    log_to_file(f"Inserted code into {file_path}")

def compile_code(file_path):
    """
    Compile the code using gcc.
    """
    compile_command = ['gcc', '-o', 'output/program', file_path]

    try:
        result = subprocess.run(compile_command, capture_output=True, text=True, check=True)
        print("Compilation successful.")
        return True
    except subprocess.CalledProcessError as e:
        print("Compilation failed:")
        print(e.stdout)
        print(e.stderr)
        return False

def clear_all_files():
    """
    Clears the content of all specified files and writes initial content to them.
    """
    open('output/generation_log.txt', 'w').close()
    file_paths = [
        "implementation/input/src/variables.h",
        "implementation/input/src/microcontroller_hal.h",
        "implementation/input/src/typedefs.h",
        "implementation/input/src/main.i",
        "implementation/dummy_ide/microcontroller_hal.h"
    ]

    initial_code = [
        "//variables \n#include <stdint.h>",
        '//microcontroller_h.h \n#include <stdint.h> \n#include "variables.h"',
        "//typedefs.h \n#include <stdint.h>",
        "", "#include <stdint.h>"
    ]

    for file_path, code in zip(file_paths, initial_code):
        with open(file_path, "w") as f:
            f.write(code)

    folder_path = "vector_stores"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print("All files in the 'vector_stores' folder have been deleted.")
    else:
        print(f"The folder '{folder_path}' does not exist.")