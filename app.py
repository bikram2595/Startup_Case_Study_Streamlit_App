import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title = 'StartUp Analysis')

df = pd.read_csv('startup_clean.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# st.dataframe(df)

st.sidebar.title('Startup Funding Analysis')

def investor_details(investor):
    st.title(investor)
    #recent 5 investments
    last_5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_5_df)

    col1, col2 = st.columns(2)
    with col1:
        #biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        # sectors invested
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(
            ascending=False)
        st.subheader('Sectors Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels = vertical_series.index,autopct = "%0.01f")
        st.pyplot(fig1)

    col1, col2 = st.columns(2)
    with col1:
        #stages invested
        stage_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending=False)
        st.subheader("Stages Of Investment")
        fig3, ax3 = plt.subplots()
        ax3.pie(stage_series,labels = stage_series.index,autopct = "%0.01f")
        st.pyplot(fig3)

    with col2:
        #stages invested
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False)
        st.subheader("City Of Investment")
        fig4, ax4 = plt.subplots()
        ax4.pie(city_series,labels = city_series.index,autopct = "%0.01f")
        st.pyplot(fig4)

    col1, col2 = st.columns(2)
    with col1:
    # print(df.info())
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YoY Investments')
        fig5, ax5 = plt.subplots()
        ax5.plot(year_series.index, year_series.values)
        st.pyplot(fig5)

def overall_analysis():
    st.title('Overall Analysis')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        #Total investment
        total = round(df['amount'].sum())
        st.metric('Total Investment:',str(total)+ ' CR' )

    with col2:
        max = round(df.groupby('startup')['amount'].sum().max())
        st.metric('Maximum Investment:', str(max)+ ' CR')

    with col3:
        avg = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('Average Ticket Size:', str(avg)+ ' CR')

    with col4:
        count = df['startup'].nunique()
        st.metric('Funded Startups', str(count))

    st.subheader('MoM graph')
    selected_plot = st.selectbox('Select Type',['Total','Count'])

    if selected_plot == "Total":
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()


    temp_df['x_axis'] = temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')

    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig6)

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == "Overall Analysis":
    overall_analysis()
elif option == "Startup":
    st.sidebar.selectbox('Select Startup',list(sorted(df['startup'].unique())))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        investor_details(selected_investor)
