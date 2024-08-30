import re
import os
import time
import streamlit as st
import base64
from implementation.helper_functions.rag import process_c_files, generate_c_function, generate_c_variable, generate_c_typedef
from implementation.helper_functions.removed_unused_or_duplicated import find_and_remove_duplicates
from implementation.helper_functions.find_missing import find_missing

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

def fix_c_code(file_path, include_directories):
    """
    Detects missing functions, variables, and typedefs in a C source file and uses ChatGPT to generate and integrate them into the source code.
    """
    source_code = read_file(file_path)
    if not source_code:
        return None

    include_files = extract_includes(source_code)

    header_files = []
    for include_file in include_files:
        for directory in include_directories:
            potential_path = os.path.join(directory, include_file)
            if os.path.isfile(potential_path):
                header_files.append(potential_path)
                break

    header_files.extend(scan_directory_for_headers('.'))

    # Read all header file contents
    header_contents = ""
    for header_file in header_files:
        header_contents += read_file(header_file) + "\n"

    # Append header contents to the source code
    source_code += "\n" + header_contents

    missing_functions, missing_variables, missing_typedefs = find_missing()
    if not missing_functions and not missing_variables and not missing_typedefs:
#        log_to_file(f"Iteration {st.session_state.iteration}: No missing functions, variables, or typedefs detected.")
        print("nothing missing")

#    log_to_file(f"Iteration {st.session_state.iteration}: Found {len(missing_functions)} missing functions, {len(missing_variables)} missing variables, and {len(missing_typedefs)} missing typedefs.")

    # Generate and insert code for each unique missing function
    processed_functions = set()
    for index, (func_name, params) in enumerate(missing_functions):
        if func_name not in processed_functions:
            log_to_file(f"Generating function: {func_name} with parameters {params}")
            print(f"Generating code for function {index + 1}/{len(missing_functions)}: {func_name}")
#            st.session_state.api_requests += 1
            func_code = generate_c_function(func_name, params)
            file_path = r"implementation\input\src\microcontroller_hal.h"
            insert_generated_code(func_code, file_path)
            processed_functions.add(func_name)

    # Generate and insert code for each unique missing variable
    processed_variables = set()
    for index, var_name in enumerate(missing_variables):
        if var_name not in processed_variables:
            log_to_file(f"Generating variable: {var_name}")
            print(f"Generating code for variable {index + 1}/{len(missing_variables)}: {var_name}")
#            st.session_state.api_requests += 1
            var_code = generate_c_variable(var_name)
            file_path = r"implementation\input\src\variables.h"
            insert_generated_code(var_code, file_path)
            processed_variables.add(var_name)

    # Generate and insert code for each unique missing typedef
    processed_typedefs = set()
    for index, typedef_name in enumerate(missing_typedefs):
        if typedef_name not in processed_typedefs:
            log_to_file(f"Generating typedef: {typedef_name}")
            print(f"Generating code for typedef {index + 1}/{len(missing_typedefs)}: {typedef_name}")
#            st.session_state.api_requests += 1
            typedef_code = generate_c_typedef(typedef_name)
            file_path = r"implementation\input\src\typedefs.h"
            insert_generated_code(typedef_code, file_path)
            processed_typedefs.add(typedef_name)

    return len(missing_functions) + len(missing_variables) + len(missing_typedefs)

def insert_generated_code(func_code, file_path):
    """
    Inserts the generated function code into the appropriate header file.
    """
    cleaned_code = re.sub(r'```c?', '', func_code)
    with open(file_path, 'a') as file:
        file.write(f"\n{cleaned_code}\n")
    log_to_file(f"Inserted code into {file_path}")

def read_c_code(file_path):
    """
    Reads and returns the content and line count of a C code file.
    """
    with open(file_path, 'r') as file:
        code = file.read()
    return code, len(code.splitlines())

# Define a CSS style for the code block
code_block_style = """
<style>
    .code-block {{
        font-family: Monaco, 'Courier New', monospace;
        background-color: #272822;
        color: #f8f8f2;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
        height: 200px;  /* Fixed height */
        overflow: auto; /* Enable scrolling */
        width: 100%;
        font-size: 16px;
        line-height: 1.5;
        white-space: pre-wrap;  /* Maintains whitespace formatting */
    }}

    .code-line-count {{
        font-size: 10px;
        color: #999;
    }}
</style>
"""

# Function to convert image file to base64
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"

def display_logs():
    """Utility function to display logs from the generation log file."""
    with open('output/generation_log.txt', 'r') as log_file:
        log_data = log_file.read()
    return log_data

def generation_cycle():
    if 'iteration' not in st.session_state:
        st.session_state.iteration = 0
        st.session_state.api_requests = 0
        st.session_state.total_time = 0.0

    # Button to start the generation cycle
    button1 = st.button("Generate")

    # Create placeholders for iteration count, API request count, and total time
    iteration_placeholder = st.empty()
    api_request_placeholder = st.empty()
    timer_placeholder = st.empty()

    if 'file_placeholders' not in st.session_state:
        st.session_state.file_placeholders = {
            "main.c": (st.empty(), st.empty(), st.empty()),
            "variables.h": (st.empty(), st.empty(), st.empty()),
            "microcontroller_hal.h": (st.empty(), st.empty(), st.empty()),
            "typedefs.h": (st.empty(), st.empty(), st.empty())
        }

    # Display the CSS style
    st.markdown(code_block_style, unsafe_allow_html=True)

    if button1 or st.session_state.iteration > 0:
        # Start the timer for the iteration
        start_time = time.time()
        while st.session_state.iteration < 15:
            process_c_files(r"implementation\input\src")

            # Example usage
            source_code_path = r'implementation\input\src\main.c'
            include_directories = [r'\implementation\input\include']

            fixed_code = fix_c_code(source_code_path, include_directories)

            st.session_state.iteration += 1
            print(f"######################Iteration {st.session_state.iteration}####################################")

            if not fixed_code:
                # Final update for the placeholders
                iteration_placeholder.markdown(f"**Iteration count: {st.session_state.iteration}**")
                api_request_placeholder.markdown(f"**API Requests: {st.session_state.api_requests}**")
                timer_placeholder.markdown(f"**Total Time: {st.session_state.total_time:.2f} seconds**")
                break

            find_and_remove_duplicates(include_directories)

            # Calculate and update the elapsed time for the iteration
            elapsed_time = time.time() - start_time
            st.session_state.total_time += elapsed_time

            # Final update for the placeholders
            iteration_placeholder.markdown(f"**Iteration count: {st.session_state.iteration}**")
            api_request_placeholder.markdown(f"**API Requests: {st.session_state.api_requests}**")
            timer_placeholder.markdown(f"**Total Time: {st.session_state.total_time:.2f} seconds**")

            st.rerun()

        st.session_state.iteration = 0
    # Log display section
    log_data = display_logs()
    st.text_area("Log Output", log_data, height=300)
# generation_cycle()
