import streamlit as st
import streamlit.components.v1 as components
import pathlib
from bs4 import BeautifulSoup
import logging
import shutil
# with open("google_analytics.html", "r") as f:
#     html_code = f.read()
#     components.html(html_code, height=0)

import pandas as pd
import numpy as np
#conda install plotly
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html
from streamlit_dynamic_filters import DynamicFilters

def inject_ga():
    """Inject Google Analytics JS code"""
    GA_JS = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-GFGYLG0VME"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-GFGYLG0VME');
    </script>
    """

    
     # Insert the script in the head tag of the static template inside your virtual
    # st.write(pathlib.Path(st.__file__).parent)
    # index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    # logging.info(f'editing {index_path}')
    # soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    # if not soup.find(id='G-GFGYLG0VME'): 
    #     # bck_index = index_path.with_suffix('.bck')

    #     # if bck_index.exists():
    #     #     shutil.copy(bck_index, index_path)  
    #     # else:
    #     #     st.write("bck not found")
    #     #     shutil.copy(index_path, bck_index)  
    #     # st.write(bck_index, index_path)
    #     html = str(soup)
    #     new_html = html.replace('<head>', '<head>\n' + GA_JS)
    #     index_path.write_text(new_html)
    #     # with open(index_path,"r") as f_in:
    #     #     st.write("\n".join(f_in.readlines()))
    #     # with open(bck_index,"r") as f_in:
    #     #     st.write("\n".join(f_in.readlines()))



    
    
    # Full HTML with GA in head
    html_code = f"""
        <html>
            <head>
                {GA_JS}
            </head>
            <body>
                <script>
                    // This ensures the GA code runs
                    console.log('GA injection successful');
                </script>
            </body>
        </html>
    """
    
    # Inject the HTML
    html(html_code, height=0, width=0)
# inject_ga()

def main():
    # Inject GA at the very start of your app
    
    st.set_page_config(page_title='Mutual Fund Return & Risk Tool',
    page_icon="🚀",
     layout="centered",
    #  initial_sidebar_state="collapsed",
     menu_items={
         'Get Help': 'mailto:hprithvikrishna@gmail.com?',
        #  'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a cool app on MF Risk and Returns with plans on more features!"
          } )
    
    # inject_ga()
    css='''
[data-testid="stSidebarNav"] {
    position:absolute;
    bottom: 0;
}
'''
    def admin_sidebar():
        with st.sidebar:
            st.page_link('./streamlit_app.py', label='Choose Filters')
    
    admin_sidebar()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    # Your regular Streamlit app code here
    # st.title("My Streamlit App")
    # ... rest of your app ...





    st.title("Exploring Risk and Return Relationship of Mutual Funds")

    def load_data_from_file():
            """
            Load data from a specific directory on drive.
            Supports multiple file formats (csv, excel, parquet).
            """
            # Define the data directory - update this path to your data location
            # data_file = "data/scheme_stats_MC_atleast_3_yrs.csv"  # Update this path
            data_file = "data/scheme_stats_with_metadata.csv"
            try:
                # Look for data files in the specified directory
                # data_file = list(Path(DATA_DIR).glob("*.csv"))  # For CSV files
                data = pd.read_csv(data_file)
                return data
                
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                st.stop()

    # st.title('Exploring Risk and Return Relationship for Mutual Funds')

    df = load_data_from_file()
    # st.write("Baba booey", df.shape)
    df['annualized_mean_std'] = np.round(df['annualized_mean_std'] , 2)
    df['annualized_median_return'] = np.round(df['annualized_median_return'] , 2)
    intro_text = '''
    
    :blue-background[Consider investment in a Fixed Deposit instrument offering a 7% returns for a period of 1 year.
    At the end of year 1, your returns would be exactly 7% with no uncertainty. Now, consider a Mutual Fund whose Net Asset Value (NAV) changes everyday.
    There is uncertainty in returns of this instrument over any time period. More the returns or NAV varies, more is the uncertainty.]
    
    :green-background[Risk is the variance in price/return, measured as Standard Deviation, 
    which will be used synonymously with risk in this tool.]  

    This tool can help you answer questions like:
    - How much risk are you taking?
    - Are there better funds at a same level of risk as the fund I'm invested in?
    - Are there funds with a lower risk that can give similar level of returns? 
    '''

    st.markdown(intro_text)
    st.image("./images/stochastic_process.png", caption = 'Example of a MF returns over 1 year as a Distribution')

    image_text = '''
                :red-background[Prices of risky instruments like MFs can't be predicted over any time period and hence we use simulations to 
                understand how the probability distribution of prices would be. The above image shows how the price a MF with an initial price of 100
                could evolve over 1 year. Distributions like this could give valuable insights like the median return, worst case return, and best case return.
                These insights could help us in making well-informed decisions.          
                ]
    
                 '''
    
    st.markdown(image_text)
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


    # st.write("\n Here, you could choose to Assess a mutual fund (one that you have/plan to invest in, maybe?) or Find what funds meet your risk and return requirements ")


    with st.form("my_form"):
        st.write("What do you want to do?")
        #    my_number = st.slider('Pick a number', 1, 10)
        my_choice = st.selectbox('Choose one action',
                                  ['Explore funds that satisfy my risk and return needs',
                                   'Assess a MF scheme I am invested / want to invest in',
                                   'I want to filter MFs based on its attributes'])
        st.form_submit_button('Submit my choice')

    # This is outside the form
    # st.write("Your choice is", my_choice)
    # st.write(my_color)

    if my_choice == 'Assess a MF scheme I am invested / want to invest in':
        
        
        st.write("\n You can choose one MF scheme to find its performance in terms of risk and returns")
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
            selected_scheme_df = pd.DataFrame(
                    {
                        'Risk': [float(selected_data['annualized_mean_std'])
                                , float(selected_data['annualized_mean_std'])
                                , float(selected_data['annualized_mean_std'])] ,
                        'Returns': [float(selected_data['annualized_median_return'])
                                , float(selected_data['bottom_5_percentile'])
                                , float(selected_data['top_5_percentile'])] ,
                        'Point_Labels': ['Median Returns'
                                , 'Worst Case Returns'
                                , 'Best Case Returns']
                    }

            )
            # selected_data['point_label'] = ['Median Returns', 'Worst case returns', 'Best Case returns']
            fig_selected_scheme = px.scatter(
                selected_scheme_df,
                x= 'Risk',
                y = 'Returns',
                # ['', '', ''],
                size = [8, 8, 8],
                # text = 'Point_Labels',
                color= ['Median Returns', 'Worst Case Returns', 'Best Case Returns'],
                # hover_data = {'Scheme Risk': selected_scheme_df['Risk']
                            #   ,'Scheme Returns': selected_scheme_df['Returns'] }
                # text = 'point_label'
                # mode='markers',
                # marker=dict(size=12, color='red'),
                # name='Selected Scheme',
                # hovertext=selected_data['scheme_name']
            )


            # Display the plot
            st.plotly_chart(fig_selected_scheme)
            
            # Display the data table
            # st.write("Data Table:")
            # st.dataframe(df)

    # If a scheme is selected, show similar risk funds
        if selected_scheme:
            selected_scheme_risk = float(df.loc[df['scheme_name']==selected_scheme]['annualized_mean_std'])
            selected_scheme_median_returns = float(df.loc[df['scheme_name']==selected_scheme]['annualized_median_return'])
            selected_scheme_best_returns = float(df.loc[df['scheme_name']==selected_scheme]['top_5_percentile'])
            selected_scheme_worst_returns = float(df.loc[df['scheme_name']==selected_scheme]['bottom_5_percentile'])

            st.write('For your selected scheme:')
            st.write("\n 1 Yr Median Returns:", round(selected_scheme_median_returns, 2))
            st.write("\n 1 Yr Best Case Scenario Returns:", round(selected_scheme_best_returns, 2))
            st.write("\n 1 Yr Worst Case Scenario Returns:", round(selected_scheme_worst_returns, 2))
            st.write("\n Annualized Risk:", round(selected_scheme_risk,2))
        
        
    #         with st.form("my_risk_return_form"):
    #             st.write("Choose which dimension you would like to focus")
    # #    my_number = st.slider('Pick a number', 1, 10)
    #             my_choice_risk_returns = st.selectbox('Choose one option', ['Explore funds with similar returns and lower risk','List funds with similar risk and top 5 returns'])
    #             st.form_submit_button('Submit my choice')
        
            st.write("\n Look at these funds if you want to get Median returns for s risk similar to the fund you've selected:")
            # st.write("\n This table lists top 5 Mutual funds in terms of annualized median return and a similar level of risk as that of your selected fund")
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

            fig = px.scatter(
                selected_data,
                x= 'annualized_mean_std',
                y = 'annualized_median_return',
                # ['', '', ''],
                size = [5],
                title = 'MEDIAN returns for your selected MF and Comparable MFs'
                # text = 'Point_Labels',
                # color= ['Median Returns', 'Worst Case Returns', 'Best Case Returns'],
                # hover_data = {'Scheme Risk': selected_scheme_df['Risk']
                            #   ,'Scheme Returns': selected_scheme_df['Returns'] }
                # text = 'point_label'
                # mode='markers',
                # marker=dict(size=12, color='red'),
                # name='Selected Scheme',
                # hovertext=selected_data['scheme_name']
            )

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
                
            st.write("\n Look at these funds if you want to get Median returns similar to that of your selected fund but at a lower level of risk")
            # st.write("\n This table lists 5 Mutual funds with low risk that have annualized median return comparable to your selected fund")

            # Get the risk of selected scheme
            selected_return = df['annualized_median_return'].values[0]
                    
            # Filter funds within 0.5% return range and sort by returns
            return_range = 0.5
            similar_return_funds = df[
            (df['annualized_median_return'] >= selected_scheme_median_returns - return_range) & 
            (df['annualized_median_return'] <= selected_scheme_median_returns + return_range)
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
            fig.add_hrect(y0 = selected_scheme_median_returns - return_range,
                            y1 = selected_scheme_median_returns + return_range,
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


    if my_choice == 'I want to filter MFs based on its attributes':

        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)

# Define numeric and categorical columns explicitly
        numeric_columns = [
            'scheme_code', 
            'annualized_median_return', 
            'top_25_percentile', 
            'bottom_25_percentile', 
            'bottom_5_percentile', 
            'top_5_percentile', 
            'annualized_mean_std'
        ]

        categorical_columns = [
            'scheme_name',
            'Fund_House',
            'Scheme_Type',
            'Asset_Class',
            'Investment_Type'
        ]

        # Convert numeric columns
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Ensure categorical columns are strings
        for col in categorical_columns:
            df[col] = df[col].astype(str)

        # Print data types to verify conversions
        # st.write("DataFrame column types:", df.dtypes)
        st.write('Use the sidebar on the top left to filter MF schemes')
        # Create filters with explicit configuration
        filters_config = {
            'Investment_Type': {
                'type': 'select',
                'values': sorted(df['Investment_Type'].unique().tolist())
            },
            'Asset_Class': {
                'type': 'select',
                'values': sorted(df['Asset_Class'].unique().tolist())
            },
            'Scheme_Type': {
                'type': 'select',
                'values': sorted(df['Scheme_Type'].unique().tolist())
            }
            
        }

        try:
            with st.sidebar:
                dynamic_filters = DynamicFilters(
                    df=df[[ 'scheme_name',
                            'Fund_House', 
                            'Asset_Class',
                            'Scheme_Type',
                            'Investment_Type',
                            'annualized_median_return',
                            'annualized_mean_std',
                              ]],
                    # filters=filters_config
                    filters = [] #, 'Asset_Class', 'Scheme_Type', 'Investment_Type']
                )
                dynamic_filters.display_filters()
            
            # Get and display filtered dataframe
            filtered_df = dynamic_filters.filter_df()
            st.write('The below table shows MF as per your selection of filters in the sidebar')
            st.dataframe(filtered_df)

        except Exception as e:
            st.error(f"Error encountered: {str(e)}")
            st.write("DataFrame head:", df.head())
            st.write("DataFrame info:", df.info())


if __name__ == "__main__":
    main()