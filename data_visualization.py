import matplotlib.pyplot as plt
from pymongo import MongoClient

# Function to draw a soccer field
def draw_soccer_field(ax):
    # Standard soccer field dimensions in meters
    field_length_m = 105
    field_width_m = 68

    # Scale factors
    field_length_px = 1050  # Fixed width in pixels
    field_width_px = int(field_length_px * (field_width_m / field_length_m))  # Maintain aspect ratio

    # Field position
    field_left = (1050 - field_length_px) / 2
    field_top = (680 - field_width_px) / 2

    # Drawing the field
    rect = plt.Rectangle((field_left, field_top), field_length_px, field_width_px, edgecolor='black', facecolor='none', lw=2)
    ax.add_patch(rect)

    # Scale for meters to pixels
    scale_x = field_length_px / field_length_m
    scale_y = field_width_px / field_width_m

    # Center Circle
    center_circle_radius_m = 9.15  # Standard center circle radius
    center_circle = plt.Circle((1050 / 2, 680 / 2), center_circle_radius_m * scale_x, color='black', fill=False, lw=2)
    ax.add_patch(center_circle)

    # Goal Areas (6-yard box)
    goal_area_length_m = 5.5
    goal_area_width_m = 18.32
    goal_area_left = plt.Rectangle((field_left, 680 / 2 - (goal_area_width_m * scale_y / 2)), 
                                   goal_area_length_m * scale_x, goal_area_width_m * scale_y, 
                                   edgecolor='black', facecolor='none', lw=2)
    goal_area_right = plt.Rectangle((1050 - field_left - goal_area_length_m * scale_x, 680 / 2 - (goal_area_width_m * scale_y / 2)), 
                                    goal_area_length_m * scale_x, goal_area_width_m * scale_y, 
                                    edgecolor='black', facecolor='none', lw=2)
    ax.add_patch(goal_area_left)
    ax.add_patch(goal_area_right)

    # Vertical Center Line
    plt.plot([1050 / 2, 1050 / 2], [field_top, field_top + field_width_px], color='black', lw=2)

# Function to fetch the latest player position data from MongoDB
def fetch_last_player_position():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["game_data"]  # Your actual database name
    collection = db["player_positions"]  # Collection name
    
    # Fetch the latest player position document
    player_data = collection.find_one(sort=[("_id", -1)])  # Sorting by _id as a proxy for the latest entry
    
    # Check if player_data is None
    if player_data is None:
        print("No data found in the collection.")
        return None  # Return None if no data is found
    
    return player_data  # Return the player data

# Main function to execute the fetching, printing, and plotting
def main():
    last_position = fetch_last_player_position()
    
    if last_position is not None:
        print("Last player position data:", last_position)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(1050 / 100, 680 / 100), dpi=100)  # Fixed size in inches
        
        # Draw the soccer field
        draw_soccer_field(ax)

        # Plot the last player position
        for player_number, position in last_position.items():
            if player_number != "_id":  # Exclude the _id field
                x = position['x']
                y = position['y']
                ax.scatter(x * (1050 / 105), y * (680 / 68), color='red', marker='o', s=100)  # Scale position
                print(f"Player {player_number}: (x: {x}, y: {y})")  # Print individual player positions

        plt.xlim(0, 1050)
        plt.ylim(0, 680)
        plt.gca().invert_yaxis()
        plt.title('Last Player Positions on Soccer Field', fontsize=24)
        ax.axis('off')
        plt.tight_layout()
        plt.show()
    else:
        print("Could not retrieve player positions.")

# Call the main function
if __name__ == "__main__":
    main()
