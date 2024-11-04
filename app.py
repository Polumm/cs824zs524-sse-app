import requests
from flask import Flask, jsonify, render_template, request
import random
import os

from utils import are_opposite_directions


query_dict = {
    "dinosaurs": "Dinosaurs ruled the Earth 200 million years ago",
    "asteroids": "Asteroids are rocky bodies orbiting the Sun",
}

app = Flask(__name__)

# Snake game state management
game_state = {
    "snake": [(100, 100), (90, 100), (80, 100)],
    "direction": "Right",
    "food": [random.randint(0, 39) * 10, random.randint(0, 39) * 10],
    "score": 0,
    "game_over": False,
}


def move_snake():
    head = list(game_state["snake"][0])
    if game_state["direction"] == "Up":
        head[1] -= 10
    elif game_state["direction"] == "Down":
        head[1] += 10
    elif game_state["direction"] == "Left":
        head[0] -= 10
    elif game_state["direction"] == "Right":
        head[0] += 10
    game_state["snake"] = [tuple(head)] + game_state["snake"][:-1]


def check_collisions():
    head = game_state["snake"][0]
    # Boundary collision
    if head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
        game_state["game_over"] = True
    # Self-collision
    if head in game_state["snake"][1:]:
        game_state["game_over"] = True


def check_food():
    if game_state["snake"][0] == tuple(game_state["food"]):
        game_state["snake"].append(game_state["snake"][-1])
        game_state["food"] = [
            random.randint(0, 39) * 10,
            random.randint(0, 39) * 10,
        ]
        game_state["score"] += 10


@app.route("/game-state", methods=["GET"])
def get_game_state():
    return jsonify(game_state)


@app.route("/move", methods=["POST"])
def move():
    if game_state["game_over"]:
        return jsonify(game_state)  # Don't allow moves when the game is over

    data = request.json
    direction = data.get("direction", game_state["direction"])
    if not are_opposite_directions(direction, game_state["direction"]):
        game_state["direction"] = direction
    move_snake()
    check_collisions()
    check_food()
    return jsonify(game_state)


@app.route("/reset", methods=["POST"])
def reset_game():
    game_state["snake"] = [(100, 100), (90, 100), (80, 100)]
    game_state["direction"] = "Right"
    game_state["food"] = [
        random.randint(0, 39) * 10,
        random.randint(0, 39) * 10,
    ]
    game_state["score"] = 0
    game_state["game_over"] = False
    return jsonify(game_state)


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


def process_query(query: str):
    if query.startswith("What") or query.startswith("Which"):
        if "name" in query:
            return "cszs"
        if "largest" in query:
            numbers = [int(i) for i in query.split(": ")[1][:-1].split(", ")]
            return str(max(numbers))
        if "plus" in query:
            numbers = query.split()
            if len(numbers) == 5:
                return str(int(numbers[2]) + int(numbers[-1][:-1]))
            else:
                return str(
                    int(numbers[2]) + int(numbers[4]) + int(numbers[-1][:-1])
                )
        if "minus" in query:
            numbers = query.split()
            return str(int(numbers[2]) - int(numbers[-1][:-1]))
        if "multiplied" in query:
            numbers = query.split()
            return str(int(numbers[2]) * int(numbers[-1][:-1]))
        if "square" in query:
            numbers = [int(i) for i in query.split(": ")[1][:-1].split(", ")]
            s_c = []
            for number in numbers:
                if is_square_and_cube(number):
                    s_c.append(str(number))
            return ", ".join(s_c)
        if "prime" in query:
            numbers = [int(i) for i in query.split(": ")[1][:-1].split(", ")]
            primes = []
            for number in numbers:
                if is_prime(number):
                    primes.append(str(number))
            return ", ".join(primes)
        if "power" in query:
            numbers = query.split()
            return str(int(numbers[2]) ** int(numbers[-1][:-1]))
        else:
            return "Unknown"
    else:
        return query_dict.get(query, "Unknown")


def is_square_and_cube(a: int):
    return round(a**0.5) ** 2 == a and round(a ** (1 / 3)) ** 3 == a


def is_prime(a: int):
    if a < 2:
        return False
    if a == 2:
        return True
    for i in range(2, a):
        if a % i == 0:
            return False
    return True


@app.route("/query")
def query_route():
    query_param = request.args.get("q")
    if query_param:
        return process_query(query_param)
    else:
        return "Query parameter missing", 400


@app.route("/github_actions")
def actions():
    return render_template("actions.html")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/repos", methods=["POST"])
def repos():
    username = request.form["username"]
    url = f"https://api.github.com/users/{username}/repos"

    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        repo_data = []

        for repo in repos:
            # Fetch latest commit information
            commits_url = repo["commits_url"].replace("{/sha}", "/main")
            commit_response = requests.get(commits_url, headers=headers)
            latest_commit = (
                commit_response.json()
                if commit_response.status_code == 200
                else None
            )

            # Fetch open issues information
            issues_url = "https://api.github.com/repos/"
            f"{username}/{repo['name']}/issues"
            issues_response = requests.get(issues_url, headers=headers)
            issues = (
                issues_response.json()
                if issues_response.status_code == 200
                else []
            )

            # Limit to the 5 most recent issues
            recent_issues = [
                {
                    "title": issue["title"],
                    "created_at": issue["created_at"],
                    "html_url": issue["html_url"],
                }
                for issue in issues[:5]
            ]

            repo_data.append(
                {
                    "name": repo["full_name"],
                    "html_url": repo["html_url"],
                    "updated_at": repo["updated_at"],
                    "stars": repo["stargazers_count"],
                    "latest_commit": latest_commit,
                    "recent_issues": recent_issues,
                }
            )

        return render_template(
            "repos.html", repos=repo_data, username=username
        )
    else:
        return f"Error fetching repositories: {response.status_code}"


if __name__ == "__main__":
    app.run(debug=True)
