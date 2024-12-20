import streamlit as st
import pandas as pd
#conda install plotly
import plotly.express as px

# st.title("Mutual Fund Risk vs Returns Analysis")

# # File upload
# uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

# if uploaded_file is not None:
#     # Read the CSV file
#     df = pd.read_csv(uploaded_file)
    
#     # Search box for scheme selection
#     search_term = st.text_input("Search for a scheme:")
    
#     # Filter schemes based on search
#     if search_term:
#         filtered_df = df[df['scheme_name'].str.contains(search_term, case=False, na=False)]
#         selected_scheme = st.selectbox(
#             "Select a scheme:",
#             filtered_df['scheme_name'].tolist()
#         )
#     else:
#         selected_scheme = None
    
#     # Create scatter plot
#     fig = px.scatter( 
#         df,
#         x='annualized_mean_std',
#         y='annualized_median_return',
#         hover_data=['scheme_name'],
#         title='Risk vs Returns Analysis'
#     )
#     fig.update_traces(marker_size=4)
#     fig.update_layout(scattergap=1)
    
#     # Highlight selected scheme if any
#     if selected_scheme:
#         selected_data = df[df['scheme_name'] == selected_scheme]
#         fig.add_scatter(
#             x=selected_data['annualized_mean_std'],
#             y=selected_data['annualized_median_return'],
#             mode='markers',
#             marker=dict(size=12, color='red'),
#             name='Selected Scheme',
#             hovertext=selected_data['scheme_name']
#         )

    
#     # Display the plot
#     st.plotly_chart(fig)
    
#     # Display the data table
#     st.write("Data Table:")
#     st.dataframe(df)

# # If a scheme is selected, show similar risk funds
# if selected_scheme:
#     st.write("\n Top 5 Funds best returns and Similar Risk Profile:")
#     # st.write("risk and returns {0}, {1}")        
#     # Get the risk of selected scheme
#     selected_risk = df['annualized_mean_std'].values[0]
            
#             # Filter funds within 0.5% risk range and sort by returns
#     risk_range = 0.5
#     similar_risk_funds = df[
#     (df['annualized_mean_std'] >= selected_risk - risk_range) & 
#     (df['annualized_mean_std'] <= selected_risk + risk_range)
#             ].sort_values('annualized_median_return', ascending=False).head(5)
            
#             # Display the similar funds in a table
#     st.dataframe(similar_risk_funds[['scheme_name', 'annualized_median_return', 'annualized_mean_std']].style.format({
#                 'returns': '{:.2f}%',
#                 'risk': '{:.2f}%'
#             }))


#     st.write("\n 5 Funds with Similar Returns Profile and lower risk:")
            
#     # Get the risk of selected scheme
#     selected_return = df['annualized_median_return'].values[0]
            
#     # Filter funds within 0.5% risk range and sort by returns
#     return_range = 0.25
#     similar_risk_funds = df[
#     (df['annualized_median_return'] >= selected_risk - risk_range) & 
#     (df['annualized_median_return'] <= selected_risk + risk_range)
#             ].sort_values('annualized_mean_std', ascending=False).tail(5)
            
#     # Display the similar funds in a table
#     st.dataframe(similar_risk_funds[['scheme_name', 'annualized_median_return', 'annualized_mean_std']].style.format({
#                 'returns': '{:.2f}%',
#                 'risk': '{:.2f}%'
#             }))
    
from pathlib import Path

def setup_page():
        """Configure the Streamlit page settings"""
        st.set_page_config(
            page_title="MF Analysis Dashboard",
            page_icon="📈",
            layout="wide"
        )
        st.title("MF Analysis Dashboard")

setup_page()

def load_data_from_drive():
        """
        Load data from a specific directory on drive.
        Supports multiple file formats (csv, excel, parquet).
        """
        # Define the data directory - update this path to your data location
        data_file = "data/scheme_stats_MC_atleast_3_yrs.csv"  # Update this path
        
        try:
            # Look for data files in the specified directory
            # data_file = list(Path(DATA_DIR).glob("*.csv"))  # For CSV files
            data = pd.read_csv(data_file)
            return data
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.stop()

df = load_data_from_drive()


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
    selected_scheme_risk = float(df.loc[df['scheme_name']==selected_scheme]['annualized_mean_std'])
    selected_scheme_returns = float(df.loc[df['scheme_name']==selected_scheme]['annualized_median_return'])

    st.write("Annualized median Returns of", selected_scheme,":", round(selected_scheme_returns, 2))
    st.write("Annualized Risk of", selected_scheme,":", round(selected_scheme_risk,2))
    st.write("\n Top 5 Funds best returns and Similar Risk Profile (within 0.5%):")
    # st.write("risk and returns {0}, {1}")        
    # Get the risk of selected scheme
    # selected_risk = df['annualized_mean_std'].values[0]
            
            # Filter funds within 0.5% risk range and sort by returns
    risk_range = 0.5
    similar_risk_funds = df[
    (df['annualized_mean_std'] >= selected_scheme_risk - risk_range) & 
    (df['annualized_mean_std'] <= selected_scheme_risk + risk_range)
            ].sort_values('annualized_median_return', ascending=False).head(5)
            
            # Display the similar funds in a table
    st.dataframe(similar_risk_funds[['scheme_name', 'annualized_median_return', 'annualized_mean_std']].style.format({
                'returns': '{:.2f}%',
                'risk': '{:.2f}%'
            }))


    st.write("\n 5 Funds with Similar Returns Profile (within 0.25%) and lower risk:")
            
    # Get the risk of selected scheme
    selected_return = df['annualized_median_return'].values[0]
            
    # Filter funds within 0.25% risk range and sort by returns
    return_range = 0.25
    similar_risk_funds = df[
    (df['annualized_median_return'] >= selected_scheme_returns - risk_range) & 
    (df['annualized_median_return'] <= selected_scheme_returns + risk_range)
            ].sort_values('annualized_mean_std', ascending=False).tail(5)
            
    # Display the similar funds in a table
    st.dataframe(similar_risk_funds[['scheme_name', 'annualized_median_return', 'annualized_mean_std']].style.format({
                'returns': '{:.2f}%',
                'risk': '{:.2f}%'
            }))
