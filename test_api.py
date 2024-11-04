import requests


username = "Polumm"
url = f"https://api.github.com/users/{username}/repos"


response = requests.get(url)


if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        full_name = repo["full_name"]
        updated_at = repo["updated_at"]
        print(f"Repository: {full_name}, Updated at: {updated_at}")
else:
    print("Failed to retrieve data")
