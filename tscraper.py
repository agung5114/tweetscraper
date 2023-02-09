import streamlit as st
import pandas as pd
import plotly_express as px
# import pickle 
# from st_aggrid import AgGrid
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from urllib.request import urlopen
import json
# from PIL import Image

import snscrape.modules.twitter as sntwitter
# from textblob import TextBlob

st.set_page_config(layout="wide")
import streamlit.components.v1 as components
import datetime


colr = {'negative':'lightcoral','positive':'green','neutral':'lightblue'}
##TOP PAGE
st.subheader("MoFMAIN TweetScraper")
st.markdown('<style>h1{color:dark-grey;font-size:62px}</style>',unsafe_allow_html=True)
# st.image(Image.open('text.png'))
@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

@st.cache
def get_data(url):
    response = urlopen(url)
    data_json = json.loads(response.read())
    df = pd.DataFrame.from_dict(data_json['data'])
    return df

# @st.cache
# def getData(keyword,start,end,n):
#     tweets_list2 = []
#     # Using TwitterSearchScraper to scrape data and append tweets to list
#     for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:{from_date} until:{end_date}').get_items()):
#         if i>(n-1):
#             break
#         tweets_list2.append([tweet.date, tweet.id, tweet.username,tweet.retweetCount, tweet.content])
#         # tweet.retweetCount
#         df = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Username','Retweeted','Text'])
#     return df.sort_values(by='Retweeted',ascending=False)

@st.cache
def getData(keyword,start,end,n):
    searchtopic = keyword.replace(' ', '')
    start = from_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")
    number = n
    url = f"https://maindata.mofdac.id/livesearch/{searchtopic}/{start}/{end}/{number}"
    response = urlopen(url)
    data_json = json.loads(response.read())
    df = pd.DataFrame.from_dict(data_json['data'])
    return df

menu = ["Live Search","Daily Trends","Account Monitoring"]
choice = st.sidebar.selectbox("Select Menu", menu)
if choice == "Live Search":
   k1,k2,k3,k4 = st.columns((1,1,1,1))
   with k1:
       search_term = st.text_input("Keyword")
   with k2:
       from_date = st.date_input("from date",datetime.date(2023, 1, 1))
   with k3:
       end_date = st.date_input("until date")
   with k4:
       numb= st.number_input("Number to scrape",min_value=1,max_value=1000,step=10,value=10)

   # if choice =="Dashboard":
   if st.button("Run Scraping"):
   #    try:
   #    st.write(search_term+from_date.strftime("%Y-%m-%d")+end_date.strftime("%Y-%m-%d")+str(numb))
      data= getData(search_term,from_date,end_date,numb)
      st.write(f"{len(data.index)} data found")
      data = data[['Datetime','Username','Likes','Retweeted','Sentiment','Text']]
      gb = GridOptionsBuilder.from_dataframe(data)
      gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
      gb.configure_grid_options(domLayout='normal')
      gO = gb.build()
      AgGrid(data,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,gridOptions =gO)
      st.empty()
      csv = convert_df(data)
      st.download_button(
      "Press to Download",
      csv,
      "file.csv",
      "text/csv",
      key='download-csv'
      )

   # try:
      c1, c2 = st.columns((1, 1))
      with c1:
         df1 = data
         fig1 = px.pie(df1, names='Sentiment', values='Retweeted', color='Sentiment', hole=.6,color_discrete_map=colr)
         st.plotly_chart(fig1)

      with c2:
         data['Date'] = pd.to_datetime(data['Datetime']).dt.date
         df2b = data.groupby(by=['Sentiment','Date'],as_index=False).agg({'Retweeted':'sum'})
         fig2 = px.bar(df2b, x='Date', y='Retweeted', color='Sentiment',color_discrete_map=colr)
         fig2.update_xaxes(title_text="")
         st.plotly_chart(fig2)
   # except:
   #    st.write('No Data Found')
if choice == "Daily Trends":
   topiclist = get_data('https://maindata.mofdac.id/list_keywords')
   topic = st.selectbox("Select Menu", topiclist['keyword'])
   seldate = st.date_input("choose date")
   dft = get_data(f"https://maindata.mofdac.id/{topic}/{seldate}")

   # dft['Date'] = dft['Datetime'].apply(lambda x : pd.to_datetime(str(x)))
   dft['Datetime'] = dft['Datetime'].astype('str')
   dft['Date'] = dft['Datetime'].str[:10]
   # dft['Date'] = dft['Datetime'].dt.normalize()
   dft['count'] = 1
   df = dft
   # df = dft.groupby(by=['Sentiment','Date'],as_index=False)['count'].sum()
   cc1, cc2 = st.columns((1, 1))
   with cc1:
      fig1 = px.line(df,
               x='Date',
               y='Retweeted',
               color='Username',
               color_discrete_map=sentcolor,
               title=gtitle,
               labels={'x': 'Time', 'y': 'Number of Tweet'}
               )

      fig1.update_layout(
      title={
         'font_size': 24,
         'xanchor': 'center',
         'x': 0.5
      })
      st.plotly_chart(fig1)
   with cc2:
      pie = px.pie(df[['Sentiment','count']],
               names='Sentiment',
               values='count',
               color='Sentiment',
               color_discrete_map=colr,
               title=gtitle,
               )

      pie.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
        })
      st.plotly_chart(pie)
      
   st.dataframe(df)
