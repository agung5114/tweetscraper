import streamlit as st
import pandas as pd
# import pickle 
from st_aggrid import AgGrid
from urllib.request import urlopen
# from PIL import Image

import snscrape.modules.twitter as sntwitter
# from textblob import TextBlob

st.set_page_config(layout="wide")
import streamlit.components.v1 as components
import datetime

##TOP PAGE
st.subheader("MoF-DAC TweetScraper")
st.markdown('<style>h1{color:dark-grey;font-size:62px}</style>',unsafe_allow_html=True)
# st.image(Image.open('text.png'))
@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

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
    url = f"https://mofdac.id/livesearch/{searchtopic}/{start}/{end}/{number}"
    response = urlopen(url)
    data_json = json.loads(response.read())
    df = pd.DataFrame.from_dict(data_json['data'])
    return df

k1,k2,k3,k4 = st.columns((1,1,1,1))
with k1:
    search_term = st.text_input("Keyword")
with k2:
    from_date = st.date_input("from date",datetime.date(2022, 1, 1))
with k3:
    end_date = st.date_input("until date")
with k4:
    numb= st.number_input("Number to scrape",min_value=1,max_value=10000,step=100,value=100)

# if choice =="Dashboard":
if st.button("Run Scraping"):
#     try:
   st.write(search_term+from_date.strftime("%Y-%m-%d")+end_date.strftime("%Y-%m-%d")+str(numb))
   data= getData(search_term,from_date,end_date,numb)
   st.write(f"{len(data.index)} data found")
   AgGrid(data)
   csv = convert_df(data)

   st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
   )
#     except:
#         st.subheader("No Data Found")
    
    
