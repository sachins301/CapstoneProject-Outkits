# import streamlit as st
# import pandas as pd
#
# # Load the Excel file
# file_paths = ['outputebay.xlsx', 'outputposhmark.xlsx', 'outputmercari.xlsx', 'outputdepop.xlsx']
#
# # Read the Excel files into DataFrames
# dfs = [pd.read_excel(file_path) for file_path in file_paths]
#
# # Combine the DataFrames into a single DataFrame
# df = pd.concat(dfs, ignore_index=True).drop_duplicates(subset=dfs[0].columns.difference(['index']))
#
# if 'Listing Date' in df.columns:
#     df['Listing Date'] = pd.to_datetime(df['Listing Date'], errors='coerce')
#
#
# # Function to display images in the dataframe
# def display_image(row):
#     if pd.notna(row['Image']):
#         return f'<img src="{row["Image"]}" width="100" height="100">'
#     return 'No Image'
#
#
# # Apply the display_image function to the Image column
# df['Image'] = df.apply(display_image, axis=1)
#
#
# # Function to make URLs clickable
# def make_clickable(url):
#     if pd.notna(url):
#         return f'<a href="{url}" target="_blank">{url}</a>'
#     return 'No URL'
#
#
# # Apply the make_clickable function to the URL column
# if 'URL' in df.columns:
#     df['URL'] = df['URL'].apply(make_clickable)
#
# # Custom CSS to control column width and height
# st.markdown("""
#     <style>
#     .dataframe td {
#         max-width: 200px;
#         overflow: hidden;
#         text-overflow: ellipsis;
#         white-space: nowrap;
#     }
#     .dataframe th {
#         max-width: 200px;
#         overflow: hidden;
#         text-overflow: ellipsis;
#         white-space: nowrap;
#     }
#     .dataframe img {
#         max-width: 100px;
#         max-height: 100px;
#     }
#     </style>
#     """, unsafe_allow_html=True)
#
# # Create a Streamlit app
# st.title('Outkits')
#
# # Sidebar for filters and sorting
# st.sidebar.header('Filter and Sort Options')
#
# # Display filters and sort options for each column
# filtered_df = df.copy()
#
# for column in df.columns:
#     if column != 'Image':  # Skip image column for filtering
#         if column == 'Name':  # Custom keyword filter for the 'Name' column
#             keyword = st.sidebar.text_input(f'Enter keyword to filter {column}')
#             if keyword:
#                 filtered_df = filtered_df[filtered_df[column].str.contains(keyword, case=False, na=False)]
#         elif column == 'Price':
#             min_val = float(df[column].min())
#             max_val = float(df[column].max())
#             selected_range = st.sidebar.slider(f'Select range for {column}', min_val, max_val, (min_val, max_val))
#             filtered_df = filtered_df[
#                 (filtered_df[column] >= selected_range[0]) & (filtered_df[column] <= selected_range[1])]
#         elif column == 'Listing Date':
#             min_date = df[column].min().date()
#             max_date = df[column].max().date()
#             start_date, end_date = st.sidebar.date_input(f'Select date range for {column}', [min_date, max_date])
#             filtered_df = filtered_df[
#                 (filtered_df[column] >= pd.to_datetime(start_date)) & (filtered_df[column] <= pd.to_datetime(end_date))]
#
#         # Add sort options for specific columns
#         if column == "Price":
#             sort_price_option = st.sidebar.radio(f'Sort {column}', ('None', 'Ascending', 'Descending'))
#             if sort_price_option == 'Ascending':
#                 filtered_df = filtered_df.sort_values(by=column, ascending=True)
#             elif sort_price_option == 'Descending':
#                 filtered_df = filtered_df.sort_values(by=column, ascending=False)
#
#         if column == "Listing Date":
#             sort_date_option = st.sidebar.radio(f'Sort {column}', ('None', 'Ascending', 'Descending'))
#             if sort_date_option == 'Ascending':
#                 filtered_df = filtered_df.sort_values(by=column, ascending=True)
#             elif sort_date_option == 'Descending':
#                 filtered_df = filtered_df.sort_values(by=column, ascending=False)
#
# filtered_df = filtered_df.drop_duplicates(subset=df.columns.difference(['index'])).reset_index(drop=True)
# # Display the dataframe
# st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)
