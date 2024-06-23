import tkinter as tk
import numpy as np
import random

G = 0.01


class Body:
    def __init__(self, mass, pos, velocity, color='medium sea green'):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.radius = (self.mass * np.pi * 0.75) ** (1./3)
        self.color = color

    def distance(self, body):
        return np.sqrt(np.sum((self.pos - body.pos) ** 2))

    def gravity_force(self, body):
        return (G * self.mass * body.mass) / (self.distance(body) ** 2)

    @staticmethod
    def generate_bodies(n, mass_max, x_max, y_max, velocity_max):
        bodies = []

        for _ in range(n):
            mass = random.random() * mass_max
            x = random.uniform(10, x_max)
            y = random.uniform(10, y_max)
            velocity = np.array(
                [random.random() * velocity_max, random.random() * velocity_max], dtype=float)

            bodies.append(Body(mass, [x, y], velocity))

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
        tx = 20
        dt = 80
        t += 1
        if t > max_t:
            return

        self.universe.delete('all')

        for body in self.bodies:
            for body_other in self.bodies:
                if body is body_other:
                    continue

                dx, dy = body_other.pos - body.pos

                if dx == 0:
                    if dy > 0:
                        angle = -np.pi / 2
                    else:
                        angle = +np.pi / 2
                else:
                    angle = np.arctan(abs(dy) / abs(dx))

                force = body.gravity_force(body_other)
                acc = force / body.mass
                velocity = acc * dt

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

            temp_pos = body.pos + body.velocity

            if temp_pos[0] < 10 or temp_pos[0] > self.width - 10:
                body.velocity[0] *= -0.5

            if temp_pos[1] < 10 or temp_pos[1] > self.height - 10:
                body.velocity[1] *= -0.5

            body.pos += body.velocity

            body_border = np.concatenate(
                (body.pos - body.radius, body.pos + body.radius))

            self.universe.create_oval(
                *body_border, fill=body.color, outline=body.color)

        self.universe.after(tx, self.render_universe, max_t, t)


bodies = [
    # Body(10, 200, 200, [0.1, -0.1]),
    # Body(10, 400, 400, [-0.1, 0.1]),
    Body(10, [450, 250], [4, 0], 'MediumPurple2'),
    Body(10, [350, 250], [4, 0], 'firebrick3'),
    Body(10, [350, 150], [1, 0], 'DeepSkyBlue2')
]
# print(bodies[0].distance(bodies[1]))
# print(bodies[0].gravity_force(bodies[1]))

X_SIZE, Y_SIZE = (700, 700)

# bodies = Body.generate_bodies(
#     20, 100, X_SIZE - 50, Y_SIZE - 50, 0)
bodies.append(Body(1500, [350, 350], [0, 0]))

app = App(X_SIZE, Y_SIZE, bodies)
app.mainloop()
