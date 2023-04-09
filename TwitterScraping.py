# importing libraries and package for scrapping the data and manipulation
import snscrape.modules.twitter as sntwitter
import streamlit as st
import pandas as pd
from pymongo import MongoClient

# setting page title
st.set_page_config(page_title='Twitter Scraping')

img = Image.open(r'C:\Users\ELCOT\streamlit\twitter scraper.PNG')
st.image(img)

st.header("Twitter Scraping")

st.subheader("Search")

# getting input from user
Search,No_of_Tweets = st.columns(2)

with Search:
    Search = st.text_input(('Enter your Search , eg. COVID Vaccine'),'COVID Vaccine')
with No_of_Tweets:
    No_of_Tweets = st.number_input('no of tweet count')


From_date,End_date = st.columns(2)
with From_date:
    From_date = st.text_input('enter the Start_date eg. 2021-01-01')
with End_date:
    End_date = st.text_input('enter the  End_date eg. 2021-05-31')
    
def Twitter_Scraping(Search,No_of_Tweets,From_date,End_date):
    Tweets_Data = []
   
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{Search} since:{From_date} until:{End_date}').get_items(),1):  # declare a keyword
        if i> No_of_Tweets: #number of tweets you want to scrape
            break
        Tweets_Data.append([tweet.date, tweet.id,tweet.url, tweet.content, tweet.user.username,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount]) # declare the attributes to be returned
 # Creating a dataframe from the tweets list above        
    tweets_df = pd.DataFrame(Tweets_Data, columns=['Date', 'Tweet Id', 'URL','Text', 'Username','Reply count','Retweet Count','Language','source','Like count'])       
    return tweets_df
    
    
tweets_df = Twitter_Scraping(Search,No_of_Tweets,From_date,End_date)
st.text('press the start button to start the Data')
start = st.checkbox('start')
if start:
    st.dataframe(tweets_df)
# to access the mongodb 
#client = MongoClient('mongodb+srv://yaseen:Yaseen11@cluster0.t6febrh.mongodb.net/test')
client = MongoClient("mongodb://localhost:27017/")
db = client['dw40']
collection = db[Search]

tweets_df.reset_index(inplace = True)

im = Image.open(r'C:\Users\ELCOT\streamlit\ts3.PNG')
st.image(im)

# upload the dataframe to mongodb
st.text('press the upload button to upload the Data in mongoDB')
upload= st.button('upload')
if upload:
    collection.insert_many(tweets_df.to_dict('records'))

imag = Image.open(r'C:\Users\ELCOT\streamlit\ts2.PNG')
st.image(imag)  
    
# Export dataframe into a CSV , json
st.text('press the download to download the Dataframe')
download_csv,download_json =st.columns(2)


with download_csv:
    download_csv =  st.download_button('Download csv') 
    if  download_csv:
        tweets_df.to_csv(f'{Search}.csv', sep=',', index=False)

with download_json:
    download_json =  st.download_button('Download json') 
    if  download_json:
        tweets_df.to_json(f'{Search}.json')  

    
    


    
