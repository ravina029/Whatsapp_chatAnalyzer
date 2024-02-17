from urlextract import URLExtract
url_extract=URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import unicodedata
import seaborn as sns

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df= df[df['user'] == selected_user]
    
    
    total_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    #fetch number of omitted media
    media_messages=df[df['message'].str.contains('omitted', case=False, na=False)].shape[0]

    #fetch number of linlk shared
    links=[]
    for message in df['message']:
        links.extend(url_extract.find_urls(message))

        
    return total_messages, len(words), media_messages, len(links)

def fetch_busy_users(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user': 'User', 'count': 'Percentage'})

    return x,df

def df_wordcloud(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    df1 = df[~df['message'].str.contains('omitted', case=False)]

    f=open('stop_hinglish.txt','r')
    original_stop_words = f.read()
    stop_words = {word.lower() for word in original_stop_words.split()}

    def remove_stop_words(message):
        x=[]
        for word in message.lower().split():
            if word not in stop_words:
                x.append(word)
        return " ".join(x)

    
    wrdcld=WordCloud(width=500,height=500,min_font_size=10,background_color='black')
    df['message']=df['message'].apply(remove_stop_words)
    wc=wrdcld.generate(df['message'].str.cat(sep=" "))
    return wc

#most common words
def most_common_words(selected_user,df):

    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    
    df1 = df[~df['message'].str.contains('omitted', case=False)]

    f=open('stop_hinglish.txt','r')
    original_stop_words = f.read()
    stop_words = {word.lower() for word in original_stop_words.split()}

    words=[]
    for message in df1['message']:
        for word in message.lower().split(" "):
            if word not in stop_words:
                words.append(word)
    
    our_df=pd.DataFrame(Counter(words).most_common(20))
    return our_df

#Emoji Analysis
def emoji_data(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([char for char in message if unicodedata.category(char) == 'So'])
    
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


#timelina analysis
def timlineinfo(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range (timeline.shape[0]):
        time.append(timeline["month"][i]+ "-" +str(timeline["year"][i]))

    timeline['time']=time
    return timeline


#daily timeline
def daily_timelineinfo(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    
    day_timeline=df.groupby(['theday']).count()['message'].reset_index()

    return day_timeline
      
#weekly activity 

def activity_track(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    
    activity_val=df['day_name'].value_counts()
    return activity_val
    


#monthly activity 

def monthly_activity_track(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    
    activity_val=df['month'].value_counts()
    return activity_val
    
#heatmap
def activity_heatmap(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    
    activityheatmap=df.pivot_table(index="day_name",columns='period',values='message',aggfunc='count').fillna(0)

    return activityheatmap

#sentiment Analysis
def setiment_analysis(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]

    sentiments=df['sentiment'].value_counts()
    return sentiments

    # Return default values if selected_user is 'Overall'
    #return 0, 0


