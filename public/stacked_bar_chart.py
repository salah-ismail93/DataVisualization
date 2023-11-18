import os
import pandas as pd

# Directory where your CSV files are located
data_directory = 'C:/Users/salah.ismail/OneDrive - unige.it/3rd term/Data Visualization 2023-24/TreeDataset/'
output_data_directory = 'C:/Users/salah.ismail/OneDrive - unige.it/3rd term/Data Visualization 2023-24/Datavisualization/'

# Create a directory for the output CSV file
output_directory = os.path.join(output_data_directory, "public")
os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

# Initialize an empty dictionary to store the aggregated data
aggregated_data = {}

# List all CSV files in the directory
csv_files = [file for file in os.listdir(data_directory) if file.endswith(".csv")]

# Define the number of top tree species to consider
top_tree_count = 5

for csv_file in csv_files:
    print("Processing " + csv_file)

    # Load the data from the CSV file
    data = pd.read_csv(os.path.join(data_directory, csv_file), usecols=['state', 'city', 'common_name', 'scientific_name'])

    # Group the data by state, city, and common_name, and count the number of trees in each combination
    city_tree_count = data.groupby(['state', 'city', 'scientific_name']).size().reset_index(name="tree_count")

    # Sort the data in descending order based on tree_count
    sorted_city_tree_count = city_tree_count.sort_values(by=['state', 'city', 'tree_count'], ascending=[True, True, False])

    # Create a dictionary to store the top tree occurrences for each city
    city_data = {}

    for (state, city), group in sorted_city_tree_count.groupby(['state', 'city']):
        top_trees = group.head(top_tree_count)
        diff = pd.concat([group, top_trees]).drop_duplicates(keep=False)
        remaining_count = diff["tree_count"].sum()
       
        top_trees = pd.concat([top_trees, pd.DataFrame({"state":group['state'], "city":city, 'scientific_name': "Other",
                                                              "tree_count": remaining_count})]).drop_duplicates(keep='last')

        tree_counts = top_trees['tree_count'].tolist()
        city_data[(state, city)] = tree_counts

    # Add the city-specific data to the aggregated_data dictionary
    aggregated_data.update(city_data)

# Create a list to store the CSV data
csv_data = []

# Define column names for the CSV
column_names = ['state', 'city'] + [f'{row["scientific_name"]}' for index, row in top_trees.iterrows()] + ['total']

# Iterate through the aggregated data and format it for CSV
for (state, city), tree_counts in aggregated_data.items():
    total_count = sum(tree_counts)
    csv_row = [state, city] + tree_counts + [total_count]
    csv_data.append(csv_row)

# Create a DataFrame from the CSV data
csv_df = pd.DataFrame(csv_data, columns=column_names)

# Save the aggregated data to a CSV file
output_file = os.path.join(output_directory, "stacked_bar_chart.csv")
csv_df.to_csv(output_file, index=False)

print("CSV file saved:", output_file)
