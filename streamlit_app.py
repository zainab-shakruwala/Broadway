import streamlit as st
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
import os
import plotly.express as px
import plotly.graph_objects as go

def plot(df, y_col):
    fig = px.line(df, x= 'DateMonth', y=y_col, 
                title='Monthly Broadway Gross Revenue',
                color_discrete_sequence=['teal'])
    fig.update_traces(line = dict(width=3))
    fig.update_layout(yaxis_tickformat = '$,.0f', hovermode = 'x unified')
    fig.update_yaxes(rangemode = 'tozero')
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(
    page_title = "Broadway Analysis",
    page_icon = "🎭",
    layout = "wide"

)

st.title("Broadway Analysis 🎭")
st.markdown("Let us see some statistics on Broadway Shows. Note this dataset is taken from Kaggle and the data in only available till 07/2016.")

tab1, tab2, tab3 = st.tabs(["💵 Revenue ", "🎙️ Top Shows ","🧙🏼‍♀️ Wicked Predictions "])
df_broadway = pd.read_csv("data/broadway.csv")
df_broadway = df_broadway[df_broadway["Date.Year"]!=1990]
df_broadway["Date"] = pd.to_datetime(df_broadway["Date.Full"])
df_broadway["DateMonth"] = df_broadway["Date"].dt.to_period('M')
df_broadway["GrossMonthly"] = df_broadway.groupby("DateMonth")['Statistics.Gross'].transform('sum')
df_result = pd.read_csv("data/WickedResult.csv")

with tab1:
    gross_monthly = df_broadway.groupby("DateMonth")['Statistics.Gross'].sum()
    gross_monthly = gross_monthly.iloc[:-1]
    gross_monthly.index = gross_monthly.index.to_timestamp()

    # Create complete date range
    date_range = pd.date_range(start=gross_monthly.index.min(), 
                            end=gross_monthly.index.max(), 
                            freq='MS')

    # Reindex and fill missing values
    gross_monthly = gross_monthly.reindex(date_range, fill_value=0)

    gross_monthly_df = gross_monthly.reset_index()
    gross_monthly_df.columns = ['DateMonth', 'GrossMonthly']
    st.header("Total Revenue")
    plot(gross_monthly_df, "GrossMonthly")

with tab2:
    st.header("Top Shows")
    
                
                # Allow user to select number of shows
    num_shows = st.slider("Number of top shows to display", 5, 20, 10)
    select_option = st.selectbox(
            "Choose an option:",
            ["Average Gross per Week", "Total Revenue", "Running Weeks"]
        )
    if select_option == "Average Gross per Week":
        avg_gross_by_show = df_broadway.groupby("Show.Name")['Statistics.Gross'].mean().sort_values(ascending=False)
        y_col = 'Average Gross'
        title = f"Top {num_shows} Broadway Shows by Average Gross per Week"
        y_axis_title = "Average Gross Revenue (Millions $)"
        y_axis_tickformat = '$,.2s'
        hovertemplate = '<b>%{x}</b><br>Average Weekly Gross: $%{y:,.0f}<extra></extra>'
        # Prepare data for Plotly
        top_shows = avg_gross_by_show.head(num_shows)
        
    elif select_option == "Total Revenue":
        gross_by_show = df_broadway.groupby(["Show.Name"])['Statistics.Gross'].sum().sort_values(ascending=False)
        top_shows = gross_by_show.head(num_shows)
        y_col = 'Total Revenue'
        title = f"Top {num_shows} Broadway Shows by Total Revenue"
        y_axis_title = "Total Revenue (Millions $)"
        y_axis_tickformat = '$,.2s'
        hovertemplate = '<b>%{x}</b><br> Total Revenue: $%{y:,.0f}<extra></extra>'
        # Prepare data for Plotly
    else:
        total_shows = df_broadway["Show.Name"].value_counts()
        y_col = 'Running Weeks'
        title = f"Top {num_shows} Broadway Shows by Number of Running Weeks"
        y_axis_title = "Number of Weeks"
        y_axis_tickformat = ',.2s'
        hovertemplate = '<b>%{x}</b><br> Running Weeks: %{y:,.0f}<extra></extra>'
        # Prepare data for Plotly
        top_shows = total_shows.head(num_shows)


        
        

    top_shows_df = top_shows.reset_index()
    top_shows_df.columns = ['Show Name', y_col]
    
    # Create Plotly bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=top_shows_df['Show Name'],
            y=top_shows_df[y_col],
            marker_color='teal',
            hovertemplate=hovertemplate
        )
    ])
    
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 16, 'family': 'Arial, sans-serif'}
        },
        xaxis_title="Show Name",
        yaxis_title=y_axis_title,
        xaxis_tickangle=-45,
        height=600,
        hovermode='x',
        yaxis_tickformat=y_axis_tickformat)


        
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Monthly Forecast of 🧙🏼‍♀️ Wicked's Broadway Sales")
    st.markdown("The Predictions are based on an ARIMA model. To learn about the methodology of this prediction, checkout this [article](https://medium.com/@zainabshakruwala/the-one-train-821d4b114435) I posted on Medium.")
    df_wicked  = df_broadway[df_broadway["Show.Name"]=="Wicked"]
    
    monthly_wicked = df_wicked.groupby("DateMonth")['Statistics.Gross'].sum()
    monthly_wicked = monthly_wicked.iloc[:-1]
    monthly_wicked.index = monthly_wicked.index.to_timestamp()

    # Making sure we have no nulls
    date_range = pd.date_range(start = monthly_wicked.index.min(),
                            end = monthly_wicked.index.max(),
                            freq = 'MS')

    monthly_wicked = monthly_wicked.reindex(date_range, fill_value = 0)
    monthly_wicked = monthly_wicked.reset_index()
    monthly_wicked.columns = ["DateMonth", "GrossMonthly"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_wicked['DateMonth'] , y = monthly_wicked['GrossMonthly'], 
                             line = dict(color = '#00A651', width = 2),
                             name = 'Historical Sales'))
    fig.add_trace(go.Scatter(x = df_result['DateMonth'], y = df_result['predicted_mean'], 
                             line=dict(color='#E94190', width=2) ,
                             name = 'Predicted Sales'))
    # fig.add_trace(go.Scatter(x = monthly_wicked['DateMonth'], y = forecast, name='Forecast'))
    fig.update_layout(hovermode = "x unified")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("To see the source code, checkout my [GitHub](https://github.com/zainab-shakruwala/Broadway).")

    

# Footer
st.divider()
st.markdown("---")
st.caption("© 2025 Zainab Shakruwala | Check Out My Work: [Portfolio](https://zainab-shakruwala.github.io/portfolio/) | All Rights Reserved | Built with Streamlit 🎈 | Learn more at [streamlit.io](https://streamlit.io)")