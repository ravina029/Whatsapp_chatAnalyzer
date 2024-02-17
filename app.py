import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns




st.sidebar.title("Whatsapp Chat Analyzer")


#uploaded_file = st.sidebar.file_uploader("Choose a file")
#if uploaded_file is not None:
    # To read file as bytes:
    #bytes_data = uploaded_file.getvalue()
    #data=bytes_data.decode('utf-8')
    #st.text(data)

import streamlit as st

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        
        # Attempt to decode as utf-8
        data = bytes_data.decode('utf-8')
        df=preprocessor.preprocess(data)
        
        # Display the data
        #st.dataframe(df)

        user_list=df['user'].unique().tolist()
        #user_list.remove('Technion Indians 🇮🇳')
        user_list.sort()
        user_list.insert(0,'Overall')
        selected_user=st.sidebar.selectbox('Show analysis wrt', user_list)
        num_messages=helper.fetch_stats(selected_user,df)

        if st.sidebar.button('Show analysis'):
            total_messages,words,media_messages,total_links=helper.fetch_stats(selected_user,df)
            st.title('Statistical information')
            col1, col2, col3, col4=st.columns(4)


            with col1:
                  st.header("Messages")
                  st.title(total_messages)
            with col2:
                  st.header('Words')
                  st.title(words)
            with col3:
                  st.header('Media')
                  st.title(media_messages)
            #with col4:
                  #st.header('Shared links')
                  #st.title(total_links)
            
            #monthly timeline of the chats
            st.title('Monthly activity')
            timeline=helper.timlineinfo(selected_user,df)
            fig,ax=plt.subplots()
            ax.set_facecolor('#D2B48C')
            ax.plot(timeline['time'],timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            #monthly timeline
            st.title('Daily activity')
            daily_timeline=helper.daily_timelineinfo(selected_user,df)
            fig,ax=plt.subplots()
            ax.set_facecolor('#FFA500')
            ax.plot(daily_timeline['theday'],daily_timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


            #Most active day
            st.title('Weekly and Monthly activity')
            col1,col2=st.columns(2)
            
            with col1:
                st.header("Most active day")
                busy_day=helper.activity_track(selected_user,df)
                fig,ax=plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='orange')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.header("Most active month")
                busy_month=helper.monthly_activity_track(selected_user,df)
                fig,ax=plt.subplots()
                ax.bar(busy_month.index,busy_month.values,color='blue')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            #weekly activity map using heatmap
            st.title('Intensity of activity on weekdays')
            active_heatmap=helper.activity_heatmap(selected_user,df)
            fig,ax=plt.subplots()
            ax=sns.heatmap(active_heatmap)
            st.pyplot(fig)



            #the busiest user 
            if selected_user=='Overall':
                  st.title('Most active users')
                  x,usr_df=helper.fetch_busy_users(df)
                  fig,ax=plt.subplots()
                  

                  col1,col2=st.columns(2)
                  with col1:
                        ax.bar(x.index,x.values,color='blue')
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                  with col2:
                        st.dataframe(usr_df)
            #wordcloud of data
            st.title('Most common words')
            word_cloud=helper.df_wordcloud(selected_user,df)
            fig,ax=plt.subplots()
            ax.imshow(word_cloud)
            st.pyplot(fig)

            #most common words
            Most_common_Words=helper.most_common_words(selected_user,df)
            fig,ax=plt.subplots()

            ax.barh(Most_common_Words[0],Most_common_Words[1])
            st.title('Frequency of common words')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            

            #st.dataframe(Most_common_Words)

            #Emoji Analysis
            emoji_df=helper.emoji_data(selected_user,df)
            st.title("Emoji Used")
            #st.dataframe(emoji_df)
            col1,col2=st.columns(2)
            if emoji_df.shape[0]>0:
                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    fig,ax=plt.subplots()
                    ax.pie(emoji_df[1].tail(5),labels=emoji_df[0].tail(5),autopct="%0.2f")
                    st.pyplot(fig)
            else:
                 print('No emoji used')


            #Sentiment Analysis
            sentiment_counts=helper.setiment_analysis(selected_user,df)
            
            #bar graph of sentiments
            st.title("Bar graph showing sentiments chats")
            fig, x = plt.subplots()
            x.bar(sentiment_counts.index,sentiment_counts,color='blue')
            plt.xticks(rotation='horizontal')
            st.pyplot(fig)

            #pie chart of sentiments
            st.title("Percentage of all sentiments")
            fig, x = plt.subplots() 
            x.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.3f%%', colors=['gray', 'green', 'red'])
            st.pyplot(fig)     

            
            
                    
            
                  
                  




                        
    
