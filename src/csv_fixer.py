import re
import pandas as pd
import os
from io import StringIO
from typing import Union, Any


def fix_estonian_encoding(text: Any) -> Any:
    """
    Fixes common UTF-8 to Latin-1 double-encoding issues for Estonian characters.

    Args:
        text: The input string potentially containing broken characters.
    Returns:
        The cleaned string with correct Estonian vowels.
    """
    if not isinstance(text, str):
        return text
    replacements = {
        'Ćµ': 'õ', 'Ć¤': 'ä', 'Ć¶': 'ö', 'Ć¼': 'ü',
        'ļ»æ': '', 'Ć•': 'Õ', 'Ć„': 'Ä', 'Ć–': 'Ö', 'Ćœ': 'Ü',
        'õ¤': 'ä', 'õµ': 'õ', 'õ¶': 'ö', 'õ¼': 'ü'
    }
    for broken, correct in replacements.items():
        text = text.replace(broken, correct)
    return text


def value_clean(value: Any) -> Any:
    """
    Normalizes textual values for the probability scale.
    Removes leading dots/spaces and standardizes case format.

    Args:
        value: Any data point (string or numeric).
    Returns:
        Cleaned string if input was string, else original value.
    """
    if not isinstance(value, str):
        return value

    text = fix_estonian_encoding(value)
    text = text.replace('"', '').replace("'", "").replace('\ufeff', '')

    # Regex: Remove all leading dots and whitespaces from the start of the string
    text = re.sub(r'^[.\s]+', '', text)

    if len(text) > 0:
        text = text[0].upper() + text[1:]

    return text.strip()


def reshape_meat_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms Meat data from wide format to long format (Tidy Data principles).

    Args:
        df: Raw DataFrame with years as columns.
    Returns:
        Reshaped DataFrame suitable for statistical analysis.
    """
    year_cols = [col for col in df.columns if col.isdigit()]
    id_cols = [col for col in df.columns if not col.isdigit()]
    if not year_cols:
        return df

    df_long = df.melt(id_vars=id_cols, value_vars=year_cols, var_name='Year', value_name='Value')

    # Identify primary columns for pivoting
    meat_col = df.columns[0]
    ind_col = df.columns[1] if len(df.columns) > 1 else id_cols[0]

    df_pivoted = df_long.pivot_table(
        index=[meat_col, 'Year'],
        columns=ind_col,
        values='Value',
        aggfunc='first'
    ).reset_index()

    df_pivoted.columns.name = None
    return df_pivoted


def reshape_fish_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reshapes fishing stats into a consistent time-series format.
    """
    year_cols = [col for col in df.columns if col.isdigit()]
    species_col = df.columns[0]
    if not year_cols:
        return df

    df_reshaped = df.melt(id_vars=[species_col], value_vars=year_cols,
                          var_name='Year', value_name='Catch_amount')
    return df_reshaped


def process_file(input_path: str, output_path: str) -> None:
    """
    Full pipeline for a single CSV file: Load -> Clean -> Reshape -> Save.
    """
    try:
        print(f"--- Processing: {os.path.basename(input_path)} ---")

        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Load with automatic separator detection
        df = pd.read_csv(StringIO(fix_estonian_encoding(content)), sep=None, engine='python')

        # 1. Header Cleaning
        new_columns = []
        for col in df.columns:
            c_str = str(col)
            year_match = re.search(r'(\d{4})', c_str)
            if year_match:
                new_columns.append(year_match.group(1))
            else:
                new_columns.append(value_clean(c_str))
        df.columns = new_columns

        # 2. Cell Cleaning
        try:
            df = df.map(value_clean)
        except AttributeError:
            df = df.applymap(value_clean)

        # 3. Safe Numeric Conversion
        text_id_cols = ['Indicator', 'Species', 'Type of meat', 'County', 'Year']
        for col in df.columns:
            if col in text_id_cols:
                continue

            try:
                numeric_col = pd.to_numeric(df[col], errors='coerce')
                if not numeric_col.isna().all():
                    df[col] = numeric_col.fillna(0)
            except Exception:
                pass

        # 4. Domain-Specific Reshaping
        fname = os.path.basename(input_path).lower()
        if 'meat' in fname:
            df = reshape_meat_data(df)
        elif 'fish' in fname:
            df = reshape_fish_data(df)

        # Final Save
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Success: {os.path.basename(output_path)}")

    except Exception as e:
        print(f"Error in {os.path.basename(input_path)}: {e}")


def run() -> None:
    """
    Main entry point for batch processing all CSV files in the data directory.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_folder = os.path.join(project_root, 'data')
    output_folder = os.path.join(input_folder, 'fixed_dataset')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for f in os.listdir(input_folder):
        # Prevent processing already fixed files or non-csv files
        if f.endswith('.csv') and '_fixed' not in f and 'fixed_dataset' not in f:
            process_file(
                os.path.join(input_folder, f),
                os.path.join(output_folder, f.replace('.csv', '_fixed.csv'))
            )


if __name__ == "__main__":
    run()