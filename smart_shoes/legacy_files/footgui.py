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
ser = serial.Serial('COM8', 115200)  # Replace 'COM5' with your COM port

def get_color(value):
    # Map sensor value to color range
    if value <= 50:
        return (1, 0, 0)  # Red for lower values
    elif value >= 400:
        return (0, 0, 1)  # Blue for higher values
    else:
        normalized_value = (value - 50) / 350  # Normalize value between 50 and 400
        return (1 - normalized_value, normalized_value, 0)  # Vary between red and green for intermediate values

def plot_circle(x, y, value):
    color = get_color(value)
    circle = plt.Circle((x, y), radius=10, color=color, alpha=0.7)
    ax.add_patch(circle)

while True:
    try:
        # Clear the previous circles for the next data update
        ax.clear()
        imgplot = ax.imshow(foot_img)

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

    except Exception as e:
        print("Error:", e)
