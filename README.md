# RMK Data Team Internship 2026: Probability Scale Challenge

## Overview
People intuitively understand physical distances (centimeters vs. kilometers), but often struggle to distinguish between probabilities like 0.04 and 0.4. This project aims to bridge that gap by creating an **intuitive probability scale** based on real-world Estonian data.

The project programmatically ingests data, cleans broken encodings, performs statistical calculations, and visualizes the results on a human-readable scale.

## Key Features
- **Programmatic Ingestion**: Automated data fetching from the Estonian Data Portal.
- **Robust Preprocessing**: Custom logic to fix Estonian broken encodings and cleaning of hierarchical artifacts (leading dots) common in official statistics.
- **Statistical Analysis**: Includes both national averages and **Bayesian updates** (calculating how location-specific context, like being in Saaremaa, shifts reforestation probabilities).
- **Aesthetic Visualization**: A color-coded probability scale categorized by data source, including "intuition zones" (Unlikely, Possible, Highly Likely).

## Project Structure
- `data/`: Contains raw CSV files and a `final_test/` folder with cleaned data.
- `src/`:
    - `fetcher.py`: Handles data ingestion from `avaandmed.eesti.ee`.
    - `csv_fixer.py`: Performs encoding fixes, Regex cleaning, and data reshaping.
    - `processor.py`: Calculates probabilities and performs Bayesian analysis.
    - `vizualizer.py`: Generates the final graphical output using `matplotlib`.
- `main.py`: Orchestrates the entire pipeline from start to finish.
- `output/`: Stores the final `probabilities.csv` and `probability_scale.png`.

## Data Sources
Data is sourced from the **Estonian Data Portal** and includes:
1. **Forest Management**: Reforestation methods (Planting vs. Sowing) — highly relevant to RMK operations.
2. **Ocean Fishing**: Catch statistics of the Estonian fleet (e.g., Atlantic Cod likelihood).
3. **Meat Consumption**: Social and dietary trends in Estonia (e.g., Pork consumption probability).

## How to Run
To reproduce the results, ensure you have Python 3.10+ installed and follow these steps:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the full pipeline:**
    ```bash
   python main.py
    ```
This will download data, clean it, calculate probabilities, and save the visualization.

## Results
The final output is a scale that helps users understand:

- **National Baseline**: The general probability of an event in Estonia.

- **Contextual Shift (Bayesian)**: How probabilities change (e.g., how much more likely reforestation is to be done by planting in Saaremaa compared to the national average).