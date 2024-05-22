import pandas as pd
import sys

# Example DataFrame

# print(data)


import pandas as pd
from pandas import DataFrame

def split_combined_column(data: DataFrame, combined_column_name: str, column1_name: str = 'column1', column2_name: str = 'column2') -> DataFrame:
    """
    Split a combined column into two separate columns.
    
    Parameters:
    data: DataFrame, The DataFrame containing the combined column.
    combined_column_name: str, The name of the combined column to split.
    column1_name: str, optional, The name of the first resulting column.
    column2_name: str, optional, The name of the second resulting column.
    
    Returns:
    DataFrame: The DataFrame with the combined column split into two separate columns.
    """
    # Extracting values from the combined column into separate columns
    data[[column1_name, column2_name]] = data[combined_column_name].str.extract(r"\((.*?), (.*?)\)")

    # Dropping the original combined column
    data = data.drop(columns=[combined_column_name])

    return data

# Example usage:
# Load your dataset using pandas
# data = pd.read_csv("your_dataset.csv")

# Apply the function to split the combined column
# data = split_combined_column(data, 'detailed_description', 'column1', 'column2')

# print(data[['column1', 'column2']])


# Example usage:
# Load your dataset using pandas
data = pd.read_csv("training_data.csv")

# Apply the function to split the combined column
data = split_combined_column(data, 'detailed_description', 'label', 'label_reason')
data.to_csv("training_data1.csv", index = False)


# print(data[['column1', 'column2']])


