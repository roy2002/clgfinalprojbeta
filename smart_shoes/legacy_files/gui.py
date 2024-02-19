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
    (167, 606), (111, 316), (97,450), (180, 305), (194, 255)
]

# Establish serial connection
ser = serial.Serial('COM8', 115200)  # Replace 'COM5' with your COM port

def plot_circle(x, y, value):
    colormap = plt.cm.hot  # Adjust colormap as needed
    normalized_value = min(value, 400) / 400.0  # Normalize value between 0 and 1
    circle = plt.Circle((x, y), radius=10, color=colormap(normalized_value), alpha=0.7)
    ax.add_patch(circle)

while True:
    try:
        data = ser.readline().decode().strip()
        sensor_data = json.loads(data)  # Decode JSON data

        # Plot sensor data on the foot image
        for sensor_id, value in sensor_data.items():
            value = int(value)
            sensor_number = int(sensor_id[6:]) - 1  # Extract sensor number from 'sensorX'
            if 0 <= sensor_number < len(circle_positions):
                x, y = circle_positions[sensor_number]  # Get circle position
                plot_circle(x, y, value)

        # Refresh the plot
        fig.canvas.draw()
        plt.pause(0.1)  # Adjust the pause duration as needed

        # Clear the previous circles for the next data update
        ax.clear()
        imgplot = ax.imshow(foot_img)

    except Exception as e:
        print("Error:", e)
