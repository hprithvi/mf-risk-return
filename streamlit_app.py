import streamlit as st
import pandas as pd

import plotly.express as px

st.title("Mutual Fund Risk vs Returns Analysis")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Search box for scheme selection
    search_term = st.text_input("Search for a scheme:")
    
    # Filter schemes based on search
    if search_term:
        filtered_df = df[df['scheme_name'].str.contains(search_term, case=False, na=False)]
        selected_scheme = st.selectbox(
            "Select a scheme:",
            filtered_df['scheme_name'].tolist()
        )
    else:
        selected_scheme = None
    
    # Create scatter plot
    fig = px.scatter(
        df,
        x='daily_std',
        y='daily_mean',
        hover_data=['scheme_name'],
        title='Risk vs Returns Analysis'
    )
    
    # Highlight selected scheme if any
    if selected_scheme:
        selected_data = df[df['scheme_name'] == selected_scheme]
        fig.add_scatter(
            x=selected_data['daily_std'],
            y=selected_data['daily_mean'],
            mode='markers',
            marker=dict(size=25, color='red'),
            name='Selected Scheme',
            hovertext=selected_data['scheme_name']
        )
    
    # Display the plot
    st.plotly_chart(fig)
    
    # Display the data table
    st.write("Data Table:")
    st.dataframe(df)