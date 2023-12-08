import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import serial
import json

# Load foot picture
foot_img = mpimg.imread('foot.png')

# Create a subplot
fig, ax = plt.subplots()
imgplot = ax.imshow(foot_img)

# Define the positions of the circles on the foot photo for sensors
circle_positions = [
    (195, 250), (110, 307), (180, 305), (100, 445), (167, 606)
]

# Establish serial connection
ser = serial.Serial('COM5', 115200)  # Replace 'COM5' with your COM port

def plot_circle(x, y, color, alpha):
    circle = plt.Circle((x, y), radius=10, color=color, alpha=alpha)
    ax.add_patch(circle)

while True:
    try:
        data = ser.readline().decode().strip()
        sensor_data = json.loads(data)  # Decode JSON data

        # Map sensor IDs to plot functions
        plot_functions = {
            'sensor1': lambda value: plot_circle(circle_positions[0][0], circle_positions[0][1], 'red', 0.5) if value <= 20 else None,
            'sensor2': lambda value: plot_circle(circle_positions[1][0], circle_positions[1][1], 'orange', 0.6) if value <= 100 else None,
            'sensor3': lambda value: plot_circle(circle_positions[2][0], circle_positions[2][1], 'green', 0.7) if value <= 200 else None,
            'sensor4': lambda value: plot_circle(circle_positions[3][0], circle_positions[3][1], 'yellow', 0.8) if value <= 300 else None,
            'sensor5': lambda value: plot_circle(circle_positions[4][0], circle_positions[4][1], 'blue', 0.9) if value <= 400 else None
        }

        # Plot sensor data on the foot image
        for sensor_id, value in sensor_data.items():
            value = int(value)
            if sensor_id in plot_functions:
                plot_functions[sensor_id](value)

        # Refresh the plot
        fig.canvas.draw()
        plt.pause(0.1)  # Adjust the pause duration as needed

        # Clear the previous circles for the next data update
        ax.clear()
        imgplot = ax.imshow(foot_img)

    except Exception as e:
        print("Error:", e)
