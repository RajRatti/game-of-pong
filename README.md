# Pong

A simple two-player Pong game made in Python using Pygame.

The game is played locally on one computer, with each player controlling a paddle on opposite sides of the screen. The ball gets faster every time it hits a paddle, so rallies become harder to keep going.

## Preview

![Pong Game](Pong_View.png)

## How it works

```text
Start the program
       │
       ▼
Instructions are printed
       │
       ▼
     Pong
       │
       ├── Player 1: W / S
       │
       ├── Player 2: ↑ / ↓
       │
       └── Ball gets faster after each paddle hit
                    │
                    ▼
          Ball gets past a paddle
                    │
                    ▼
             Player scores
                    │
                    ▼
             Ball resets
                    │
                    ▼
          Press ENTER to continue
                    │
                    ▼
       First player to 5 points wins