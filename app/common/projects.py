from .configuration import GITHUB_TOKEN, GITHUB_USERNAME
import requests

API_URL = "https://api.github.com/repos/"


async def get_repository_data(repository: str):
    """Uses the configured github username and token to retrieve information about a repository.

    Args:
        repository (str): The name of the repository

    Raises:
        ValueError: Invalid repository
        ValueError: Data retrieval error

    Returns:
        list: A list containing the name, description, license, stars and forks in that order.
    """
    # I have almost no clue what is going on here, so I will avoid making an inline request statement
    repo_url = f"{API_URL}{GITHUB_USERNAME}/{repository}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 200:
        repository_info = response.json()
        name = repository_info["name"]
        description = repository_info["description"]
        license = (
            repository_info["license"]["name"] if repository_info["license"] else "N/A"
        )
        stargazers_count = repository_info["stargazers_count"]
        forks_count = repository_info["forks_count"]
        return [name, description, license, stargazers_count, forks_count]
    elif response.status_code == 404:
        raise ValueError(f"Repository '{GITHUB_USERNAME}/{repository}' does not exist.")
    else:
        raise ValueError("Failed to retrieve repository information.")


async def get_all_repositories():
    response = requests.get(
        f"https://api.github.com/users/{GITHUB_USERNAME}/repos",
        headers={"Authorization": f"token {GITHUB_TOKEN}"},
    )
    if response.status_code == 200:
        repositories = response.json()
        repos = [repo["name"] for repo in repositories]
        return repos
    else:
        raise ValueError("Failed to retrieve user repositories.")
