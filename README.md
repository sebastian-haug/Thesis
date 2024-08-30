
# CodeGeneration

## Installation

To install all required libraries, run the following command:

```bash
pip install -r requirements.txt
```

## Configuration

Before running the project, ensure you have set up your environment variables:

- **OpenAI API Key:**

  - Add your OpenAI API key to the `.env` file as follows:
    ```
    OPENAI_API_KEY=your-api-key-here
    ```

## Getting Started

### Initial Testing

To begin exploring the project, follow these steps:

- **Test Vectorstore with PDF and Retrieval-Augmented Generation:**
  ```bash
  streamlit run interface_2.py
  ```

- **View Results from the Last Test Run:**
  ```bash
  python show_plots_3_1.py
  ```
  or
  ```bash
  python show_plots_3_2.py
  ```

### Compiler Methods

To utilize the compiler methods, follow these steps:

1. **Configure the Compiler Path:**
   - Open the settings file located at `/.vscode/settings.json`.
   - Update the `compilerPath` to point to your `gcc.exe` compiler.

2. **Run and Update Tests:**
   - To execute the tests and update the results, run:
     ```bash
     python test_3_1.py
     ```
     or
     ```bash
     python test_3_2.py
     ```

   - You can view the updated results with the `show_plots` scripts mentioned above.

3. **Use Compiler Method via Interface:**
   - To use the compiler method through the interface, run:
     ```bash
     streamlit run interface_3.py
     ```

## Project Structure

- **Reference Application Layer:**  
  Located in `implementation/dummy_ide/main.c`.

- **Input Code for Interface 3:**  
  Found in the `implementation/input/` folder, containing the code utilized by the `interface_3` application.
