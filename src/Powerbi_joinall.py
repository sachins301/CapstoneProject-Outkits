#This code combined all the xlsx into one in power bi "Pythin scripts" - 07/10/24 - AR
import pandas as pd

# Load the data from the uploaded Excel files
file1 = "Add_path_here/outputposhmark.xlsx" #"Add_path_here" is can be delete and add the path where the file is located
file2 = "Add_path_here/outputmercari.xlsx"  #"Add_path_here" is can be delete and add the path where the file is located
file3 = "Add_path_here/outputebay.xlsx"  #"Add_path_here" is can be delete and add the path where the file is located
file4 = "Add_path_here/outputdepop.xlsx"  #"Add_path_here" is can be delete and add the path where the file is located

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
