# Project README

## Overview

This project uses Ollama for running machine learning models locally, making it efficient and easy to manage on your own machine. Additionally, you can easily set up the required Python environment using a provided Conda environment YAML file.

You should use Python 3.10.15.
if you can't use the yml file to create the conda evnironment use the requirements.txt

### Prerequisites

- Conda (Anaconda or Miniconda) installed on your machine.
- Ollama installed to run LLMs locally.

## Setting Up the Project

### Step 1: Clone the Repository

First, clone this repository to your local machine:

```sh
git clone <repository-url>
cd <repository-name>
```

### Step 2: Set Up the Conda Environment

This project provides a Conda environment XML file that makes it easy to create the necessary Python environment with all dependencies.

1. **Create the Conda Environment:**

   Run the following command to create a new Conda environment using the provided XML file (`environment.yml`):

   ```sh
   conda env create -f environment.yml
   ```

2. **Activate the Environment:**

   Once the environment is successfully created, activate it:

   ```sh
   conda activate <env_name>
   ```

   Replace `<env_name>` with the name of the environment specified in the XML file.

3. **Verify Installation:**

   Make sure that all necessary packages are installed:

   ```sh
   conda list
   ```

### Step 3: Install and Configure Ollama

Ollama is used to run machine learning models locally. Follow these steps to install and configure Ollama:

1. **Install Ollama:**

   You can download and install Ollama from its official website: [Ollama Installation](https://ollama.com/download).

2. **Configure Ollama:**

   Once Ollama is installed, verify it is running correctly:

   ```sh
   ollama list
   ```

   This command will list the available models installed locally.

3. **Load the Required Model:**



   If you need a specific model (e.g., llama3\:latest), you can pull it by running:

   ```sh
   ollama pull llama3:latest
   ```

### Step 4: Running the Project

Now that the environment is set up and Ollama is configured, you can run the project.

Use the following command to start the project:

```sh
python app_socketio.py
```

Replace `app_socketio.py` with the name of the main Python script for your project.

## Additional Information

- **Updating the Conda Environment:** If you need to update the environment, modify `environment.yml` and run:

  ```sh
  conda env update -f environment.yml
  ```

- **Deactivating the Conda Environment:** To deactivate the Conda environment, use:

  ```sh
  conda deactivate
  ```

## Additional Note

We are also planning to use the Hugging Face Inference Client API for this project, but it is not implemented yet.

## Conclusion

This setup allows you to easily manage your environment using Conda and run models locally using Ollama, ensuring reproducibility and easy collaboration.


