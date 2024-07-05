import gitlab


# Enter your personal access token and GitLab URL
GITLAB_URL = "https://gitlab.example.com"
PRIVATE_TOKEN = "your_private_token"


# Initialize GitLab connection
gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)


def get_all_projects():
    """Retrieve all projects from GitLab"""
    return gl.projects.list(all=True)


def get_requirements(project, branch):
    """Retrieve requirements.txt file from the project"""
    try:
        file = project.files.get(file_path="requirements.txt", ref=branch)
        print(f"File found in project {project.name} in branch {branch}")
        return file.decode().splitlines()
    except gitlab.exceptions.GitlabGetError as e:
        print(
            f"requirements.txt not found in project {project.name} in branch {branch}. Error: {e}"
        )
        return []


def collect_dependencies(projects):
    """Collect all dependencies from all projects"""
    all_dependencies = set()
    preferred_branches = ["main", "master", "dev"]

    for project in projects:
        requirements = []

        # Check preferred branches
        for branch in preferred_branches:
            requirements = get_requirements(project, branch)
            if requirements:
                break

        # If not found in preferred branches, check all other branches
        if not requirements:
            branches = project.branches.list()
            for branch in branches:
                if branch.name not in preferred_branches:
                    requirements = get_requirements(project, branch.name)
                    if requirements:
                        break

        # Update the set of all dependencies
        if requirements:
            all_dependencies.update(requirements)

    return all_dependencies


def clean_req(req):
    if isinstance(req, bytes):
        # Decode the byte string to a string with 'utf-8' encoding
        return req.decode("utf-8")
    else:
        # If it is already a string, return it unchanged
        return req


def save_dependencies_all(dependencies, filename):
    """Save dependencies to a file"""
    sorted_dependencies = sorted(clean_req(dep) for dep in dependencies)
    with open(filename, "w") as f:
        for dep in sorted_dependencies:
            f.write(f"{dep}\n")
    print(f"List of all dependencies saved to {filename}")


def save_dependencies_clean(dependencies, filename):
    """Save cleaned list of dependencies to a file"""
    dependencies_clean = {clean_req(dep).split("==")[0] for dep in dependencies}
    sorted_dependencies = sorted(dependencies_clean)
    with open(filename, "w") as f:
        for dep in sorted_dependencies:
            f.write(f"{dep}\n")
    print(f"Cleaned list of all dependencies saved to {filename}")


def main():
    projects = get_all_projects()
    dependencies = collect_dependencies(projects)
    save_dependencies_all(dependencies, "all_dependencies.txt")
    save_dependencies_clean(dependencies, "all_dependencies_clean.txt")


if __name__ == "__main__":
    main()
