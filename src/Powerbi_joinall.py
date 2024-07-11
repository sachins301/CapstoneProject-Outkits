
import pandas as pd

# Load the data from the uploaded Excel files
file1 = "E:\IS 6495-001\pythonProject/Carhartt Hooded Jacket Orange.xlsx"
file2 = "E:\IS 6495-001\pythonProject/Carhartt Hooded Jacket Purple.xlsx"
file3 = "E:\IS 6495-001\pythonProject/Carhartt Hooded Jacket Red.xlsx"
file4 = "E:\IS 6495-001\pythonProject/Carhartt Hooded Jacket Teal.xlsx"

# Read the Excel files into DataFrames
df1 = pd.read_excel(file1, sheet_name=None)
df2 = pd.read_excel(file2, sheet_name=None)
df3 = pd.read_excel(file3, sheet_name=None)
df4 = pd.read_excel(file4, sheet_name=None)

# Combine all sheets from each file into separate DataFrames
combined_df1 = pd.concat(df1.values(), ignore_index=True)
combined_df2 = pd.concat(df2.values(), ignore_index=True)
combined_df3 = pd.concat(df3.values(), ignore_index=True)
combined_df4 = pd.concat(df4.values(), ignore_index=True)

# Combine all DataFrames into one
combined_data = pd.concat([combined_df1, combined_df2, combined_df3, combined_df4], ignore_index=True)

# Display the combined DataFrame
print(combined_data)