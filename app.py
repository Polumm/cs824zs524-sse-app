from flask import Flask, jsonify, render_template, request
import random

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
        game_state["food"] = [random.randint(0, 39) * 10, random.randint(0, 39) * 10]
        game_state["score"] += 10


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game-state", methods=["GET"])
def get_game_state():
    return jsonify(game_state)


@app.route("/move", methods=["POST"])
def move():
    if game_state["game_over"]:
        return jsonify(game_state)  # Don't allow moves when the game is over

    data = request.json
    game_state["direction"] = data.get("direction", game_state["direction"])
    move_snake()
    check_collisions()
    check_food()
    return jsonify(game_state)


@app.route("/reset", methods=["POST"])
def reset_game():
    game_state["snake"] = [(100, 100), (90, 100), (80, 100)]
    game_state["direction"] = "Right"
    game_state["food"] = [random.randint(0, 39) * 10, random.randint(0, 39) * 10]
    game_state["score"] = 0
    game_state["game_over"] = False
    return jsonify(game_state)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
