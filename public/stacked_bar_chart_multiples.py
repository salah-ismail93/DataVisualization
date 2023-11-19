import os
import pandas as pd

# Constants
TOP_TREE_COUNT = 5

def generate_top_trees_for_city(city_group):
    """Generate top trees for each city."""
    top_trees = city_group.head(TOP_TREE_COUNT)
    remaining_trees = pd.concat([city_group, top_trees]).drop_duplicates(keep=False)
    remaining_count = remaining_trees["tree_count"].sum()

    other_species = pd.DataFrame({
        "state": city_group['state'],
        "city": city_group['city'],
        'scientific_name': "Other",
        "tree_count": remaining_count
    }).drop_duplicates(keep='last')

    top_trees = pd.concat([top_trees, other_species])
    return top_trees

def main():
    # Directory where your CSV files are located
    data_directory = 'C:/Users/salah.ismail/OneDrive - unige.it/3rd term/Data Visualization 2023-24/TreeDataset/'
    output_data_directory = 'C:/Users/salah.ismail/OneDrive - unige.it/3rd term/Data Visualization 2023-24/Datavisualization/'

    # Output directory
    output_directory = os.path.join(output_data_directory, "public")
    os.makedirs(output_directory, exist_ok=True)

    # Aggregated data dictionary
    aggregated_data = {}

    # List all CSV files in the directory
    csv_files = [file for file in os.listdir(data_directory) if file.endswith(".csv")]

    for csv_file in csv_files:
        print("Processing " + csv_file)

        # Load data from CSV file
        data = pd.read_csv(os.path.join(data_directory, csv_file), usecols=['state', 'city', 'common_name', 'scientific_name'])

        # Group data and count tree occurrences
        city_tree_count = data.groupby(['state', 'city', 'scientific_name']).size().reset_index(name="tree_count")

        # Sort data based on tree_count
        sorted_city_tree_count = city_tree_count.sort_values(by=['state', 'city', 'tree_count'], ascending=[True, True, False])

        # Process each city's data
        for (state, city), group in sorted_city_tree_count.groupby(['state', 'city']):
            top_trees = generate_top_trees_for_city(group)
            tree_counts = top_trees['tree_count'].tolist()
            aggregated_data[(state, city)] = tree_counts

    # Create a DataFrame from the aggregated data
    column_names = ['city', 'state', 'scientific_name', 'tree_count']
    csv_data = [[city, state, scientific_name, tree_count] for (state, city), tree_counts in aggregated_data.items() for scientific_name, tree_count in zip(top_trees['scientific_name'], tree_counts)]
    csv_df = pd.DataFrame(csv_data, columns=column_names)

    # Filter cities with at least one of each of the top 5 species
    filtered_df = csv_df.groupby(['city', 'state']).filter(lambda x: x['scientific_name'].nunique() >= TOP_TREE_COUNT)

    # Save the aggregated data to a CSV file
    output_file = os.path.join(output_directory, "stacked_bar_chart_multiples.csv")
    filtered_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
