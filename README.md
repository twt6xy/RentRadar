## Setup

### Prerequisites

Before setting up the project, ensure you have Poetry installed. If you do not have Poetry installed, follow the installation instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

### Development Environment

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
    After installing the hooks, they will run automatically on files staged for commit. If any hook reports errors, the commit will be blocked until the issues are resolved. Run the following command to verify the hooks have been installed correctly.

    ```bash
    poetry run pre-commit run
    ```

### Environment Variables

This project requires certain environment variables to be set for its proper operation. Specifically, you will need an API access key from RentCast to access rental market data.

1. Visit [RentCast](https://www.rentcast.io/) and sign up for an account or log in if you already have one.
2. Navigate to the API section and follow the instructions to obtain your API access key.
3. In the root directory, create a file named `.env`.
4. Open the `.env` file in a text editor and add the following line:

    ```
    RENTCAST_API_KEY=<your_api_key>
    ```

   Replace `your_api_key` with the actual API key you obtained from RentCast.
