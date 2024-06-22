import tkinter as tk
import numpy as np
import random

G = 0.01


class Body:
    def __init__(self, mass, x, y, velocity):
        self.mass = mass
        self.x = x
        self.y = y
        self.pos = np.array([self.x, self.y], dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.radius = (self.mass * np.pi * 0.75) ** (1./3)

    def distance(self, body):
        return np.sqrt(np.sum((self.pos - body.pos) ** 2))

    def gravity_force(self, body):
        f = (G * self.mass * body.mass) / (self.distance(body) ** 2)

        return f

    @staticmethod
    def generate_bodies(n, mass_max, x_max, y_max, velocity_max):
        bodies = []

        for _ in range(n):
            mass = random.random() * mass_max
            x = random.uniform(10, x_max)
            y = random.uniform(10, y_max)
            velocity = np.array(
                [random.random() * velocity_max, random.random() * velocity_max], dtype=float)

            bodies.append(Body(mass, x, y, velocity))

        return bodies


class App(tk.Tk):
    def __init__(self, width, height, bodies):
        root = super().__init__()

        self.width = width
        self.height = height
        self.bodies = bodies
        self.universe = tk.Canvas(
            root, width=self.width, height=self.height, bg='gray9')
        self.universe.pack()

        self.render_universe()

    def render_universe(self, max_t=10000, t=0):
        tx = 50

        t += 1
        if t > max_t:
            return

        self.universe.delete('all')

        for body in self.bodies:
            for body_other in self.bodies:
                self.universe.create_oval(body.x - body.radius, body.y - body.radius, body.x + body.radius, body.y + body.radius,
                                          fill='medium sea green', outline='medium sea green')

                if body is body_other:
                    continue

                dx = body_other.x - body.x
                dy = body_other.y - body.y

                if dx == 0:
                    if dy > 0:
                        angle = -np.pi / 2
                    else:
                        angle = +np.pi / 2
                else:
                    angle = np.arctan(abs(dy) / abs(dx))

                force = body.gravity_force(body_other)
                acc = force / body.mass
                velocity = acc * tx

                # print(f'distance: {body.distance(body_other)}')
                # print(f'force: {force}')
                # print(f'acceleration: {acc}')
                # print(f'angle: {angle}')
                # print(f'velocity: {velocity}')
                # print(f'body velocity: {body.velocity}')

                if dx > 0:
                    body.velocity[0] += velocity * np.cos(angle)
                else:
                    body.velocity[0] -= velocity * np.cos(angle)
                if dy > 0:
                    body.velocity[1] += velocity * np.sin(angle)
                else:
                    body.velocity[1] -= velocity * np.sin(angle)

            temp_x = body.x + body.velocity[0]
            temp_y = body.y + body.velocity[1]

            if temp_x < 10 or temp_x > self.width - 10:
                body.velocity[0] *= -0.9

            if temp_y < 10 or temp_y > self.height - 10:
                body.velocity[1] *= -0.9

            body.x += body.velocity[0]
            body.y += body.velocity[1]

        self.universe.after(tx, self.render_universe, max_t, t)


# bodies = [
#     Body(1000, 500, 300, [0, 0]),
#     Body(80, 400, 100, [0.1, 0.5]),
#     Body(30, 700, 460, [0.8, 0.2]),
#     Body(120, 260, 40, [0.0, 0.6])
# ]
# print(bodies[0].distance(bodies[1]))
# print(bodies[0].gravity_force(bodies[1]))

X_SIZE, Y_SIZE = (800, 800)

bodies = Body.generate_bodies(
    30, 100, X_SIZE - 50, Y_SIZE - 50, 0)

app = App(X_SIZE, Y_SIZE, bodies)
app.mainloop()
