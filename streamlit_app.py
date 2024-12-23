import streamlit as st
import pandas as pd
import numpy as np
#conda install plotly
import plotly.express as px

import streamlit.components.v1 as components

with open("google_analytics.html", "r") as f:
    html_code = f.read()
    components.html(html_code, height=0)

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

# Include Google Analytics tracking code
# from pathlib import Path

# def setup_page():
#         """Configure the Streamlit page settings"""
#         st.set_page_config(
#             page_title="Mutual Funds - Risk and Return Relationship",
#             page_icon="📈",
#             layout="wide"
#         )
#         st.title("Exploring Risk and Return Relationship of Mutual Funds")

# setup_page()

# with open("google_analytics.html", "r") as f:
#     html_code = f.read()
#     components.html(html_code, height=0)

st.title("Exploring Risk and Return Relationship of Mutual Funds")

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

# st.title('Exploring Risk and Return Relationship for Mutual Funds')

df = load_data_from_drive()
df['annualized_mean_std'] = np.round(df['annualized_mean_std'] , 2)
df['annualized_median_return'] = np.round(df['annualized_median_return'] , 2)
intro_text = '''From my own experience and conversations with friends, investing decisions in 
Mutual Funds revolved only around returns. We understand that risk is an important component of investing. 
With Risk being such an important part, there is hardly any discourse and limited
availablity of tools (riskometer being a widely used one) out there. This prompted me to build a tool that maps returns with risk in the context of mutual funds.

We all have risk preferences - some are risk neutral, some risk loving, and others risk averse.
'How do I compare two funds with same risk rating, say, very high?' Is it enough to make a decision by comparing the returns of those two funds?

First, let's understand what 'Risk' means. Consider investment in a Fixed Deposit instrument offering a 7% returns for a period of 1 year.
At the end of year 1, your returns would be exactly 7%. Not more, not less. There is no uncertainty over this. Ignoring the withdrawal charges and other nuances,
the daily return of this instrument is constant (one that equals 7% over a period of 1 year). Now, consider a Mutual Fund whose Net Asset Value (NAV) changes everyday.
There is uncertainty in returns of this instrument. More the returns or NAV varies, more is the uncertainty.
This variability is the risk, measured as Standard Deviation, which will be used synonymously with risk in this tool.  

This tool can help you answer questions like:
 - How much risk am I actually taking?
 - Are there better funds at a same level of risk as the fund I'm invested in?
 - Are there funds with a lower risk that can give similar level of returns? 
'''

st.markdown(intro_text)

# Create scatter plot
# fig = px.scatter( 
#     df,
#     x='annualized_mean_std',
#     y='annualized_median_return',
#     hover_data=['scheme_name'],
#     title='Risk vs Returns Mapping'
#     )
# fig.update_traces(marker_size=4)
# fig.update_layout(scattergap=1)
# st.plotly_chart(fig)

# st.write("\n The above plot shows how **risk and median returns** (both annualized) are related for funds that are *at least 3 years old and currently active* ")
# st.write("\n Risk is the variation in NAV returns (annualized) of a mutual fund")
# st.write("\n Annualized Median Return is the return one could expect about 50 percent of the time, given the funds historical returns")


st.write("\n Here, you could choose to Assess a mutual fund (one that you have/plan to invest in, maybe?) or Find what funds meet your risk and return requirements ")


with st.form("my_form"):
   st.write("What do you want to do?")
#    my_number = st.slider('Pick a number', 1, 10)
   my_choice = st.selectbox('Choose one action', ['Explore funds that satisfy my risk and return needs','Assess a MF scheme I am invested'])
   st.form_submit_button('Submit my choice')

# This is outside the form
# st.write("Your choice is", my_choice)
# st.write(my_color)

if my_choice == 'Assess a MF scheme I am invested':
     
    st.write("\n This workflow will help you understand how your selected fund performs in terms of risk and returns")
    search_scheme = st.text_input("Search for a scheme:")
        
        # Filter schemes based on search
    if search_scheme:
        filtered_df = df[df['scheme_name'].str.contains(search_scheme, case=False, na=False)]
        selected_scheme = st.selectbox(
        "Select a scheme:",
            filtered_df['scheme_name'].tolist()
        )
    else:
        selected_scheme = None
        

        
        # Highlight selected scheme if any
    if selected_scheme:
        selected_data = df[df['scheme_name'] == selected_scheme]
        fig = px.scatter(
            selected_data,
            x='annualized_mean_std',
            y='annualized_median_return',
            size = [10],
            color = ['Selected scheme']
            # mode='markers',
            # marker=dict(size=12, color='red'),
            # name='Selected Scheme',
            # hovertext=selected_data['scheme_name']
        )


        # Display the plot
        st.plotly_chart(fig)
        
        # Display the data table
        # st.write("Data Table:")
        # st.dataframe(df)

# If a scheme is selected, show similar risk funds
    if selected_scheme:
        selected_scheme_risk = float(df.loc[df['scheme_name']==selected_scheme]['annualized_mean_std'])
        selected_scheme_returns = float(df.loc[df['scheme_name']==selected_scheme]['annualized_median_return'])

        st.write("Annualized median Returns of", selected_scheme,":", round(selected_scheme_returns, 2))
        st.write("Annualized Risk of", selected_scheme,":", round(selected_scheme_risk,2))
    
    
        with st.form("my_risk_return_form"):
            st.write("Choose which dimension you would like to focus")
#    my_number = st.slider('Pick a number', 1, 10)
            my_choice_risk_returns = st.selectbox('Choose one option', ['Explore funds with similar returns and lower risk','List funds with similar risk and top 5 returns'])
            st.form_submit_button('Submit my choice')
    
            st.write("\n Top 5 Funds best returns and Similar Risk Profile (within 0.5%):")
            st.write("\n This table lists top 5 Mutual funds in terms of annualized median return and a similar level of risk as that of your selected fund")
    # st.write("\n If your selected fund is not in the list, investing in one of these funds would ")
    # st.write("risk and returns {0}, {1}")        
    # Get the risk of selected scheme
    # selected_risk = df['annualized_mean_std'].values[0]
        # if my_choice_risk_returns == 'List funds with similar risk and top 5 returns':
                
        # Filter funds within 0.5% risk range and sort by returns
        risk_range = 0.5
        similar_risk_funds = df[
        (df['annualized_mean_std'] >= selected_scheme_risk - risk_range) & 
        (df['annualized_mean_std'] <= selected_scheme_risk + risk_range)
                ].sort_values('annualized_median_return', ascending=False).head(5)
                
                # Display the similar funds in a table
        st.dataframe(similar_risk_funds[['scheme_name', 'annualized_median_return', 'annualized_mean_std']].rename
                    (columns = {'annualized_median_return': 'Median_Return', 
                                'annualized_mean_std': 'Risk'}))
        # similar_risk_x = similar_risk_funds['annualized_mean_std']
        # similar_risk_y = similar_risk_funds['annualized_median_return']
        fig.add_scatter( 
                        x=similar_risk_funds['annualized_mean_std'],
                        y=similar_risk_funds['annualized_median_return'],
                        mode='markers',
                        marker=dict(size=6, color='blue'),
                        name='Top 5 Schemes with similar risk',
                        hovertext=similar_risk_funds['scheme_name']
                        )
        # x = [21, 22]
        # y = [40, 40]
        fig.add_vrect(x0=selected_scheme_risk - risk_range,
                    x1=selected_scheme_risk + risk_range,
                    fillcolor="blue",
                    opacity=0.2,
                    line_width=0.5)
        # st.plotly_chart(fig)
    # if my_choice_risk_returns == 'Explore funds with similar returns and lower risk':
            
        st.write("\n 5 Funds with Similar Returns Profile (within 0.5%) and lower risk:")
        st.write("\n This table lists 5 Mutual funds with low risk that have annualized median return comparable to your selected fund")

        # Get the risk of selected scheme
        selected_return = df['annualized_median_return'].values[0]
                
        # Filter funds within 0.5% return range and sort by returns
        return_range = 0.5
        similar_return_funds = df[
        (df['annualized_median_return'] >= selected_scheme_returns - return_range) & 
        (df['annualized_median_return'] <= selected_scheme_returns + return_range)
                ].sort_values('annualized_mean_std', ascending=False).tail(5)
                
        # Display the similar funds in a table
        st.dataframe(similar_return_funds[['scheme_name', 'annualized_median_return', 'annualized_mean_std']].rename
                        (columns = {'annualized_median_return': 'Return (%)', 
                                'annualized_mean_std': 'Risk (%)'}))
        fig.add_scatter( 
                        x=similar_return_funds['annualized_mean_std'],
                        y=similar_return_funds['annualized_median_return'],
                        mode='markers',
                        marker=dict(size=6, color='green'),
                        name='5 Schemes with least risk and Similar Returns',
                        hovertext=similar_return_funds['scheme_name'],
                        text= ('Focus on this bar to find funds with similar risk and higher median returns ')
                        )
        fig.add_hrect(y0 = selected_scheme_returns - return_range,
                        y1 = selected_scheme_returns + return_range,
                        fillcolor="green",
                        opacity=0.2,
                        line_width=0.5)
        st.plotly_chart(fig)


if my_choice == 'Explore funds that satisfy my risk and return needs':
    st.write("\n This choice helps you explore mutual funds with Risk and Returns within the range of your selection, if they exist")
    st.write('Please select return and risk ranges from the slider')
    required_return_range = st.slider("Select a range of required return", 
                                      df['annualized_median_return'].min(), 
                                      df['annualized_median_return'].max(), 
                                      (12.0, 15.0), step = 0.1)
    required_risk_range = st.slider("Select a range of acceptable risk", 
                                    df['annualized_mean_std'].min(), 
                                    df['annualized_mean_std'].max(), 
                                    (10.0, 12.0), step = 0.1)
    no_of_funds_to_display = st.slider("Select maximum no. of funds the satisfying conditions to display:", 1, 10, 5)
    st.write("Required Return Range:", required_return_range)
    st.write("Acceptable Risk Range:", required_risk_range)

    funds_satisfying_requirements = df[
    (df['annualized_median_return'].between(required_return_range[0], required_return_range[1])) &
    (df['annualized_mean_std']).between(required_risk_range[0], required_risk_range[1])
                            ]
    no_of_funds_to_display = min(no_of_funds_to_display, funds_satisfying_requirements.shape[0])
            
    # Display the similar funds in a table
    st.dataframe(funds_satisfying_requirements[['scheme_name', 'annualized_median_return', 'annualized_mean_std']].head(no_of_funds_to_display).
                 rename(columns = {'annualized_median_return': 'Median_Return', 
                                   'annualized_mean_std': 'Risk'}))
    path2_fig = px.scatter(
            funds_satisfying_requirements,
            x='annualized_mean_std',
            y='annualized_median_return',
            hover_data='scheme_name',
            # title_text= 'Schemes that satisfy your Return and Risk characteristics',
            labels={
                     "annualized_mean_std": "Risk (%)",
                     "annualized_median_return": "Return (%)"                     
                 }
            # size = [6],
            # color = ['Selected scheme']
            # mode='markers',
            # marker=dict(size=12, color='red'),
            # name='Selected Scheme',
            # hovertext=selected_data['scheme_name']
        )
    path2_fig.add_vrect(
         x0 = required_risk_range[0],
         x1 = required_risk_range[1],
         fillcolor="green",
        opacity=0.2,
        line_width=0.5
    )
    path2_fig.add_hrect(
         y0 = required_return_range[0],
         y1 = required_return_range[1],
         fillcolor="lightblue",
        opacity=0.2,
        line_width=0.5
    )
    path2_fig.update_xaxes(range=[df['annualized_mean_std'].min(), df['annualized_mean_std'].max()])
    path2_fig.update_yaxes(range=[df['annualized_median_return'].min(), df['annualized_median_return'].max()])
    st.plotly_chart(path2_fig)