"""PyPython game rules: the snake, the food and the score. No drawing and no browser code in here."""
import random

COLS = ROWS = 24
BASE_TICK_MS, MIN_TICK_MS = 120, 65

# weight = relative spawn odds, ttl = ms before a special food vanishes (0 = never)
FOODS = [
    {"mult": 1,  "points": 10,  "weight": 70, "ttl": 0,    "color": 0xe4583f},
    {"mult": 3,  "points": 30,  "weight": 20, "ttl": 9000, "color": 0x5d96bf},
    {"mult": 5,  "points": 50,  "weight": 8,  "ttl": 7000, "color": 0xa867b0},
    {"mult": 10, "points": 100, "weight": 2,  "ttl": 5000, "color": 0xf2c14e},
]
MODES = {"classic": "CLASSIC", "teleport": "TELEPORT"}
DIRS = {"up": (0, -1), "w": (0, -1), "down": (0, 1), "s": (0, 1),
        "left": (-1, 0), "a": (-1, 0), "right": (1, 0), "d": (1, 0)}


class Game:
    def __init__(self, mode="classic", rng=random):
        self.mode = mode
        self.rng = rng
        self.snake = [(12, 12), (11, 12), (10, 12)]  # head first
        self.prev = list(self.snake)                 # positions before the last step (for animation)
        self.direction = (1, 0)
        self.queue = []                              # buffered turns (max 2)
        self.score = 0
        self.alive = True
        self.food = self.spawn_food(0)

    @property
    def tick_ms(self):
        return max(MIN_TICK_MS, BASE_TICK_MS - (self.score // 50) * 3)

    def spawn_food(self, now_ms):
        kind = self.rng.choices(FOODS, weights=[f["weight"] for f in FOODS])[0]
        taken = set(self.snake)
        free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in taken]
        if not free:                                  # board full: you win
            self.alive = False
            return {**FOODS[0], "pos": (-1, -1), "born": now_ms}
        return {**kind, "pos": self.rng.choice(free), "born": now_ms}

    def turn(self, direction):
        """Queue a turn; ignores reversals and repeats."""
        ref = self.queue[-1] if self.queue else self.direction
        if len(self.queue) < 2 and direction != ref and direction != (-ref[0], -ref[1]):
            self.queue.append(direction)

    def step(self, now_ms):
        """Advance one tick. Returns the food eaten this tick, or None."""
        if self.queue:
            self.direction = self.queue.pop(0)
        hx = self.snake[0][0] + self.direction[0]
        hy = self.snake[0][1] + self.direction[1]
        if self.mode == "teleport":
            hx, hy = hx % COLS, hy % ROWS
        elif not (0 <= hx < COLS and 0 <= hy < ROWS):
            self.alive = False
            return None
        head = (hx, hy)
        eating = head == self.food["pos"]
        body = self.snake if eating else self.snake[:-1]   # tail moves away unless we grow
        if head in body:
            self.alive = False
            return None
        self.prev = list(self.snake)
        self.snake.insert(0, head)
        if not eating:
            self.snake.pop()
        if eating:
            eaten = self.food
            self.score += eaten["points"]
            self.food = self.spawn_food(now_ms)
            return eaten
        if self.food["ttl"] and now_ms - self.food["born"] > self.food["ttl"]:
            self.food = self.spawn_food(now_ms)
        return None
