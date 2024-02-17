import re 
import pandas as pd 
import datetime
from textblob import TextBlob
import string



def preprocess(file1):
    pattern='\[\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}:\d{2} [APMapm]{2}\]'
    messages=re.split(pattern,file1)[1:]
    dates=re.findall(pattern,file1)
    
    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    #convert type of date
    df['message_date']=pd.to_datetime(df['message_date'],format="[%d/%m/%Y, %I:%M:%S %p]")
    df['message_date'] = df['message_date'].dt.strftime("%Y-%m-%d %I:%M:%S %p")
    df.rename(columns={'message_date':'date'},inplace=True)

    # Your datetime object
    date_time_obj = datetime.datetime.strptime("2019-03-20 17:12:32", "%Y-%m-%d %H:%M:%S")

    # Format with AM/PM
    formatted_time = date_time_obj.strftime("%Y-%m-%d %I:%M:%S %p")

    #separate the user and their message in seprate columns
    user=[]
    message=[]
    for messages in df['user_message']:
        text=re.split('([\w\W]+?):\s',messages)
        if text[1:]:
            user.append(text[1])
            message.append(text[2])
        else:
            user.append('group_notification')
            message.append(text[0])

    df['user']=user
    df['user'] = df['user'].apply(lambda name: name.split('~\u202f')[-1].strip() if '\u202a' not in name else '')

    df['message']=message

    def clean_message(text):
        if pd.notna(text):  # Check for non-null values
        # Remove punctuations and non-alphanumeric characters
            translator = str.maketrans('', '', string.punctuation)
            text = text.translate(translator)
            return text
        else:
            return text
    df['message']=df['message'].apply(lambda x: clean_message(x))
   

    exclude_list = ["Messages and calls are end-to-end encrypted.", "You were added", "code changed", 
                "security code", "message deleted", "invite link", "joined group", "group invite"]

    df = df[~df['message'].str.contains('|'.join(map(re.escape, exclude_list)))]

    df= df.dropna(subset=['user'])
    #df=df.dropna()



    #to extract the year fro datetime first i need to convert it into same format
    df['datetime_column'] = pd.to_datetime(df['date'], format='%Y-%m-%d %I:%M:%S %p')

    # Now, we can use the .dt accessor to extract the year
    df['year'] = df['datetime_column'].dt.year
    df['month'] = df['datetime_column'].dt.month_name()
    df['day'] = df['datetime_column'].dt.day
    df['hour'] = df['datetime_column'].dt.hour
    df['minute'] = df['datetime_column'].dt.minute
    df.drop('datetime_column',axis=1, inplace=True)
    df['month_num']=pd.to_datetime(df['date']).dt.month
    df['theday']=pd.to_datetime(df['date']).dt.date
    df['day_name']=pd.to_datetime(df['theday']).dt.day_name()

    #Extracting total number of links


    #activity time heat map
    duration=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            duration.append(str(hour) + "-"+ str("0"))
        elif hour==0:
            duration.append(str('00')+ "-"+ str(hour+1))
        else:
            duration.append(str(hour)+"-"+str(hour+1))

    df['period']=duration 


    #sentiment analysis
    def analyze_sentiment(text):
        analysis = TextBlob(text)
        return 'Positive' if analysis.sentiment.polarity > 0 else ('Negative' if analysis.sentiment.polarity < 0 else 'Neutral')      

    df['sentiment'] = df['message'].apply(analyze_sentiment)
    return df 