import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button
import serial
import json

# Load foot picture
foot_img = mpimg.imread('foot.png')

# Create a subplot
fig, ax = plt.subplots()
imgplot = ax.imshow(foot_img)

# Define positions for sensor circles
circle_positions = [
    (195, 250), (110, 307), (180, 305), (100, 445), (167, 606)
]

# Define color map for sensor data
cmap = plt.cm.inferno
norm = plt.Normalize(0, 500)

# Create sensor circles
circles = []
for position in circle_positions:
    circle = plt.Circle(xy=position, radius=10, color=cmap(0.5), alpha=0.3, zorder=10)
    ax.add_patch(circle)
    circles.append(circle)

# Establish serial connection
ser = serial.Serial('COM5', 115200)

# Function to update circle color and size
def update_circle(sensor_id, value):
    if 0 <= value <= 500:
        color = cmap(norm(value))
        circles[sensor_id].set_color(color)
        circles[sensor_id].set_alpha(0.8)
    else:
        circles[sensor_id].set_color(cmap(0.5))
        circles[sensor_id].set_alpha(0.3)

# Function to handle data received from serial port
def handle_data(data):
    try:
        sensor_data = json.loads(data.decode().strip())
        for sensor_id, value in sensor_data.items():
            update_circle(int(sensor_id), int(value))
        fig.canvas.draw()
    except Exception as e:
        print("Error:", e)

# Button to clear circles and reset plot
reset_button = Button(ax.transAxes, "Reset", (0.9, 0.1), color='lightgray', hovercolor='gray')

def reset_plot(event):
    for circle in circles:
        circle.set_color(cmap(0.5))
        circle.set_alpha(0.3)
    fig.canvas.draw()

reset_button.on_clicked(reset_plot)

# Read data from serial port continuously
while True:
    data = ser.readline()
    if data:
        handle_data(data)

# Display the plot
plt.show()
