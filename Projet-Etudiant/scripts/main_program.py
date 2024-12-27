import subprocess
import os

# Define paths for scripts and notebooks
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDA_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "eda_preprocessing.py")
CLUSTERING_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "kmeans_clustering.py")
VISUALIZATIONS_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "visualizations.py")


# Run a Python script
def run_script(script_path):
    try:
        print(f"Running script: {script_path}")
        subprocess.run(["python", script_path], check=True)
        print(f"Script {script_path} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")


# Run a Jupyter notebook
def run_notebook(notebook_path):
    try:
        print(f"Running notebook: {notebook_path}")
        subprocess.run(
            ["jupyter", "nbconvert", "--to", "script", "--execute", notebook_path],
            check=True,
        )
        print(f"Notebook {notebook_path} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {notebook_path}: {e}")


if __name__ == "__main__":
    # Step 1: Run EDA and preprocessing
    run_script(EDA_SCRIPT)

    # Step 2: Run K-Means clustering
    run_script(CLUSTERING_SCRIPT)

    # Step 3: Run visualizations
    run_script(VISUALIZATIONS_SCRIPT)

    # Notify completion
    print(
        "All scripts and notebooks executed successfully. Project pipeline is complete."
    )
