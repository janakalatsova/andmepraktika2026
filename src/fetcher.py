import io
import json
import os

import pandas as pd
import requests


def fetch_to_pandas() -> None:
    """
    Fetches raw data from the Estonian Statistics API using local JSON queries.
    Saves results as raw CSV files in the data/ directory.
    """
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    project_root: str = os.path.dirname(current_dir)
    queries_dir: str = os.path.join(project_root, 'data', 'queries')
    output_dir: str = os.path.join(project_root, 'data')

    if not os.path.exists(queries_dir):
        print(f"Error: Folder {queries_dir} not found!")
        return

    base_url: str = "https://andmed.stat.ee/api/v1/en/stat/"

    for filename in os.listdir(queries_dir):
        if filename.endswith('.json'):
            query_path: str = os.path.join(queries_dir, filename)

            with open(query_path, 'r', encoding='utf-8') as f:
                query_data: dict = json.load(f)

            table_id: str = query_data["tableIdForQuery"].replace(".px", "")
            api_url: str = base_url + table_id

            print(f"Fetching {table_id}...")
            query_data['queryObj']['response']['format'] = 'csv'

            try:
                response: requests.Response = requests.post(
                    api_url,
                    json=query_data['queryObj'],
                    timeout=30
                )

                if response.status_code == 200:
                    df: pd.DataFrame = pd.read_csv(io.StringIO(response.text))
                    csv_filename: str = filename.replace("_query.json", ".csv")
                    df.to_csv(os.path.join(output_dir, csv_filename), index=False)
                    print(f"Saved {csv_filename}")
                else:
                    print(f"Error {response.status_code} for {table_id}")
            except Exception as e:
                print(f"Connection error for {table_id}: {e}")


if __name__ == "__main__":
    fetch_to_pandas()