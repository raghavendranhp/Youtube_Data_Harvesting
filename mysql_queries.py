import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
class sql_work():
    def __init__(self) :
        #for connections to mysql
        self.connection1 = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            database='you_harvest'
        )
        self.curs1 = self.connection1.cursor()
        self.engine = create_engine('mysql+mysqlconnector://root:1234@127.0.0.1/you_harvest', echo=True)
    def table_creation(self):
        #creating tables if not exists
        channel_table="""CREATE TABLE IF NOT EXISTS CHANNEL_TABLE (
        channel_id VARCHAR(50) PRIMARY KEY NOT NULL,
        channel_title TEXT NOT NULL,
        channel_description TEXT,
        channel_published DATETIME,
        channel_country VARCHAR(30),
        channel_viewcount INT NOT NULL,
        channel_subscriber INT NOT NULL,
        channel_videocount INT NOT NULL
        );"""
        playlist_table = """CREATE TABLE IF NOT EXISTS PLAYLIST_TABLE (
        Playlist_Id VARCHAR(50) PRIMARY KEY NOT NULL,
        channel_id VARCHAR(50) NOT NULL,
        Playlist_Title TEXT,
        Playlist_Published_date DATETIME,
        Playlist_Description TEXT,
        Playlist_Item_Count INT    
        );"""
        
        video_table="""CREATE TABLE IF NOT EXISTS VIDEO_TABLE (
            Video_Id TEXT PRIMARY KEY NOT NULL,
            Video_Name TEXT NOT NULL,
            PublishedAt DATETIME,
            View_Count INT,
            Like_Count INT,
            Dislike_Count INT,
            Favorite_Count INT,
            Comment_Count INT,
            Duration TIME,
            channel_id VARCHAR(50)
        );"""
        comments_table="""CREATE TABLE IF NOT EXISTS COMMENTS_TABLE (
            Author_ID VARCHAR(50) ,
            Video_Id VARCHAR(50) NOT NULL,
            Author_Name TEXT,
            Published_Date DATETIME,
            Comment_Text TEXT,
            Like_Count INT
        );"""
        self.curs1.execute(channel_table)
        self.curs1.execute(playlist_table)
        self.curs1.execute(video_table)
        self.curs1.execute(comments_table)
    def insert_to_mysql(self,channel_dataframe,playlist_dataframe,video_dataframe,comments_dataframe):
        #function to insert values in table if not empty and also handle duplicate error
        try:
            if not channel_dataframe.empty:
                channel_dataframe.reset_index(drop=True, inplace=True)
                channel_dataframe.to_sql("channel_table", self.engine, if_exists="append", index=False)
        except IntegrityError:
            pass
        try:
            if not playlist_dataframe.empty:
                playlist_dataframe.reset_index(drop=True, inplace=True)
                playlist_dataframe.to_sql("playlist_table", self.engine, if_exists="append", index=False)
        except IntegrityError:
            pass
        try:
            if not video_dataframe.empty:
                video_dataframe.reset_index(drop=True, inplace=True)
                video_dataframe.to_sql("video_table", self.engine, if_exists="append", index=False)
        except IntegrityError as e:
            pass
        try:
            if not comments_dataframe.empty:
                comments_dataframe.reset_index(drop=True, inplace=True)
                comments_dataframe.to_sql("comments_table", self.engine, if_exists="append", index=False)
        except IntegrityError:
            pass
    def question1(self):
        try:
            #What are the names of all the videos and their corresponding channels?
            query_question1="""SELECT v.Video_Name, c.channel_title
            FROM video_table v
            JOIN channel_table c ON v.channel_id = c.channel_id;
            """
            answer1 = []
            self.curs1.execute(query_question1)
            for details in self.curs1:
                answer1.append(details)
            answer1df = pd.DataFrame(answer1, columns=["Video_Name", "Channel_Title"])
            self.curs1.close()
            self.connection1.close()
            return answer1df
        except Exception:
            return None
    def question2(self):
        try:
            #Which channels have the most number of videos, and how many videos do they have
            query_question2="""SELECT channel_title,channel_videocount FROM channel_table 
            ORDER BY channel_videocount DESC ;"""
            answer2=[]
            self.curs1.execute(query_question2)
            for details in self.curs1:
                answer2.append(details)
            answer2df = pd.DataFrame(answer2, columns=["channel_title", "channel_videocount"])
            self.curs1.close()
            self.connection1.close()
            return answer2df
        except Exception:
            return None
    def question3(self):
        try:   
            #What are the top 10 most viewed videos and their respective channels
            query_question3="""SELECT v.Video_Name,v.View_Count, c.channel_title
            FROM video_table v
            JOIN channel_table c ON v.channel_id = c.channel_id
            ORDER BY View_Count DESC LIMIT 10;"""
            answer3=[]
            self.curs1.execute(query_question3)
            for details in self.curs1:
                answer3.append(details)
            answer3df = pd.DataFrame(answer3, columns=["Video_Name", "View_Count","channel_title"])
            self.curs1.close()
            self.connection1.close()
            return answer3df
        except Exception:
            return None
    def question4(self):
        try:
            # How many comments were made on each video, and what are their corresponding video names?
            query_question4 = """SELECT v.Video_Name, v.Comment_Count, c.channel_title
            FROM video_table v
            JOIN channel_table c ON v.channel_id = c.channel_id
            ORDER BY v.Comment_Count DESC ;"""
            answer4 = []
            self.curs1.execute(query_question4)
            for details in self.curs1:
                answer4.append(details)
            answer4df = pd.DataFrame(answer4, columns=["Video_Name", "Comment_count", "channel_title"])
            self.curs1.close()
            self.connection1.close()
            return answer4df
        except Exception:
            return None

    def question5(self):
        try:
            # Which videos have the highest number of likes, and what are their corresponding channel names?
            query_question5 = """SELECT v.Video_Name, v.Like_Count, c.channel_title
            FROM video_table v
            JOIN channel_table c ON v.channel_id = c.channel_id
            ORDER BY v.Like_Count DESC ;"""
            answer5 = []
            self.curs1.execute(query_question5)
            for details in self.curs1:
                answer5.append(details)
            answer5df = pd.DataFrame(answer5, columns=["Video_Name", "Like_count", "channel_title"])
            self.curs1.close()
            self.connection1.close()
            return answer5df
        except Exception:
            return None

    def question6(self):
        try:
            # What is the total number of likes and dislikes for each video, and what are their corresponding video names?
            query_question6 = """SELECT v.Video_Name, v.Like_Count, v.Dislike_Count
            FROM video_table v
            ORDER BY v.Like_Count DESC;"""
            answer6 = []
            self.curs1.execute(query_question6)
            for details in self.curs1:
                answer6.append(details)
            answer6df = pd.DataFrame(answer6, columns=["Video_Name", "Like_count", "Dislike_count"])
            self.curs1.close()
            self.connection1.close()
            return answer6df
        except Exception:
            return None

    def question7(self):
        try:
            # What is the total number of views for each channel, and what are their corresponding channel names?
            query_question7 = """SELECT c.channel_title, SUM(v.View_Count) AS total_views
            FROM channel_table c
            JOIN video_table v ON v.channel_id = c.channel_id
            GROUP BY c.channel_title
            ORDER BY total_views DESC;"""
            answer7 = []
            self.curs1.execute(query_question7)
            for details in self.curs1:
                answer7.append(details)
            answer7df = pd.DataFrame(answer7, columns=["Channel_title", "Total_views"])
            self.curs1.close()
            self.connection1.close()
            return answer7df
        except Exception:
            return None

    def question8(self):
        try:
            # What are the names of all the channels that have published videos in the year 2022?
            query_question8 = """SELECT c.channel_title, COUNT(v.video_id) AS video_count
            FROM channel_table c JOIN video_table v ON v.channel_id = c.channel_id
            WHERE YEAR(v.PublishedAt) = 2022 GROUP BY c.channel_title ORDER BY video_count desc;"""
            answer8 = []
            self.curs1.execute(query_question8)
            for details in self.curs1:
                answer8.append(details)
            answer8df = pd.DataFrame(answer8, columns=["Channel_title","Video_count"])
            self.curs1.close()
            self.connection1.close()
            return answer8df
        except Exception:
            return None

    def question9(self):
        try:
            # What is the average duration of all videos in each channel, and what are their corresponding channel names?
            query_question9 = """SELECT c.channel_title,
            SEC_TO_TIME(AVG(TIME_TO_SEC(v.Duration))) AS average_duration
            FROM video_table v
            JOIN channel_table c ON v.channel_id = c.channel_id
            GROUP BY c.channel_title
            ORDER BY average_duration DESC;"""
            answer9 = []
            self.curs1.execute(query_question9)
            for details in self.curs1:
                answer9.append(details)
            answer9df = pd.DataFrame(answer9, columns=["Channel_title", "Average_duration"])
            self.curs1.close()
            self.connection1.close()
            return answer9df
        except Exception:
            return None

    def question10(self):
        try:
            # Which videos have the highest number of comments, and what are their corresponding channel names?
            query_question10 = """SELECT v.Video_Name, v.Comment_Count, c.channel_title
            FROM video_table v
            JOIN channel_table c ON v.channel_id = c.channel_id
            ORDER BY v.Comment_Count DESC ;"""
            answer10 = []
            self.curs1.execute(query_question10)
            for details in self.curs1:
                answer10.append(details)
            answer10df = pd.DataFrame(answer10, columns=["Video_Name", "Comment_count", "channel_title"])
            self.curs1.close()
            self.connection1.close()
            return answer10df
        except Exception:
            return None
if __name__ == "__main__":
    sql_work = sql_work()

