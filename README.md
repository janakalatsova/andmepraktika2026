# RMK Probability Scale Challenge 2026

## Overview
People intuitively understand physical distances (centimeters vs. kilometers), but often struggle to distinguish between probabilities like 0.04 and 0.4. This project aims to bridge that gap by creating an intuitive probability scale based on real-world Estonian data.

The project programmatically ingests data, cleans broken encodings, performs statistical calculations, and visualizes the results on a human-readable scale.


## Thought Process & Challenges
### 1. Data Selection
I chose three distinct areas to provide a diverse scale:
- **Forestry (RMK Focus)**: Essential to understand reforestation methods.
- **Ocean Fishing**: Represents large-scale industrial output.
- **Meat Consumption**: A relatable social metric.

### 2. The Encoding Battle (Biggest Technical Challenge)
The raw data from the Estonian Data Portal often uses hierarchical dot notation (e.g., `..loss`) and broken encodings (UTF-8 interpreted as Latin-1, resulting in `Ćµ`). 
- **Solution**: Instead of manual cleanup, I implemented a robust `csv_fixer.py` using **Regular Expressions** to strip artifacts and a dictionary-based mapping to restore Estonian vowels. This ensures the pipeline is fully reproducible with any new data from the portal.

### 3. Bayesian Reasoning
To go beyond simple averages, I applied a Bayesian logic to the Forest dataset. We look at the **Prior** probability of planting a forest nationally and update it to a **Posterior** probability when we add the context of a specific region (Saaremaa). This highlights how evidence shifts likelihood.

## Project Structure
- `data/queries/`: JSON API query objects.
- `data/fixed_dataset/`: Cleaned, Tidy-formatted CSVs.
- `src/fetcher.py`: API ingestion logic.
- `src/csv_fixer.py`: Regex cleaning and reshaping.
- `src/processor.py`: Statistical math (Bayesian).
- `src/vizualizer.py`: Matplotlib plotting.
- `main.py`: Full pipeline orchestrator.

## AI Usage Disclosure
I utilized AI (Gemini) as a specialized pair-programmer for:
1. **Regular Expressions**: Designing the `re.sub` patterns to clean leading dots without breaking decimal values.
2. **Refactoring**: Applying PEP8 standards and Type Hints to ensure professional code quality.
3. **Visualization**: Fine-tuning the Matplotlib aesthetics (z-order and intuition zones).
*The core logic, data selection, and architectural decisions were driven by human input.*

## How to Run
1. `pip install -r requirements.txt`
2. `python main.py`

## Final Scale Preview
The resulting `output/probability_scale.png` categorizes events into **Unlikely**, **Possible**, and **Highly Likely**, providing a clear intuitive benchmark.
