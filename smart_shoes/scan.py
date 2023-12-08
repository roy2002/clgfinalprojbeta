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
ser = serial.Serial('COM5', 115200)  # Replace 'COM10' with your COM port

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
                # Assign color based on value ranges
                if value <= 20:
                    color = 'red'
                    alpha = 0.5
                elif 20 < value <= 100:
                    color = 'orange'
                    alpha = 0.6
                elif 100 < value <= 200:
                    color = 'green'
                    alpha = 0.7
                elif 200 < value <= 300:
                    color = 'yellow'
                    alpha = 0.8
                else:
                    color = 'blue'
                    alpha = 0.9
                circle = plt.Circle((x, y), radius=10, color=color, alpha=alpha)
                ax.add_patch(circle)
        
        # Refresh the plot
        fig.canvas.draw()
        plt.pause(0.1)  # Adjust the pause duration as needed

        # Clear the previous circles for the next data update
        ax.clear()
        imgplot = ax.imshow(foot_img)

    except Exception as e:
        print("Error:", e)
