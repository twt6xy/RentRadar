## Setup

### Prerequisites

Before setting up the project, ensure you have Poetry installed. If you do not have Poetry installed, follow the installation instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

### Installing the Project

1. **Clone the Repository**

    First, clone the project repository to your local machine using Git:

    ```bash
    git clone https://github.com/twt6xy/RentRadar.git
    cd RentRadar
    ```

2. **Install Dependencies**
    With Poetry installed, run the following command in the project root directory to install both production and development dependencies. This command reads the `pyproject.toml` file and installs the dependencies specified there, honoring the versions specified in the `poetry.lock` file:

    ```bash
    poetry install
    ```

3. **Activating the Environment**

    Poetry creates a virtual environment for your project to manage dependencies separately from your global Python installation. To activate this environment, use the command:

    ```bash
    poetry shell
    ```

4. **Setting Up Pre-commit Hooks**

    To ensure code quality and consistency, this project uses pre-commit hooks with tools like `black` for automatic code formatting. First, install the pre-commit hooks defined in the `.pre-commit-config.yaml` file by running the following command within the root directory:

    ```bash
    poetry run pre-commit install
    ```

    This command installs the pre-commit hooks into your Git hooks directory, enabling them to run automatically on `git commit`. To verify the installation, run the pre-commit hooks on all files. It should return `(no files to check) Skipped` for each of the hooks defined in the config.

    ```bash
    poetry run pre-commit run
    ```

    It's also important to keep your pre-commit hooks up to date. You can update the hooks to their latest versions with the following command:

    ```bash
    poetry run pre-commit autoupdate
    ```
