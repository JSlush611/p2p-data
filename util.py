import matplotlib.pyplot as plt
import os
import argparse

def save_fig(fig, filename):
    media_folder = './graphs' 
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)  # Create the folder if it doesn't exist

    filepath = os.path.join(media_folder, filename)
    fig.savefig(filepath, bbox_inches='tight')
    plt.close(fig)

    print("Plot successfully saved as ", filename)


def clear_graphs(directory='./graphs'):
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")

        return
    
    # List all files in the directory
    files = os.listdir(directory)

    # Remove each file in the directory
    for file in files:
        file_path = os.path.join(directory, file)

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed file: {file_path}")

            else:
                print(f"Skipping non-file item: {file_path}")

        except Exception as e:
            print(f"Error removing file {file_path}: {e}")

    print(f"All files in {directory} have been removed.")


# Function to calculate the percentile of a value in a series
def calculate_percentile(series, value):
    rank = series.rank(pct=True).loc[series == value]
    if rank.empty:
        return None
    else:
        return rank.values[0] * 100
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility functions from util.py")
    
    parser.add_argument('function', choices=['clear_graphs'], 
                        help="The function you want to run (e.g., clear_graphs)")
    parser.add_argument('--directory', type=str, default='./graphs', 
                        help="The directory path for clear_graphs (default is ./graphs)")

    args = parser.parse_args()

    if args.function == 'clear_graphs':
        clear_graphs(args.directory)