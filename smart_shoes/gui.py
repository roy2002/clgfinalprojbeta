import serial
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import json

# Define threshold values for color mapping
red_threshold = 10
orange_threshold = 20
blue_threshold = 30

# Load foot picture
foot_img = mpimg.imread(r'foot.png')

# Create a subplot
fig, ax = plt.subplots()
imgplot = ax.imshow(foot_img)

# Define the positions of the circles on the foot photo for sensors
circle_positions = [
    (195, 250), (110, 307), (180, 305), (100, 445), (167, 606)
]

# Create custom colormaps
red_cmap = plt.cm.Reds
orange_cmap = plt.cm.Oranges
blue_cmap = plt.cm.Blues

def value_to_color_and_size(value):
    # Map data value to color and size
    if value < red_threshold:
        cmap = red_cmap
        size = 100
    elif value < orange_threshold:
        cmap = orange_cmap
        size = 200
    else:
        cmap = blue_cmap
        size = 300
    return cmap(value / blue_threshold), size

# Create a heatmap object
heatmap = ax.scatter(np.array([]), np.array([]), c=[], s=100, alpha=0.3)

# Open a serial connection
ser = serial.Serial('COM10', 9600)

def update_heatmap():
    try:
        data = ser.readline().decode().strip()
        sensor_data = json.loads(data)  # Decode JSON data

        # Process each sensor data entry
        for sensor_id, value in sensor_data.items():
            value = int(value)
            # Map data to color and size
            color, size = value_to_color_and_size(value)

            # Update heatmap for the corresponding sensor position
            sensor_number = int(sensor_id[6:]) - 1  # Extract sensor number from 'sensorX'
            if 0 <= sensor_number < len(circle_positions):
                heatmap.set_offsets([circle_positions[sensor_number]])
                heatmap.set_array([color])
                heatmap.set_sizes([size])
                fig.canvas.draw()

    except (ValueError, KeyError) as e:
        print("Error decoding JSON:", e)

    # Schedule the update after a delay
    root.after(100, update_heatmap)  # Adjust the delay (in milliseconds) as needed

def plot_on_tkinter():
    global root
    root = tk.Tk()
    root.title("Heatmap GUI")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    # Start updating the heatmap
    update_heatmap()

    root.mainloop()

plot_on_tkinter()
