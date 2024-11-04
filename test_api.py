import requests


username = "Polumm"
url = f"https://api.github.com/users/{username}/repos"


response = requests.get(url)


if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        print(f"Repository: {repo['full_name']}, Updated at: {repo['updated_at']}")
else:
    print("Failed to retrieve data")
