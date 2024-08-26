import tkinter as tk
import numpy as np
import random
from utils import load_yaml

G = 0.01  # Gravitational constant


class Body:
    def __init__(self, mass, pos, velocity, log_size, isStatic=False, color=None, trail_color=None):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.isStatic = isStatic

        # Calculate the radius of sphere based on its mass
        # Assuming a constant density = 1
        # volume = (0.75) * pi * radius ^ 3, mass = volume * density
        # Thus, radius = (mass * pi * 0.75)^1/3
        self.radius = (self.mass * np.pi * 0.75) ** (1./3)

        if color is None:
            self.color = "medium sea green"
        else:
            self.color = color

        if trail_color is None:
            self.trail_color = "darkslategray"
        else:
            self.trail_color = trail_color

        # keep history of previous positions
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
                Body(mass, [x, y], velocity, properties['trail_length'], False, color, properties['trail_color']))

        return bodies


class App(tk.Tk):
    def __init__(self, CONFIG_PATH, BODIES_PATH=None):
        root = super().__init__()
        properties = load_yaml(CONFIG_PATH)['properties']

        self.width = properties['width']
        self.height = properties['height']

        # Populating bodies list
        if properties['generate_bodies']:
            properties['body']['x_max'] = self.width - properties['x_padding']
            properties['body']['y_max'] = self.width - properties['y_padding']

            self.bodies = Body.generate_bodies(properties['body'])
            if properties['append_bodies']:
                self.bodies += [Body(**body)
                                for body in load_yaml(BODIES_PATH)]
        else:
            self.bodies = [Body(**body) for body in load_yaml(BODIES_PATH)]

        # Generate universe
        self.universe = tk.Canvas(
            root, width=self.width, height=self.height, bg=properties['bg_color'])
        self.universe.pack()

        # Start simulation
        self.render_universe(properties['max_time'], properties['start_time'])

    def render_universe(self, max_t, t):
        tx = 20  # One time frame
        dt = 10  # Change in time per time frame
        t += 1  # Keeps track of total time frames
        if t > max_t:
            return

        self.universe.delete('all')

        # Calculate net force on each body
        for body in self.bodies:
            # Calculate force exerted by each body
            for body_other in self.bodies:
                if body is body_other:
                    continue

                if not body.isStatic:
                    dx, dy = body_other.pos - body.pos

                    # Avoid division by zero when calculating angle
                    if dx == 0:
                        angle = np.pi / 2  # 90 degrees
                    else:
                        angle = np.arctan(abs(dy) / abs(dx))

                    # Compute gravitational force exerted by another body
                    force = body.gravity_force(body_other)
                    acc = force / body.mass
                    velocity = acc * dt

                    # Add perpendicular components of velocity according to direction of force
                    if dx > 0:
                        body.velocity[0] += velocity * np.cos(angle)
                    else:
                        body.velocity[0] -= velocity * np.cos(angle)
                    if dy > 0:
                        body.velocity[1] += velocity * np.sin(angle)
                    else:
                        body.velocity[1] -= velocity * np.sin(angle)

            # Stop bodies from going out-of-bounds by bouncing them back
            temp_pos = body.pos + body.velocity * dt

            if temp_pos[0] < 10 or temp_pos[0] > self.width - 10:
                body.velocity[0] *= -0.5

            if temp_pos[1] < 10 or temp_pos[1] > self.height - 10:
                body.velocity[1] *= -0.5

            # update bodies position based upon net force
            body.pos += body.velocity * dt

            body_border = np.concatenate(
                (body.pos - body.radius, body.pos + body.radius))

            # maintain history of previous positions, removing the oldest position
            body.log_pos = [*body.pos] + body.log_pos[:-2]

            # Draw body on canvas
            self.universe.create_line(
                body.log_pos, smooth=True, width=2, fill=body.trail_color)
            self.universe.create_oval(
                *body_border, fill=body.color, outline=body.color)

        # Adds delay between before rendering next frame
        self.universe.after(tx, self.render_universe, max_t, t)


app = App('./config.yaml', './examples/orbit.yaml')
app.resizable(False, False)
app.mainloop()
