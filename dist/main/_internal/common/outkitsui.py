import streamlit as st
import pandas as pd
import openpyxl

# Load the Excel files into DataFrames
file_paths = ['outputebay.xlsx', 'outputposhmark.xlsx', 'outputmercari.xlsx', 'outputdepop.xlsx']
dfs = [pd.read_excel(file_path) for file_path in file_paths]

# Combine the DataFrames into a single DataFrame
df = pd.concat(dfs, ignore_index=True).drop_duplicates()

# Convert 'Listing Date' to datetime if the column exists
if 'Listing Date' in df.columns:
    df['Listing Date'] = pd.to_datetime(df['Listing Date'], errors='coerce')

# Function to display images in the dataframe
def display_image(row):
    if pd.notna(row['Image']):
        return f'<img src="{row["Image"]}" width="100" height="100">'
    return 'No Image'

# Apply the display_image function to the Image column
if 'Image' in df.columns:
    df['Image'] = df.apply(display_image, axis=1)

# Function to make URLs clickable
def make_clickable(url):
    if pd.notna(url):
        return f'<a href="{url}" target="_blank">{url}</a>'
    return 'No URL'

# Apply the make_clickable function to the URL column
if 'URL' in df.columns:
    df['URL'] = df['URL'].apply(make_clickable)

# Custom CSS to control column width and height
st.markdown("""
    <style>
    .dataframe td {
        max-width: 200px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .dataframe th {
        max-width: 200px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .dataframe img {
        max-width: 100px;
        max-height: 100px;
    }
    </style>
    """, unsafe_allow_html=True)

# Create a Streamlit app
st.title('Outkits')

# Sidebar for filters and sorting
st.sidebar.header('Filter and Sort Options')

# Display filters and sort options for each column
filtered_df = df.copy()

# Filter by Name
if 'Name' in df.columns:
    keyword = st.sidebar.text_input(f'Enter keyword to filter by Name')
    if keyword:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(keyword, case=False, na=False)]

# Filter by Size
if 'Size' in df.columns:
    size_number = st.sidebar.text_input(f'Enter size number to filter by Size')
    if size_number:
        filtered_df = filtered_df[filtered_df['Size'].astype(str).str.contains(size_number, case=False, na=False)]

# Filter by Price
if 'Price' in df.columns:
    min_val = float(df['Price'].min())
    max_val = float(df['Price'].max())
    selected_range = st.sidebar.slider(f'Select range for Price', min_val, max_val, (min_val, max_val))
    filtered_df = filtered_df[
        (filtered_df['Price'] >= selected_range[0]) & (filtered_df['Price'] <= selected_range[1])]

# Filter by Listing Date
if 'Listing Date' in df.columns:
    min_date = df['Listing Date'].min().date()
    max_date = df['Listing Date'].max().date()
    start_date, end_date = st.sidebar.date_input(f'Select date range for Listing Date', [min_date, max_date])
    filtered_df = filtered_df[
        (filtered_df['Listing Date'] >= pd.to_datetime(start_date)) & (filtered_df['Listing Date'] <= pd.to_datetime(end_date))]

# Add sort options for specific columns
if 'Price' in df.columns:
    sort_price_option = st.sidebar.radio(f'Sort Price', ('None', 'Ascending', 'Descending'))
    if sort_price_option == 'Ascending':
        filtered_df = filtered_df.sort_values(by='Price', ascending=True)
    elif sort_price_option == 'Descending':
        filtered_df = filtered_df.sort_values(by='Price', ascending=False)

if 'Listing Date' in df.columns:
    sort_date_option = st.sidebar.radio(f'Sort Listing Date', ('None', 'Ascending', 'Descending'))
    if sort_date_option == 'Ascending':
        filtered_df = filtered_df.sort_values(by='Listing Date', ascending=True)
    elif sort_date_option == 'Descending':
        filtered_df = filtered_df.sort_values(by='Listing Date', ascending=False)

# Drop duplicates and reset index
filtered_df = filtered_df.drop_duplicates().reset_index(drop=True)

# Display the DataFrame directly
st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)

# Save the filtered DataFrame to an Excel file
filtered_df.to_excel("filtered_output.xlsx", index=False)

# Consolidate all DataFrames into one and save to "outputall.xlsx"
df.to_excel("outputall.xlsx", index=False)

# Open the workbook with openpyxl to adjust column width
wb_outputall = openpyxl.load_workbook("outputall.xlsx")
ws_outputall = wb_outputall.active

# Set the width of the "Name" column to twice the default width
default_width = 8.43  # Default width in Excel is 8.43
name_col_index = df.columns.get_loc('Name') + 1
name_col_letter = openpyxl.utils.get_column_letter(name_col_index)
ws_outputall.column_dimensions[name_col_letter].width = default_width * 2

# Save the "outputall" workbook with adjusted column width
wb_outputall.save("outputall.xlsx")
