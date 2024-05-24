import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import os

def visualizer(file_path, output_image_path):
    # Read the file and process the grid
    with open(file_path, 'r') as f:
        grid = [line.strip().split() for line in f]

    # Path to the images directory
    path_to_images = 'images/'

    # Create a matplotlib figure and axis for each image in the grid
    fig, axs = plt.subplots(len(grid), len(grid[0]), figsize=(15, 15))

    # Adjust spacing between subplots
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    # Remove axis for each subplot
    for ax in axs.flatten():
        ax.axis('off')

    # Load and display each image in the grid
    for i, row in enumerate(grid):
        for j, img_code in enumerate(row):
            img_path = f"{path_to_images}{img_code}.png"
            try:
                img = mpimg.imread(img_path)
                axs[i, j].imshow(img)
            except FileNotFoundError:
                print(f"Image not found: {img_path}")
                axs[i, j].text(0.5, 0.5, 'Image\nNot Found', ha='center', va='center', color='red')

    # Save the grid of images to a file
    plt.savefig(output_image_path)
    print(f"Grid image saved to {output_image_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python visualizer.py <file_path> <output_image_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_image_path = sys.argv[2]
    visualizer(file_path, output_image_path)
