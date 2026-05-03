import pandas as pd
import os


def calculate_probabilities():
    """
    Calculates specific probabilities from cleaned Estonian datasets.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_data_dir = os.path.join(base_dir, 'data', 'fixed_dataset')
    output_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    results = []

    # 1. MEAT (meat_fixed.csv)
    try:
        filename = 'meat_fixed.csv'
        df_meat = pd.read_csv(os.path.join(clean_data_dir, filename))
        latest_year = str(df_meat['Year'].max())
        latest_data = df_meat[df_meat['Year'].astype(str) == latest_year]

        pork_cons = latest_data[latest_data['Type of meat'] == 'Pork']['Human consumption, thousand tons'].values[0]
        total_cons = \
        latest_data[latest_data['Type of meat'] == 'Meat and offals total']['Human consumption, thousand tons'].values[
            0]

        results.append({
            'event': f'Consumed meat is Pork ({latest_year})',
            'probability': round(pork_cons / total_cons, 2),
            'source_file': filename
        })
    except Exception as e:
        print(f"Error processing meat: {e}")

    # 2. FISHING (fish_fixed.csv)
    try:
        filename = 'fish_fixed.csv'
        df_fish = pd.read_csv(os.path.join(clean_data_dir, filename))
        latest_year = str(df_fish['Year'].max())
        year_data = df_fish[df_fish['Year'].astype(str) == latest_year]

        total_catch = year_data[year_data.iloc[:, 0].str.contains('total', case=False)]['Catch_amount'].sum()
        cod_catch = year_data[year_data.iloc[:, 0].str.contains('Atlantic cod', case=False)]['Catch_amount'].sum()

        results.append({
            'event': f'Ocean fish is Atlantic Cod ({latest_year})',
            'probability': round(cod_catch / total_catch, 2) if total_catch > 0 else 0,
            'source_file': filename
        })
    except Exception as e:
        print(f"Error processing fish: {e}")

    # 3. FOREST (forest_fixed.csv)
    try:
        filename = 'forest_fixed.csv'
        df_forest = pd.read_csv(os.path.join(clean_data_dir, filename))
        latest_year = df_forest['Year'].max()
        forest_latest = df_forest[df_forest['Year'] == latest_year]

        # National
        total_all = forest_latest[forest_latest['County'] == 'Whole country']['Total'].values[0]
        plant_all = forest_latest[forest_latest['County'] == 'Whole country']['Planting'].values[0]

        # Bayesian context (Saaremaa)
        saare_total = forest_latest[forest_latest['County'].str.contains('Saare')]['Total'].values[0]
        saare_plant = forest_latest[forest_latest['County'].str.contains('Saare')]['Planting'].values[0]

        results.append({
            'event': 'Forest renewal method is Planting (Whole country)',
            'probability': round(plant_all / total_all, 2),
            'source_file': filename
        })
        results.append({
            'event': 'Forest renewal is Planting (Context: Saaremaa)',
            'probability': round(saare_plant / saare_total, 2),
            'source_file': filename
        })
    except Exception as e:
        print(f"Error processing forest: {e}")

    # Save summary
    summary_df = pd.DataFrame(results)
    summary_df.to_csv(os.path.join(output_dir, 'probabilities.csv'), index=False)
    print(f"Calculated {len(results)} events. Saved to output/probabilities.csv")


if __name__ == "__main__":
    calculate_probabilities()