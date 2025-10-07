import subprocess
import sys

def run_notebook(notebook_path):
    try:
        result = subprocess.run(
            [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", 
             "--output", "executed_output.ipynb", notebook_path],
            capture_output=True,
            text=True,
            check=True
        )
        print("Notebook executed successfully!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing notebook: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

if __name__ == "__main__":
    notebook_path = "tutorial/fixed_tutorial.ipynb"
    success = run_notebook(notebook_path)
    if success:
        print(f"Successfully executed {notebook_path}")
    else:
        print(f"Failed to execute {notebook_path}")
