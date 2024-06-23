import tkinter as tk
import numpy as np
import random

G = 0.01


class Body:
    def __init__(self, mass, pos, velocity, log_size, color=None, trail_color=None):

        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.radius = (self.mass * np.pi * 0.75) ** (1./3)

        if color is None:
            self.color = "medium sea green"
        else:
            self.color = color

        if trail_color is None:
            self.trail_color = "darkslategray"
        else:
            self.trail_color = trail_color

        self.log_pos = [*pos] + [None for _ in range(log_size - 2)]

    def distance(self, body):
        return np.sqrt(np.sum((self.pos - body.pos) ** 2))

    def gravity_force(self, body):
        return (G * self.mass * body.mass) / (self.distance(body) ** 2)

    @staticmethod
    def generate_bodies(properties):
        bodies = []

        for _ in range(properties['num_bodies']):
            mass = random.random() * properties['mass_max']
            x = random.uniform(10, properties['x_max'])
            y = random.uniform(10, properties['y_max'])
            velocity = np.array(
                [random.random() * properties['velocity_max'], random.random() * properties['velocity_max']], dtype=float)

            if properties['random_color']:
                color = "#"+("%06x" % random.randint(0, 16777215))
            else:
                color = properties['color']

            bodies.append(
                Body(mass, [x, y], velocity, properties['trail_length'], color, properties['trail_color']))

        return bodies


class App(tk.Tk):
    def __init__(self, properties):
        root = super().__init__()

        self.width = properties['width']
        self.height = properties['height']

        if properties['generate_bodies']:
            self.bodies = Body.generate_bodies(properties['body'])
            if properties['append_bodies']:
                self.bodies += (properties['bodies'])
        else:
            self.bodies = properties['bodies']

        self.universe = tk.Canvas(
            root, width=self.width, height=self.height, bg=properties['bg_color'])
        self.universe.pack()

        self.render_universe(properties['max_time'], properties['start_time'])

    def render_universe(self, max_t, t):
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

            body.log_pos = [*body.pos] + body.log_pos[:-2]

            self.universe.create_line(
                body.log_pos, smooth=True, width=2, fill=body.trail_color)
            self.universe.create_oval(
                *body_border, fill=body.color, outline=body.color)

        self.universe.after(tx, self.render_universe, max_t, t)


bodies = [
    Body(10, [350, 250], [3.5, 0], 80, 'firebrick3'),
    Body(10, [350, 150], [2.5, 0], 80, 'DeepSkyBlue2'),
    Body(10, [350, 50], [2, 0], 80, 'MediumPurple2'),
    Body(1500, [350, 350], [0, 0], 80)
]

X_SIZE, Y_SIZE = (700, 700)

properties = {
    'width': X_SIZE,
    'height': Y_SIZE,
    'bg_color': 'gray9',
    'max_time': 10000,
    'start_time': 0,
    'generate_bodies': False,
    'append_bodies': False,
    'bodies': bodies,
    'body': {
        'num_bodies': 5,
        'mass_max': 100,
        'x_max': X_SIZE - 50,
        'y_max': Y_SIZE - 50,
        'velocity_max': 0,
        'trail_length': 40,
        'random_color': False,
        'trail_color': 'darkslategray',
        'color': "medium sea green"
    }
}

app = App(properties)
app.mainloop()
