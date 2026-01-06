import re
import numpy as np
import matplotlib.pyplot as plt

def parse_header_file(filename):
    """
    Parses a C header file to extract LED position data from a struct array.

    Args:
        filename (str): The path to the C header file.

    Returns:
        np.ndarray: A NumPy array containing the LED positions.
    """
    with open(filename, 'r') as f:
        content = f.read()

    # Regex to find the C array definition and capture the content inside the curly braces.
    match = re.search(r'const Position ledPositions\[NUM_LEDS\] = \{(.*?)\};', content, re.DOTALL)
    if not match:
        raise ValueError("Could not find ledPositions array in header file.")

    raw_data = match.group(1)
    
    # Use regex to find all the numeric pairs within the struct initialization.
    positions_matches = re.findall(r'\{ (.*?),\s*(.*?) \}', raw_data)
    
    positions = []
    for match in positions_matches:
        try:
            x = float(match[0].strip('f'))
            z = float(match[1].strip('f'))
            # Filter out any placeholder data points like {-999, -999}
            if x > -900 and z > -900:
                positions.append((x, z))
        except (ValueError, IndexError):
            # Skip any lines that don't conform to the expected format
            continue

    if not positions:
        raise ValueError("No valid position data found in header file.")
        
    return np.array(positions)



# plot points
def visualize_led_pos_points(positions):

    x, z = positions[:, 0], positions[:, 1]
    
    fig, ax = plt.subplots()
    ax.scatter(x, z, c='red', marker='o')
    
    for i, (xi, zi) in enumerate(zip(x, z)):
        ax.text(xi, zi, f'  {i}', va='center', ha='left', fontsize=9)
        
    ax.set_title('2D LED Position Visualization (X vs Z)')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Z Coordinate')
    ax.grid(True)
    ax.axis('equal')  # Ensure equal scaling for X and Z axes
    
    plt.show()


# shows connecting lines
def visualize_led_pos(positions):

    x, z = positions[:, 0], positions[:, 1]
    
    fig, ax = plt.subplots()
    ax.plot(x, z, color='grey', linestyle='--', linewidth=1, marker='o', markersize=6, markerfacecolor='red')

    # label each point with led number
    for i, (xi, zi) in enumerate(zip(x, z)):
        ax.text(xi, zi, f'  {i}', va='center', ha='left', fontsize=9)

    # label each line with its length
    for i in range(len(x) - 1):
        x1, z1 = x[i], z[i]
        x2, z2 = x[i+1], z[i+1]

        distance = np.sqrt((x2 - x1)**2 + (z2 - z1)**2)

        mid_x = (x1 + x2) / 2
        mid_z = (z1 + z2) / 2

        ax.text(mid_x, mid_z, f'  {distance:.1f}', va='center', ha='left', fontsize=7, color='blue')


        
    ax.set_title('2D LED Position Visualization (X vs Z)')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Z Coordinate')
    ax.grid(True)
    ax.axis('equal')  # Ensure equal scaling for X and Z axes
    
    plt.show()



# shows connecting lines
def visualize_led_pos_with_regularization(positions):

    x, z = positions[:, 0], positions[:, 1]

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(x, z, color='grey', linestyle='--', linewidth=1, marker='o', markersize=6, markerfacecolor='red')
    
    # -------- not regularized ------- #

    # label each point with led number
    for i, (xi, zi) in enumerate(zip(x, z)):
        ax1.text(xi, zi, f'  {i}', va='center', ha='left', fontsize=9)

    # label each line with its length
    for i in range(len(x) - 1):
        x1, z1 = x[i], z[i]
        x2, z2 = x[i+1], z[i+1]

        distance = np.sqrt((x2 - x1)**2 + (z2 - z1)**2)

        mid_x = (x1 + x2) / 2
        mid_z = (z1 + z2) / 2

        ax1.text(mid_x, mid_z, f'  {distance:.1f}', va='center', ha='left', fontsize=7, color='blue')


        
    ax1.set_title('2D LED Position Visualization (X vs Z)')
    ax1.set_xlabel('X Coordinate')
    ax1.set_ylabel('Z Coordinate')
    ax1.grid(True)
    ax1.axis('equal')  # Ensure equal scaling for X and Z axes



    # ----- regularized ----- #

    max_distance = 1 # could update this
        
    for led in range(len(x) - 1):
        prev_x, prev_z = positions[led-1]
        current_x, current_z = positions[led]
        next_x, next_z = positions[led+1]

        prev_distance = np.sqrt((current_x - prev_x)**2 + (current_z - prev_z)**2)
        next_distance = np.sqrt((next_x - current_x)**2 + (next_z - current_z)**2)

        # If distance > 1 between previous and next, put position between the two
        # try and/or
        if (prev_distance > max_distance and next_distance > max_distance):
            mid_x = (prev_x + next_x) / 2
            mid_z = (prev_z + next_z) / 2
            x[led], z[led] = mid_x, mid_z

    ax2.plot(x, z, color='grey', linestyle='--', linewidth=1, marker='o', markersize=6, markerfacecolor='blue')


    # label each point with led number
    for i, (xi, zi) in enumerate(zip(x, z)):
        ax2.text(xi, zi, f'  {i}', va='center', ha='left', fontsize=9)

    # label each line with its length
    for i in range(len(x) - 1):
        x1, z1 = x[i], z[i]
        x2, z2 = x[i+1], z[i+1]

        distance = np.sqrt((x2 - x1)**2 + (z2 - z1)**2)

        mid_x = (x1 + x2) / 2
        mid_z = (z1 + z2) / 2

        ax2.text(mid_x, mid_z, f'  {distance:.1f}', va='center', ha='left', fontsize=7, color='blue')


        
    ax2.set_title('2D LED Position Visualization (X vs Z) -- Regularized')
    ax2.set_xlabel('X Coordinate')
    ax2.set_ylabel('Z Coordinate')
    ax2.grid(True)
    ax2.axis('equal')  # Ensure equal scaling for X and Z axes
    
    plt.tight_layout()
    plt.show()



    filename=r"C:\Users\conno\OneDrive\Desktop\Projects\Christmas Tree\Led Mapping (Arduino)\include\led_pos_regularized.h"
    
    with open(filename, 'w') as f:
        f.write("#ifndef LED_POS_REGULARIZED_H\n")
        f.write("#define LED_POS_REGULARIZED_H\n\n")
        
        # Define a struct for position data
        f.write("struct Position { float x, z; };\n\n")
        
        # Create a C++ array of Position structs
        f.write(f"const int NUM_LEDS = {len(x)};\n")
        f.write("const Position ledPositions[NUM_LEDS] = {\n")
        
        for led in range(len(x)):
            f.write(f"  {{ {x[led]:.6f}f, {z[led]:.6f}f }},\n")
        
        f.write("};\n\n")
        f.write("#endif // LED_POS_REGULARIZED_H\n")

    print(f"Saved final positions to {filename}")



file_path = r"C:\Users\conno\OneDrive\Desktop\Projects\Christmas Tree\Led Mapping (Arduino)\include\led_positions.h"

if __name__ == "__main__":
    led_positions_data = parse_header_file(file_path)
    visualize_led_pos_with_regularization(led_positions_data)
    # visualize_led_pos(led_positions_data)
    # visualize_led_pos_points(led_positions_data)

