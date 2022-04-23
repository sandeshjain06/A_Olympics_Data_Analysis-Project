import streamlit  as st
import pandas as pd
import  preprocessor , helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.sidebar.image('https://www.urbanriver.com/wp-content/uploads/2012/04/olympic-rings.gif')
st.sidebar.title('Olympics Analysis')

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
# To Get the EDA part Done
df = preprocessor.preprocess(df,region_df)

user_menu = st.sidebar.radio(
    'Select an option',('Medal Tally','Overall Analysis',
                        'Country-Wise Analysis','Athlete-Wise Analysis'))

if user_menu == 'Medal Tally':
    years, country = helper.country_year_list(df)
    selected_country=st.sidebar.selectbox("Select Country",country)
    selected_year=st.sidebar.selectbox("Select Year",years)


############### Medal Tally  #########################

if user_menu == 'Medal Tally':
    medal_tally_values = helper.fetch_medal_country_years(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally for All Countries')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Won in '+str(selected_year) +'by all countries')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal Won by '+str(selected_country))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal Won by '+str(selected_country) +' in the year '+str(selected_year))

    st.table(medal_tally_values)

############### Overall Analysis  #########################

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]-1
    sports = df['Sport'].unique().shape[0]-1
    events = df['Event'].unique().shape[0]-1
    atheletes = df['Name'].unique().shape[0]-1
    nations = df['region'].unique().shape[0]-1

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2 :
        st.header("Hosting Nations")
        st.title(cities)
    with col3 :
        st.header("Nation Participated")
        st.title(nations)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Event")
        st.title(events)
    with col2 :
        st.header("Athletes")
        st.title(atheletes)
    with col3 :
        st.header("Sports")
        st.title(sports)

    # Nations participating every year
    st.title('Participating Nations Over Time')
    nations_over_time,events_over_time,atheletes_over_time=helper.nations_over_time(df)
    fig = px.line(nations_over_time, x='Year', y='No_of_Country')
    st.plotly_chart(fig)
    # Events happening every year
    st.title('Events Over Time')
    fig = px.line(events_over_time, x='Year', y='No_of_Events')
    st.plotly_chart(fig)
    # Atheltes participating every year
    st.title('Athletes Over Time')
    fig = px.line(atheletes_over_time, x='Year', y='No_of_athletes')
    st.plotly_chart(fig)
    # No of events over time(Every Sport)
    st.title('No of Events & Sports Over Time')
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0),annot=True)
    st.pyplot(fig)

    st.title('Most Successful Atheletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    Sports_filter = st.selectbox("Select Sports", sports_list)
    x= helper.most_successful(df,Sports_filter)
    st.table(x)

############### Country - Wise Medal Tally  #########################


if user_menu == 'Country-Wise Analysis':

    st.title('Country-Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    select_country = st.sidebar.selectbox("Select Country",country_list)

    st.title(select_country + ' Medal Tally Over the years')
    year_wise_medal_forcountry =helper.Yearwise_country_medal(df,select_country)
    fig = px.line(year_wise_medal_forcountry, x='Year', y='Medal')
    st.plotly_chart(fig)

    st.title(select_country + ' Participation List')
    participation_list = helper.country_allgames_details(df,select_country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax = sns.heatmap(participation_list,annot=True)
    st.pyplot(fig)

    # Most Successfull Athletes over the years
    st.title(select_country + ' Top Athletes')
    top_atheltes=helper.most_successful_country_wise_player(df,select_country)
    st.table(top_atheltes)

############### Atheltes Wise Analysis  #########################

if user_menu == 'Athlete-Wise Analysis':

    st.title('Athlete Height Vs Weight Comparison')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    Sports_filter = st.selectbox("Select Sports", sports_list)
    temp_df = helper.weight_vs_height(df,Sports_filter)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],
               style=temp_df['Sex'],s=50)
    st.pyplot(fig)

    st.title('Male Vs Female Participation')
    men_women_participate = helper.menvswomen(df)
    fig = px.line(men_women_participate, x='Year', y=['Male','Female'])
    st.plotly_chart(fig)


