import pandas as pd
import os
from typing import List, Dict, Any


def calculate_probabilities() -> None:
    """
    Analyzes cleaned datasets to derive probability metrics.
    Implements a simple Bayesian approach by comparing national priors
    to regional posterior context (Saaremaa).
    """
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_data_dir: str = os.path.join(base_dir, 'data', 'fixed_dataset')
    output_dir: str = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    results: List[Dict[str, Any]] = []

    # 1. MEAT CONSUMPTION
    try:
        df_meat: pd.DataFrame = pd.read_csv(os.path.join(clean_data_dir, 'meat_fixed.csv'))
        latest_year: str = str(df_meat['Year'].max())
        meat_data: pd.DataFrame = df_meat[df_meat['Year'].astype(str) == latest_year]

        pork: float = meat_data[meat_data['Type of meat'] == 'Pork']['Human consumption, thousand tons'].values[0]
        total: float = \
        meat_data[meat_data['Type of meat'] == 'Meat and offals total']['Human consumption, thousand tons'].values[0]

        results.append({
            'event': f'Consumed meat is Pork ({latest_year})',
            'probability': round(pork / total, 2),
            'source_file': 'meat_fixed.csv'
        })
    except Exception as e:
        print(f"Meat calculation failed: {e}")

    # 2. FISHING
    try:
        df_fish: pd.DataFrame = pd.read_csv(os.path.join(clean_data_dir, 'fish_fixed.csv'))
        latest_year = str(df_fish['Year'].max())
        fish_latest: pd.DataFrame = df_fish[df_fish['Year'].astype(str) == latest_year]

        total_catch: float = fish_latest[fish_latest.iloc[:, 0].str.contains('total', case=False)]['Catch_amount'].sum()
        cod_catch: float = fish_latest[fish_latest.iloc[:, 0].str.contains('Atlantic cod', case=False)][
            'Catch_amount'].sum()

        results.append({
            'event': f'Ocean fish is Atlantic Cod ({latest_year})',
            'probability': round(cod_catch / total_catch, 2),
            'source_file': 'fish_fixed.csv'
        })
    except Exception as e:
        print(f"Fish calculation failed: {e}")

    # 3. FOREST (Bayesian Reasoning)
    # P(Planting) = Prior (National)
    # P(Planting | Saaremaa) = Posterior (Evidence-based)
    try:
        df_for: pd.DataFrame = pd.read_csv(os.path.join(clean_data_dir, 'forest_fixed.csv'))
        latest_year = df_for['Year'].max()
        for_latest: pd.DataFrame = df_for[df_for['Year'] == latest_year]

        # Prior
        nat_total: float = for_latest[for_latest['County'] == 'Whole country']['Total'].values[0]
        nat_plant: float = for_latest[for_latest['County'] == 'Whole country']['Planting'].values[0]

        # Posterior
        saare_total: float = for_latest[for_latest['County'].str.contains('Saare')]['Total'].values[0]
        saare_plant: float = for_latest[for_latest['County'].str.contains('Saare')]['Planting'].values[0]

        results.append({
            'event': 'Forest renewal is Planting (National Prior)',
            'probability': round(nat_plant / nat_total, 2),
            'source_file': 'forest_fixed.csv'
        })
        results.append({
            'event': 'Forest renewal is Planting (Saaremaa Posterior)',
            'probability': round(saare_plant / saare_total, 2),
            'source_file': 'forest_fixed.csv'
        })
    except Exception as e:
        print(f"Forest calculation failed: {e}")

    # Final summary
    pd.DataFrame(results).to_csv(os.path.join(output_dir, 'probabilities.csv'), index=False)
    print("Probability calculations complete.")


if __name__ == "__main__":
    calculate_probabilities()