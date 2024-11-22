import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Load the dataset (adjust path if needed)
    names_2023_df = pd.read_csv('Data/names/yob2023.txt', header=None, names=['Name', 'Gender', 'Count'])

    # Set up Streamlit UI components
    st.title("2023 Names Dashboard")

    # Sidebar with inputs
    st.sidebar.title("Filters")
    gender_filter = st.sidebar.selectbox('Select Gender', options=['All', 'M', 'F'])
    top_n = st.sidebar.slider('Select Top N Names', min_value=1, max_value=50, value=10)
    
    # Fourth input widget: Checkbox to filter names by a minimum count
    filter_by_count = st.sidebar.checkbox('Filter by Minimum Count')
    count_threshold = 0
    if filter_by_count:
        count_threshold = st.sidebar.slider('Minimum Count for Name', min_value=1, max_value=5000, value=100)

    # Filter dataset based on sidebar inputs
    if gender_filter != 'All':
        names_2023_df = names_2023_df[names_2023_df['Gender'] == gender_filter]
    
    # Filtering based on top N names
    top_names_df = names_2023_df.nlargest(top_n, 'Count')
    
    # Apply the count threshold filter if enabled
    if filter_by_count:
        names_2023_df = names_2023_df[names_2023_df['Count'] >= count_threshold]

    # Tabs for organizing layout
    tab1, tab2 = st.tabs(["Top Names Overview", "Name Search"])

    with tab1:
        # Display filtered top names
        st.subheader(f"Top {top_n} Names in 2023")
        st.dataframe(top_names_df, use_container_width=True)

        # Plot a bar chart of top names by count
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x='Count', y='Name', data=top_names_df, ax=ax, palette='Blues_d')
        ax.set_title(f"Top {top_n} Names in 2023")
        st.pyplot(fig)

        # Show some basic statistics
        st.subheader("Statistics")
        total_names = len(names_2023_df)
        total_count = names_2023_df['Count'].sum()
        st.write(f"Total Names: {total_names}")
        st.write(f"Total Count: {total_count}")

        # Gender distribution plot
        st.subheader("Gender Distribution")
        gender_counts = names_2023_df['Gender'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        gender_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'], ax=ax)
        ax.set_title("Gender Distribution")
        st.pyplot(fig)

    with tab2:
        # Name Search functionality
        st.subheader("Search for a Name")
        name_input = st.text_input('Enter Name to Search', '')

        if name_input:
            search_result = names_2023_df[names_2023_df['Name'].str.contains(name_input, case=False)]
            if not search_result.empty:
                st.write(f"Found {len(search_result)} result(s) for '{name_input}'")
                st.dataframe(search_result, use_container_width=True)

                # Frequency bar chart for the searched name
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.barplot(x='Count', y='Name', data=search_result, ax=ax, palette='Set2')
                ax.set_title(f"Name Frequency for '{name_input}'")
                st.pyplot(fig)
            else:
                st.write(f"No results found for '{name_input}'")

    # Container for additional layout
    with st.container():
        st.markdown("""<hr>""", unsafe_allow_html=True)
        st.write("### Additional Information")
        st.write("This dashboard provides insights into the most popular names of 2023.")
        st.write("You can filter by gender, select the top N names, or search for a specific name.")
        st.write("The dashboard is built using **Streamlit**, and **Seaborn** for visualizations.")

        # Example of a footer using Markdown
        st.markdown("""
            <p style="text-align:center; color:gray;">
                Made with 💻 by Your Name | Data Source: SSA
            </p>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
