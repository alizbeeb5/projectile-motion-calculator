from flask import Flask, render_template, request
from markupsafe import Markup
import math

app = Flask(__name__)


def calculate_projectile_motion(initial_velocity, launch_angle):
    # Convert launch angle from degrees to radians
    launch_angle_rad = launch_angle * (math.pi / 180)

    # Calculate horizontal and vertical components of initial velocity
    initial_velocity_x = initial_velocity * math.cos(launch_angle_rad)
    initial_velocity_y = initial_velocity * math.sin(launch_angle_rad)

    # Calculate time of flight
    time_of_flight = (2 * initial_velocity_y) / 9.81

    # Calculate horizontal range
    horizontal_range = initial_velocity_x * time_of_flight

    # Calculate maximum height
    max_height = (initial_velocity_y**2) / (2 * 9.81)

    # Calculate trajectory points
    time_step = time_of_flight / 100
    time_points = [i * time_step for i in range(101)]
    x_points = [initial_velocity_x * t for t in time_points]
    y_points = [initial_velocity_y * t - 0.5 * 9.81 * t**2 for t in time_points]

    # Calculate velocity vectors at each point
    velocity_x = [initial_velocity_x for _ in time_points]
    velocity_y = [initial_velocity_y - 9.81 * t for t in time_points]

    return {
        "time_of_flight": time_of_flight,
        "horizontal_range": horizontal_range,
        "max_height": max_height,
        "trajectory": (x_points, y_points),
        "velocity_x": velocity_x,
        "velocity_y": velocity_y,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        initial_velocity = float(request.form["initial_velocity"])
        launch_angle = float(request.form["angle"])
        results = calculate_projectile_motion(initial_velocity, launch_angle)
        return render_template("index.html", results=results)
    return render_template("index.html", results=None)


if __name__ == "__main__":
    app.run(debug=True)
