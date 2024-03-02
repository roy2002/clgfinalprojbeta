import matplotlib.pyplot as plt

# Provided data
y_values = [7.666968, 8.26184, 8.706408, 8.711288, 8.732272, 9.222712, 8.806488, 8.989448, 8.662976]
x_values = [1.524, 1.6256, 1.6764, 1.6764, 1.7018, 1.7018, 1.778, 1.8034, 1.8288]


# Plotting the scatter plot
plt.scatter(x_values, y_values)

# Labeling axes
plt.xlabel('Height')
plt.ylabel('Mean')

# Adding title
plt.title('Height V/S Mean')

plt.savefig("Height_vs_Mean.jpg")

# Display the plot
plt.show()

#

# Given data in feet.inch
# data_feet_inches = [5.7, 5.4, 5, 5.6, 5.7, 5.6, 6, 5.10, 5.9]
#
# # Conversion function
# def feet_inches_to_meters(feet_inches):
#     feet = int(feet_inches)
#     inches = (feet_inches - feet) * 12
#     total_meters = (feet * 0.3048) + (inches * 0.0254)
#     return total_meters
#
# # Convert the data to meters
# data_meters = [feet_inches_to_meters(value) for value in data_feet_inches]
#
# # Display the converted data
# print("Original data (feet.inch):", data_feet_inches)
# print("Converted data (meters):", data_meters)
#
