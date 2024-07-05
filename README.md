# Python Dependencies Collector

A Python script to collect and aggregate dependencies from multiple GitLab repositories.

## Features

- Collects dependencies from `requirements.txt` files across multiple repositories.
- Checks `main`, `master`, and `dev` branches.
- Saves dependencies to `all_dependencies.txt` and `all_dependencies_clean.txt`.

## Installation

```bash
git clone https://github.com/Sergey360/python-dependencies-collector.git

cd python-dependencies-collector

python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt
```

## Usage

Update the GITLAB_URL and PRIVATE_TOKEN in the script with your GitLab instance URL and personal access token.

Run the script:

```bash
python python-dependencies-collector.py
```

## Output

The script generates two files:

- `all_dependencies.txt` : Sorted list of all dependencies with versions.
- `all_dependencies_clean.txt` : Sorted list of all dependencies without versions and duplicates.

## License

This project is licensed under the MIT License.
