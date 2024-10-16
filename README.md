# Snake Game Web Application

This project was created for the **70085 Software Systems Engineering** course at **Imperial College London**.

## Introduction

This is a simple **Snake Game** web application built using **Flask** for the backend and **JavaScript** for the frontend. The goal of this project is to provide a fun, interactive game, while exploring core web development concepts like routing, form submission, and using API endpoints.

**Do be careful, this is a tricky snake**: In **impaas**, the snake will sometimes go down 1 block when you go left or right to disturb you (the player). This is part of the game's challenge to test your reflexes!

## Game Controls

- **Keyboard**:
    - Use the arrow keys to control the snake's direction (Up, Down, Left, Right).
  
- **On-screen buttons**:
    - The on-screen buttons are also available for controlling the snake.
    - Buttons are styled in a cross-like layout for intuitive interaction.

## Technologies Used

- **Python (Flask)**: Backend framework for API routing and form handling.
- **HTML/CSS**: For structuring and styling the frontend.
- **JavaScript**: For handling user input and updating the game state dynamically.
- **Jinja2**: For templating in the HTML files served by Flask.

## Features

- Classic Snake Game with scoring.
- Responsive controls using both keyboard and buttons on the screen.
- Automatically redirects back to the game after form submission.
- Built-in API to control the game state (move, reset).
- Simple form submission to enter player details.
