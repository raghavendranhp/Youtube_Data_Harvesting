import streamlit as st
from youtube_class import YoutubeHarvesting  #import YouTube API Handler class
from mongodb_query import mongodb_work #import Mongodb Handler class
from mysql_queries import sql_work #import mysql Handler class
import datetime #for converting duration
import matplotlib.pyplot as plt #for display appealing results

youtube_handler = YoutubeHarvesting()
mongodb_handler=mongodb_work()
sql_handler=sql_work()


channel_details = None
# Streamlit app
st.set_page_config(
    page_title="Youtube Data Harvesting-Project1",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")
st.title("YouTube Data Harvesting")
#channel details getting from user
st.header("Channel Details")
channel_name = st.text_input("Enter the YouTube Channel Name:")
st.write('You entered Channel Name',channel_name)
if st.button("Confirm & Fetch Channel Details"):
    if channel_name:
        channel_details = youtube_handler.get_channel_details_using_channelname(channel_name)
        if channel_details:
            st.json(channel_details)
        else:
            st.error("Channel not found. Please check the channel name.")
    else:
        st.warning("Please enter a YouTube channel name.")

# Check if channel_details is not None before accessing it
if channel_details:
    try:
        channel_id = channel_details['channel_id']
        video_ids_list=youtube_handler.get_video_ids_by_channel_id(channel_id)
        playlist_details=youtube_handler.playlist_details_using_channelid(channel_id)
        video_details=youtube_handler.get_videos_details_using_videoidslist(video_ids_list)
        record={
        '_id':channel_id,
        'channel_details':channel_details,
        'playlist_details':playlist_details,
        'video_details':video_details}
        insert_condition=mongodb_handler.insert_into_mongodb(record)
    except Exception as e:
        st.error("Error Occured while retrieving data",e)

# creating question dictionary by which analyse can be done
question_dictionary={
'What are the names of all the videos and their corresponding channels?':1,
'Which channels have the most number of videos, and how many videos do they have?':2,
'What are the top 10 most viewed videos and their respective channels?':3,
'How many comments were made on each video, and what are their corresponding video names?':4,
'Which videos have the highest number of likes, and what are their corresponding channel names?':5,
'What is the total number of likes and dislikes for each video, and what are their corresponding video names?':6,
'What is the total number of views for each channel, and what are their corresponding channel names?':7,
'What are the names of all the channels that have published videos in the year 2022?':8,
'What is the average duration of all videos in each channel, and what are their corresponding channel names?':9,
'Which videos have the highest number of comments, and what are their corresponding channel names?':10}
questions=list(question_dictionary.keys())
channel_dictionary=mongodb_handler.get_channels()   
channels=list(channel_dictionary.keys())
if channels:
    st.header("Channel Data Migration")
    option = st.selectbox(
    'Select the Channel Name,for Migration to MySQL',
    (channels))
    st.write('You selected:', option)
    if st.button("Migrate Data"):
        if option=='No Channel available':
            pass
        else:
            try:
                channel_id=channel_dictionary[option]
                channel_dataframe=mongodb_handler.channel_query(channel_id)
                video_dataframe=mongodb_handler.video_query(channel_id)
                playlist_dataframe=mongodb_handler.playlist_query(channel_id)
                comments_dataframe=mongodb_handler.comment_query(channel_id)
                sql_handler.table_creation()
                sql_handler.insert_to_mysql(channel_dataframe,playlist_dataframe,video_dataframe,comments_dataframe)
            except exception as e:
                st.error("Error Occured while Migrating data",e)
st.header("DATA Analysis")
question_option=st.selectbox(
    'Select the question for display analysis',
    (questions))
st.write('You selected:', question_option)
if st.button("Fetch Results"):
    required_function=question_dictionary[question_option]
    if required_function==1:
        display=sql_handler.question1()
        st.write("TABLE-the names of all the videos and their corresponding channels")
        st.dataframe(display)
    elif required_function==2:
        display=sql_handler.question2()
        display = display.sort_values(by='channel_videocount', ascending=False)
        # Create the bar chart
        fig, ax = plt.subplots()
        fig.set_figheight(8)
        fig.set_figwidth(12)
        ax.bar(display['channel_title'], display['channel_videocount'])
        # Customize the plot
        plt.xticks(rotation=45, fontsize=12)
        plt.xlabel('Channel Title', fontsize=14)
        plt.ylabel('Channel Video Count', fontsize=14)
        plt.title('Channel Video Count by Title (Descending Order)', fontsize=16)
        st.pyplot(fig)
        st.write("TABLE-Channels have the most number of videos")
        st.dataframe(display)
    elif required_function==3:
        display=sql_handler.question3()
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(display['Video_Name'], display['View_Count'], color='skyblue')
        plt.xlabel('View Count', fontsize=14)
        plt.ylabel('Video Name', fontsize=14)
        plt.title('View Count by Video Name', fontsize=16)
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        for i, (v, channel_title) in enumerate(zip(display['View_Count'], display['channel_title'])):
            ax.text(v + 50, i, f'{v} ({channel_title})', va='center', fontsize=12, color='black')
        st.pyplot(fig)
        st.markdown("---")
        st.write("TABLE-The Top 10 most Viewed videos")
        st.dataframe(display)
    elif required_function==4:
        display=sql_handler.question4()
        st.write("TABLE-The Comments were made on each video ")
        st.dataframe(display)
    elif required_function==5:
        display=sql_handler.question5()
        st.write("TABLE-The Videos have the Highest number of Likes, and their corresponding channel names")
        st.dataframe(display)
    elif required_function==6:
        display=sql_handler.question6()
        st.write("TABLE-The Total number of Likes and Dislikes for each video & their corresponding video names")
        st.dataframe(display)
    elif required_function==7:
        display=sql_handler.question7()
        # Display the DataFrame
        st.write("TABLE-The Total number of Views for each channel & their corresponding Channel names")
        st.dataframe(display)
    elif required_function==8:
        display=sql_handler.question8()
        st.write('Video published in year 2022')
        st.bar_chart(display,x='Channel_title',y='Video_count')
        st.markdown("---")
        st.write("TABLE-The names of all the Channels that have Published videos in the year 2022")
        st.dataframe(display)
        
    elif required_function==9:
        display=sql_handler.question9()
        def format_duration(duration):#here duration in format of 0 days,hh:mm:ss with nanoseconds so converting
            seconds = duration.total_seconds()
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
        display['Average_duration'] = display['Average_duration'].apply(format_duration)
        st.write("TABLE-The average duration of all videos in each channel & Their corresponding channel names")
        st.dataframe(display)
    elif required_function==10:
        display=sql_handler.question10()
        st.write("TABLE-The highest number of comments & Their corresponding channel names")
        st.dataframe(display)
