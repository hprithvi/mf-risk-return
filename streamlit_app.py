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
        x='annualized_mean_std',
        y='annualized_median_return',
        hover_data=['scheme_name'],
        title='Risk vs Returns Analysis'
    )
    fig.update_traces(marker_size=4)
    fig.update_layout(scattergap=1)
    
    # Highlight selected scheme if any
    if selected_scheme:
        selected_data = df[df['scheme_name'] == selected_scheme]
        fig.add_scatter(
            x=selected_data['annualized_mean_std'],
            y=selected_data['annualized_median_return'],
            mode='markers',
            marker=dict(size=12, color='red'),
            name='Selected Scheme',
            hovertext=selected_data['scheme_name']
        )

    
    # Display the plot
    st.plotly_chart(fig)
    
    # Display the data table
    st.write("Data Table:")
    st.dataframe(df)

# If a scheme is selected, show similar risk funds
if selected_scheme:
    st.write("\n Top 5 Funds best returns and Similar Risk Profile:")
    # st.write("risk and returns {0}, {1}")        
    # Get the risk of selected scheme
    selected_risk = df['annualized_mean_std'].values[0]
            
            # Filter funds within 0.5% risk range and sort by returns
    risk_range = 0.5
    similar_risk_funds = df[
    (df['annualized_mean_std'] >= selected_risk - risk_range) & 
    (df['annualized_mean_std'] <= selected_risk + risk_range)
            ].sort_values('annualized_median_return', ascending=False).head(5)
            
            # Display the similar funds in a table
    st.dataframe(similar_risk_funds[['scheme_name', 'annualized_median_return', 'annualized_mean_std']].style.format({
                'returns': '{:.2f}%',
                'risk': '{:.2f}%'
            }))


    st.write("\n 5 Funds with Similar Returns Profile and lower risk:")
            
    # Get the risk of selected scheme
    selected_return = df['annualized_median_return'].values[0]
            
    # Filter funds within 0.5% risk range and sort by returns
    return_range = 0.25
    similar_risk_funds = df[
    (df['annualized_median_return'] >= selected_risk - risk_range) & 
    (df['annualized_median_return'] <= selected_risk + risk_range)
            ].sort_values('annualized_mean_std', ascending=False).tail(5)
            
    # Display the similar funds in a table
    st.dataframe(similar_risk_funds[['scheme_name', 'annualized_median_return', 'annualized_mean_std']].style.format({
                'returns': '{:.2f}%',
                'risk': '{:.2f}%'
            }))
    