import pandas as pd
import os
import glob

def combine_datasets(folder_path, year):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        raise ValueError(f"The folder path '{folder_path}' does not exist.")
    
    # Search for files in the specified folder
    file_paths = glob.glob(os.path.join(folder_path, "*"))

    # Debug print to check file paths
    print(f"Found {len(file_paths)} files in {folder_path}")
    for file in file_paths:
        print(file)

    if not file_paths:
        raise ValueError("No files found in the specified folder.")

    # Read the files as CSVs
    dataframes = []
    for file in file_paths:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
        except Exception as e:
            print(f"Could not read {file} as CSV. Error: {e}")

    if not dataframes:
        raise ValueError("No valid CSV files found in the specified folder.")

    # Combine all datasets
    combined_df = pd.concat(dataframes)

    # Trim leading and trailing spaces from column names if needed
    combined_df.columns = combined_df.columns.str.strip()

    # Convert the 'valid' column to datetime for sorting
    combined_df['date time'] = pd.to_datetime(combined_df['valid'])
    combined_df = combined_df.sort_values(by='date time')

    # Save to Excel and CSV in the same folder as the input files
    output_excel = os.path.join(folder_path, f"skocjan_combined_{year}.xlsx")
    output_csv = os.path.join(folder_path, f"skocjan_combined_{year}.csv")

    combined_df.to_excel(output_excel, index=False)
    combined_df.to_csv(output_csv, index=False)

    return output_excel, output_csv

folder_path = "C:/Users/samuel/Desktop/ARSO/Skocjan"
combine_datasets(folder_path, 2024)