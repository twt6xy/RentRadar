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

    To ensure code quality and consistency, this project uses pre-commit hooks with tools like `black`, `isort`, `ruff`, and `pytest` for automatic code formatting and quality checks. First, install the pre-commit hooks defined in the `.pre-commit-config.yaml` file by running the following command within the project's root directory:

    ```bash
    poetry run pre-commit install
    ```

    Here's what each hook does:

    - **`black`**: This hook automatically formats Python code to adhere to a consistent style, making it readable and maintainable according to the Black code style guide.

    - **`isort`**: This hook ensures that all Python import statements follow a consistent format by sorting imports alphabetically and automatically separates them into sections.

    - **`ruff`**: Provides fast linting for Python code, catching syntax errors and stylistic issues based on common Python coding standards. Unlike `black`, which formats code, `ruff` focuses on identifying and reporting issues without automatically fixing them.

    - **`pytest`**: Runs your project's test suite with Pytest, ensuring that all tests pass before a commit is finalized. This hook helps catch and prevent errors in code functionality. Any files prefixed with `test_`, and any functions within those files prefixed with `test_` in the `tests` directory will be run.

    <br>
    After installing the hooks, they will run automatically on files staged for commit. If any hook reports errors, the commit will be blocked until the issues are resolved. It's also important to keep your pre-commit hooks up to date. You can update the hooks to their latest versions with the following command:

    ```bash
    poetry run pre-commit autoupdate
    ```
