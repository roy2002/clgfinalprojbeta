import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import cv2

foot_img = mpimg.imread('foot.png')
# Replace 'your_data.csv' with the path to your CSV file
csv_file = 'Pritwish_attemp1.csv'

# Specify the column names for left and right sensors
left_sensor_names = ['Sensor1-L', 'Sensor2-L', 'Sensor3-L', 'Sensor4-L', 'Sensor5-L']
right_sensor_names = ['Sensor1-R', 'Sensor2-R', 'Sensor3-R', 'Sensor4-R', 'Sensor5-R']

# Read CSV data into a DataFrame
df = pd.read_csv(csv_file)

timestamp_list = df['Timestamp'].tolist()


# Initialize lists for each column for both left and right sensors
left_column_data = {col: df[col].tolist() for col in left_sensor_names}
right_column_data = {col: df[col].tolist() for col in right_sensor_names}

# Circle positions
circle_positions = [
    (167, 606), (111, 316), (97,450), (180, 305), (194, 255)
]

circle_positions2 = [(307, 244), (334, 422), (325, 300), (388, 299),(350, 601)]


# Set up video parameters
video_filename = 'pritwish_video.gif'
fps = 2

# Plotting the foot image
fig, ax = plt.subplots()
ax.imshow(foot_img)

# Define a custom colormap using RdYlGn
cmap = cm.get_cmap('RdYlGn_r')


# Update function for animation
def update(frame):
    ax.clear()
    ax.imshow(foot_img)

    # Plot points for left sensors
    for col, position, values in zip(left_sensor_names, circle_positions, left_column_data.values()):
        value = values[frame]
        if min(values) == max(values):  # Check if min and max are equal to avoid division by zero
            normalized_value = max(values)
        else:
            normalized_value = (value - min(values)) / (max(values) - min(values))
        color = cmap(normalized_value)
        ax.scatter(position[0], position[1], color=color, marker='o', label=f'{col} Point')

    # Plot points for right sensors
    for col, position, values in zip(right_sensor_names, circle_positions2, right_column_data.values()):
        value = values[frame]
        print(max(values) - min(values))
        if min(values) == max(values):  # Check if min and max are equal to avoid division by zero
            normalized_value = max(values)
        else:
            normalized_value = (value - min(values)) / (max(values) - min(values))
        print("Normal", normalized_value)
        color = cmap(normalized_value)
        ax.scatter(position[0], position[1], color=color, marker='o',
                   label=f'{col} Point')  # Adjust X position for right sensors

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(f'Frame {frame + 1}')

    # Optional: Display a legend
    # ax.legend()


# Create animation
num_frames = min(len(col_data) for col_data in left_column_data.values())
animation = FuncAnimation(fig, update, frames=num_frames, interval=1000 / fps)

# Save the animation as a GIF
animation.save(video_filename, writer='pillow', fps=fps)

# Show the plot (optional)
plt.show()
