import os
from src.csv_fixer import run as run_csv_fixer
from src.processor import calculate_probabilities
from src.vizualizer import create_visual

def main():
    print("Starting RMK Probability Scale Pipeline...")

    # Verification: Check if raw data files exist
    data_dir = "data"
    required_files = ["forest.csv", "fish.csv", "meat.csv"]
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(data_dir, f))]

    if missing_files:
        print(f"Error: The following files are missing in the 'data/' folder: {missing_files}")
        print("Please ensure your raw CSV files are placed in the 'data/' directory.")
        return

    # Step 1: Data Preprocessing
    print("\n[1/3] Step 1: Preprocessing and fixing encodings...")
    run_csv_fixer()

    # Step 2: Statistical Analysis
    print("\n[2/3] Step 2: Calculating probabilities and Bayesian context...")
    calculate_probabilities()

    # Step 3: Visualization
    print("\n[3/3] Step 3: Generating probability scale graphic...")
    create_visual()

    print("\n" + "="*50)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("Final Output: output/probability_scale.png")
    print("="*50)

if __name__ == "__main__":
    main()