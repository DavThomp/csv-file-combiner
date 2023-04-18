import os
import pandas as pd


def combine_csv_files(directory, output_filename):
        
    files = []
    for filename in os.listdir(directory):
        files.append(os.path.basename(filename))

    csv_files = []
    for file in files:
        if file.endswith("csv"):
            csv_files.append(file)

    frames_concatenated = pd.DataFrame()
    for file in csv_files:
        try:
            frame = pd.read_csv(f"{directory}\{file}", index_col="key")
            frames_concatenated = pd.concat([frame, frames_concatenated])
        except ValueError:
            next
        except TypeError:
            next

    frames_concatenated.sort_index(inplace=True) 
    frames_concatenated.sort_index(axis=1, inplace=True)

    count_missing_values = frames_concatenated.isna().sum() 
    number_of_rows = len(frames_concatenated)
    proportions_missing = count_missing_values / number_of_rows

    # Work out which columns to keep
    columns_to_keep_boolean = proportions_missing <= 0.5
    columns_to_keep = frames_concatenated.columns[columns_to_keep_boolean]

    # Drop columns
    frames_concatenated = frames_concatenated.reindex(columns=columns_to_keep)

    # Save to csv file including header and index
    frames_concatenated.to_csv(f"{directory}\{output_filename}")
    


