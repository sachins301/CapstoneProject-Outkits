import streamlit as st
import pandas as pd

# Load the Excel file
file_path = 'outputebay.xlsx'
df = pd.read_excel(file_path)

if 'Listing Date' in df.columns:
    df['Listing Date'] = pd.to_datetime(df['Listing Date'], errors='coerce')


# Function to display images in the dataframe
def display_image(row):
    if pd.notna(row['Image']):
        return f'<img src="{row["Image"]}" width="100" height="100">'
    return 'No Image'


# Apply the display_image function to the Image column
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

for column in df.columns:
    if column != 'Image':  # Skip image column for filtering
        if column == 'Name':  # Custom keyword filter for the 'Name' column
            keyword = st.sidebar.text_input(f'Enter keyword to filter {column}')
            if keyword:
                filtered_df = filtered_df[filtered_df[column].str.contains(keyword, case=False, na=False)]
        elif column == 'Price':
            min_val = float(df[column].min())
            max_val = float(df[column].max())
            selected_range = st.sidebar.slider(f'Select range for {column}', min_val, max_val, (min_val, max_val))
            filtered_df = filtered_df[
                (filtered_df[column] >= selected_range[0]) & (filtered_df[column] <= selected_range[1])]
        elif column == 'Listing Date':
            min_date = df[column].min().date()
            max_date = df[column].max().date()
            start_date, end_date = st.sidebar.date_input(f'Select date range for {column}', [min_date, max_date])
            filtered_df = filtered_df[
                (filtered_df[column] >= pd.to_datetime(start_date)) & (filtered_df[column] <= pd.to_datetime(end_date))]


        # Add sort options
        if column == "Price" or column == "Listing Date":
            sort_ascending = st.sidebar.checkbox(f'Sort {column} ascending', value=True)
            filtered_df = filtered_df.sort_values(by=column, ascending=sort_ascending)

# Display the dataframe
st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)
