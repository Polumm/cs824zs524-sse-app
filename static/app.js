const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
let direction = null;  // Initially, snake won't move until a key is pressed
let gameStarted = false;

// Show the "Press any key to start" prompt
const promptMessage = document.createElement("div");
promptMessage.innerHTML = "Press any direction key to start";
promptMessage.style.color = "white";
promptMessage.style.fontSize = "24px";
promptMessage.style.position = "absolute";
promptMessage.style.top = "50%";
promptMessage.style.left = "50%";
promptMessage.style.transform = "translate(-50%, -50%)";
promptMessage.style.display = "block";  // Show the prompt at the very beginning
document.body.appendChild(promptMessage);

// Prevent window resizing
window.addEventListener('resize', function(event) {
    event.preventDefault();  // Prevent any resize actions
    window.resizeTo(400, 400);  // Optional: Fixed size, adjust to your desired size
});

// Prevent default arrow key behavior (scrolling)
window.addEventListener("keydown", function(event) {
    // If the arrow keys are pressed, prevent scrolling
    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.key)) {
        event.preventDefault();
    }
});

// Listen for key presses to change direction and start the game
document.addEventListener("keydown", (event) => {
    const key = event.key;
    gameStarted = true;  // Start game on key press
    promptMessage.style.display = "none";  // Hide the prompt when the game starts

    // Improve key handling to prevent unintended direction changes
    if (key === "ArrowUp" && direction !== "Down") {
        direction = "Up";
    } 
    if (key === "ArrowDown" && direction !== "Up") {
        direction = "Down";
    } 
    if (key === "ArrowLeft" && direction !== "Right") {
        direction = "Left";
    } 
    if (key === "ArrowRight" && direction !== "Left") {
        direction = "Right";
    }

    // Handle reset game when 'R' is pressed
    if (key === "r" || key === "R") resetGame();
});

function updateGame() {
    if (!gameStarted || !direction) return;  // Don't update if the game hasn't started or no direction is set

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
                gameStarted = false;  // Stop the game if it's over
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
            direction = null;  // Reset direction so the snake doesn't move until a key is pressed
            gameStarted = false;  // Reset the game state
            promptMessage.style.display = "block";  // Show the prompt message after reset
            promptMessage.innerHTML = "Press any direction key to start";  // Re-show the start message
        });
}

// Button event listeners for on-screen controls
function upButtonClicked() {
    if (direction !== "Down") direction = "Up";
    gameStarted = true;
    promptMessage.style.display = "none";
}

function downButtonClicked() {
    if (direction !== "Up") direction = "Down";
    gameStarted = true;
    promptMessage.style.display = "none";
}

function leftButtonClicked() {
    if (direction !== "Right") direction = "Left";
    gameStarted = true;
    promptMessage.style.display = "none";
}

function rightButtonClicked() {
    if (direction !== "Left") direction = "Right";
    gameStarted = true;
    promptMessage.style.display = "none";
}

// Update the game every 100ms
setInterval(updateGame, 100);
