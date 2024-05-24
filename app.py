import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
import time


# Define Olympic colors
olympic_colors = ['#0085C7', '#F4C300', '#009F3D', '#FF5800', '#A71930']

# Function to fetch the cleaned web server logs from the API endpoint
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def fetch_cleaned_web_logs(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()['cleaned_data']
        else:
            st.error(f"Failed to fetch cleaned web server logs: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Failed to establish a connection to the API. Please check your connection or contact the admin for further assistance.")
        return None


# Function to create a world map visualization
def create_world_map(df):
    location_counts = df['location'].value_counts().reset_index()
    location_counts.columns = ['country', 'count']
    
    fig = px.choropleth(location_counts, 
                        locations="country", 
                        locationmode="country names", 
                        color="count",
                        title="World Map of Users by Country",
                        color_continuous_scale=olympic_colors)  # Apply Olympic colors
    
    return fig

# Function to create a heatmap of peak traffic periods
def create_heatmap(df):
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['day'] = pd.to_datetime(df['timestamp']).dt.day_name()
    traffic_data = df.groupby(['day', 'hour']).size().unstack(fill_value=0)
    
    fig = go.Figure(data=go.Heatmap(
        z=traffic_data.values,
        x=traffic_data.columns,
        y=traffic_data.index,
        colorscale=olympic_colors))  # Apply Olympic colors
    
    fig.update_layout(
        title='Heatmap of Peak Traffic Periods',
        xaxis_nticks=24
    )
    
    return fig

# Function to create a word cloud for sports-related words
def create_word_cloud(df):
    text = ' '.join(df['sports_related'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.title('Word Cloud for Sports-Related Words')

    return fig

# Function to display the main dashboard
def main_dashboard(api_url):
    st.title('PAYRIS FUNOLYMPICS DASHBOARD')

    # Fetch latest cleaned web server logs from the API endpoint
    logs = fetch_cleaned_web_logs(api_url)
    if logs:
        # Convert logs to DataFrame
        web_logs_df = pd.DataFrame(logs)
        
        # Sidebar filters
        st.sidebar.subheader('Filters')

        # Date Range Filter
        min_date = st.sidebar.date_input('Min Date', None)
        max_date = st.sidebar.date_input('Max Date', None)

        # Country Filter (allow multiple selections)
        selected_countries = st.sidebar.multiselect('Select Country', options=web_logs_df['location'].unique())

        # Apply date range filter if set
        if min_date and max_date:
            web_logs_df['timestamp'] = pd.to_datetime(web_logs_df['timestamp'])
            web_logs_df = web_logs_df[(web_logs_df['timestamp'] >= pd.Timestamp(min_date)) & 
                                      (web_logs_df['timestamp'] <= pd.Timestamp(max_date))]

        # Apply country filter if set
        if selected_countries:
            web_logs_df = web_logs_df[web_logs_df['location'].isin(selected_countries)]

        # KPI Metrics
        st.subheader('Key Performance Indicators (KPIs)')

        # Total Visits
        total_visits = len(web_logs_df)

        # Unique Visitors
        unique_visitors = web_logs_df['num_unique_visitors'].sum()

        # Average Session Duration
        avg_session_duration = web_logs_df['visit_duration'].mean() / 60  # Convert seconds to minutes

        # Bounce Rate
        bounce_rate = (web_logs_df['http_errors'].sum() / total_visits) * 100

        # Display KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Visits", total_visits)
        col2.metric("Unique Visitors", unique_visitors)
        col3.metric("Avg. Session Duration", f"{avg_session_duration:.2f} mins")
        col4.metric("Bounce Rate", f"{bounce_rate:.2f}%")

        # Display updated logs DataFrame
        st.subheader('Cleaned Web Server Logs')
        st.dataframe(web_logs_df)

        # Analysis: Number of visits per country
        if 'location' in web_logs_df:
            st.subheader('Number of Visits per Country')
            visits_per_country = web_logs_df['location'].value_counts().reset_index()
            visits_per_country.columns = ['Country', 'Visit Count']
            st.bar_chart(visits_per_country.set_index('Country'))
            
            # Display world map visualization
            st.subheader('World Map of Users by Country')
            world_map_fig = create_world_map(web_logs_df)
            st.plotly_chart(world_map_fig)

        # Analysis: Popular Sports
        if 'sports_related' in web_logs_df:
            st.subheader('Popular Sports')
            popular_sports = web_logs_df['sports_related'].value_counts().reset_index()
            popular_sports.columns = ['Sport', 'Count']
            st.bar_chart(popular_sports.set_index('Sport'))
            
            # Display word cloud for sports-related words
            st.subheader('Word Cloud for Sports-Related Words')
            word_cloud_fig = create_word_cloud(web_logs_df)
            st.pyplot(word_cloud_fig)

        # Analysis: Referrer Methods and Status Codes in the same row
        if 'referral_traffic' in web_logs_df and 'http_status' in web_logs_df:
            st.subheader('Referral Traffic and Status Codes')

            # Custom CSS to style pie charts side by side
            st.markdown(
                """
                <style>
                .chart-container {
                    display: flex;
                    justify-content: space-between;
                    align-items: left;
                    flex-wrap: wrap;
                }
                .chart-container > div {
                    flex: 1 1 45%;
                    margin: 50px;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader('Referral Traffic')
                    referral_traffic = web_logs_df['referral_traffic'].value_counts().reset_index()
                    referral_traffic.columns = ['Referral Traffic', 'Count']
                    pie_fig = px.pie(referral_traffic, values='Count', names='Referral Traffic', title='Referral Traffic Distribution', width= 400, height=450)
                    pie_fig.update_traces(textinfo='percent+label')
                    pie_fig.update_layout(showlegend=True)
                    st.plotly_chart(pie_fig, use_container_width=True)

                with col2:
                    st.subheader('Status Codes')
                    status_codes = web_logs_df['http_status'].value_counts().reset_index()
                    status_codes.columns = ['Status Code', 'Count']
                    pie_fig = px.pie(status_codes, values='Count', names='Status Code', title='Status Codes Distribution', width= 350, height=300)
                    pie_fig.update_traces(textinfo='percent+label')
                    pie_fig.update_layout(showlegend=True)
                    st.plotly_chart(pie_fig, use_container_width=True)

        # Analysis: Heatmap of Peak Traffic Periods
        if 'timestamp' in web_logs_df:
            st.subheader('Heatmap of Peak Traffic Periods')
            heatmap_fig = create_heatmap(web_logs_df)
            st.plotly_chart(heatmap_fig)

        st.subheader('Time Series Plot: Number of Requests Over Time')

        # Filter for Timeframe
        timeframe_options = ['Hourly', 'Daily', 'Monthly']
        selected_timeframe = st.selectbox('Select Timeframe', timeframe_options, index=0)  # Set default index to 0 for "Hourly"

        # Time Series Plot: Number of Requests Over Time
        if 'timestamp' in web_logs_df:
            web_logs_df['timestamp'] = pd.to_datetime(web_logs_df['timestamp'])  # Convert timestamp to datetime format
            web_logs_df.set_index('timestamp', inplace=True)  # Set timestamp as the index
            
            if selected_timeframe == 'Hourly':
                requests_over_time = web_logs_df.resample('H').size()
                requests_over_time.index = requests_over_time.index.strftime('%Y-%m-%d %H:%M')
                title = 'Number of Requests per Hour'
            elif selected_timeframe == 'Daily':
                requests_over_time = web_logs_df.resample('D').size()
                requests_over_time.index = requests_over_time.index.strftime('%Y-%m-%d')
                title = 'Number of Requests per Day'
            else:
                requests_over_time = web_logs_df.resample('M').size()
                requests_over_time.index = requests_over_time.index.strftime('%Y-%m')
                title = 'Number of Requests per Month'

            fig = px.line(x=requests_over_time.index, y=requests_over_time.values, title=title, labels={'x': 'Date', 'y': 'Number of Requests'})
            st.plotly_chart(fig)

# Function to display the report page
def report_page(api_url):
    st.title('Statistical Report')

    # Fetch latest cleaned web server logs from the API endpoint
    logs = fetch_cleaned_web_logs(api_url)
    if logs:
        # Convert logs to DataFrame
        web_logs_df = pd.DataFrame(logs)

        st.subheader('Descriptive Statistics')
        st.write(web_logs_df.describe())

        # Further detailed statistical analysis can be added here

# Streamlit app main function
def main():
    # API endpoint URL for cleaned data
    api_url = "http://localhost:5000/clean_data"

    # Sidebar navigation
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ["Dashboard", "Report"])

    # Add Olympics rings logo to the top of the sidebar
    olympics_logo_url = "kisspng-olympic-games-2020-summer-olympics-olympic-symbols-5b65a507f20559.3374076815333880399913.png"  # You can replace this with the path to your local image
    st.sidebar.image(olympics_logo_url, use_column_width=True)

    # Add a refresh button to the app
    if st.sidebar.button('Refresh'):
        st.experimental_rerun()

    # Render the selected page
    if page == 'Dashboard':
        main_dashboard(api_url)
    elif page == 'Report':
        report_page(api_url)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
        st.rerun()
