import pandas as pd
import requests
import json
import os
import io


def fetch_to_pandas():
    """This method converses JSON data to pandas dataframe."""
    # This gets the directory where fetcher.py is located (src/)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # This goes one level up to the project root
    project_root = os.path.dirname(current_dir)

    # Now we define paths relative to the project root
    queries_dir = os.path.join(project_root, 'data', 'queries')
    output_dir = os.path.join(project_root, 'data')

    # Print for debugging to see where it's looking
    print(f"Looking for queries in: {queries_dir}")

    # If folder in not found, it prints error
    if not os.path.exists(queries_dir):
        print(f"Error: Folder {queries_dir} not found!")
        return

    base_url = "https://andmed.stat.ee/api/v1/en/stat/"

    # Get all JSON files
    for filename in os.listdir(queries_dir):
        if filename.endswith('.json'):
            # Load the query
            query_path = os.path.join(queries_dir, filename)
            with open(query_path, 'r') as f:
                query_data = json.load(f)

            table_id = query_data["tableIdForQuery"].replace(".px", "")
            api_url = base_url + table_id

            print(f"Fetching {table_id}...")

            # Requesting CSV format
            query_data['queryObj']['response']['format'] = 'csv'

            try:
                response = requests.post(api_url, json=query_data['queryObj'], timeout=30)

                if response.status_code == 200:
                    df = pd.read_csv(io.StringIO(response.text))
                    csv_filename = filename.replace("_query.json", ".csv")
                    df.to_csv(os.path.join(output_dir, csv_filename), index=False)
                    print(f"Success! Saved {csv_filename}")
                else:
                    print(f"Error {response.status_code} for {table_id}")
            except Exception as e:
                print(f"Connection error for {table_id}: {e}")


if __name__ == "__main__":
    fetch_to_pandas()