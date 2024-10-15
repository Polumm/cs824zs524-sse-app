const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
let direction = "Right";

// Listen for key presses to change direction
document.addEventListener("keydown", (event) => {
    const key = event.key;
    if (key === "ArrowUp") direction = "Up";
    if (key === "ArrowDown") direction = "Down";
    if (key === "ArrowLeft") direction = "Left";
    if (key === "ArrowRight") direction = "Right";
    if (key === "r" || key === "R") resetGame();
});

function updateGame() {
    // Send current direction to server
    fetch("/move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ direction }),
    })
    .then((response) => response.json())
    .then((data) => {
        drawGame(data.snake, data.food, data.score);
        if (data.game_over) {
            document.getElementById("game-over").style.display = "block";
        }
    });
}

function drawGame(snake, food, score) {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the snake
    snake.forEach(([x, y]) => {
        ctx.fillStyle = "white";
        ctx.fillRect(x, y, 10, 10);
    });

    // Draw the food
    const [foodX, foodY] = food;
    ctx.fillStyle = "red";
    ctx.fillRect(foodX, foodY, 10, 10);

    // Update the score
    document.getElementById("score").textContent = score;
}

function resetGame() {
    fetch("/reset", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then((response) => response.json())
    .then(() => {
        document.getElementById("game-over").style.display = "none";
        direction = "Right";
    });
}

// Update the game every 100ms
setInterval(updateGame, 100);
