import pandas as pd
import pymongo
from pymongo import MongoClient
from pymongo import errors
class mongodb_work:
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        # create Database
        db_name = 'Youtube_Harvesting'
        db = client[db_name]
        #using channel_details collection name
        self.channel_details_collection = db['Channel_details']
        
    def insert_into_mongodb(self,record):
        try:
            #inserting record into the mongodb database
            self.channel_details_collection.insert_one(record)
            return 'document inserted sucessfully'
        except errors.DuplicateKeyError as e:
            return 'document already inserted'
    def get_channels(self):
        try:
            #to display available channels details in mongodb database
            display_projection = {
                '_id': 1,
                'channel_details.channel_id': 1,
                'channel_details.channel_title': 1
            }
            display_documents = self.channel_details_collection.find({}, display_projection)
            display_dictionary = {}  
            for document in display_documents:
                display_details = document.get('channel_details', {})
                channel_title =display_details['channel_title']
                channel_id = display_details['channel_id']
                display_dictionary[channel_title] = channel_id  
        
            return display_dictionary
        except Exception as e:
            return {'No Channel available':0}

    def channel_query(self,selected_channel_id):
        try:
            #function to retrieve channel details from mongodb database
            channel_query = {'_id': selected_channel_id}
            channel_projection = {'_id': 1, 
                          'channel_details.channel_id':1,
                          'channel_details.channel_title': 1, 
                          'channel_details.channel_published': 1, 
                          'channel_details.channel_country': 1, 
                          'channel_details.channel_description': 1,
                          'channel_details.channel_viewcount': 1, 
                          'channel_details.channel_subscriber': 1, 
                          'channel_details.channel_videocount': 1}
            channel_document = self.channel_details_collection.find_one(channel_query, channel_projection)
    
            if channel_document:
                channel_information = channel_document.get('channel_details', {})
                channel_dataframe = pd.DataFrame([channel_information])
                #conversion
                ch_columns_to_convert_int = ['channel_viewcount', 'channel_subscriber', 'channel_videocount']
                ch_columns_to_convert_str = ['channel_title', 'channel_description', 'channel_country']
                ch_column_to_convert_date = ['channel_published']
                for col in ch_columns_to_convert_int:
                    channel_dataframe[col] = channel_dataframe[col].astype(int)
                for col in ch_columns_to_convert_str:
                    channel_dataframe[col] = channel_dataframe[col].astype(str)
                for col in ch_column_to_convert_date:
                    channel_dataframe[col] = pd.to_datetime(channel_dataframe[col])
        
            return  channel_dataframe  
        except Exception as e:
            return None
    def video_query(self,selected_channel_id):
        try:
            #function to retrieve video details  of a from mongodb database
            empty_list=[]
            video_query = {'_id': selected_channel_id}
            video_projection = {
                '_id': 1,
                'video_details.Video_Id': 1,  
                'video_details.Video_Name': 1,
                'video_details.PublishedAt': 1,
                'video_details.View_Count': 1,
                'video_details.Like_Count': 1,
                'video_details.Dislike_Count': 1,
                'video_details.Favorite_Count': 1,
                'video_details.Comment_Count': 1,
                'video_details.Duration': 1,
                }
            video_document = self.channel_details_collection.find_one(video_query, video_projection)
    
            if video_document:
                video_details = video_document.get('video_details', [])
        
                if video_details:
                    video_dataframe = pd.DataFrame(video_details)
            
                    # conversion
                    vid_columns_to_convert_int = ['View_Count', 'Like_Count', 'Dislike_Count', 'Favorite_Count', 'Comment_Count']
                    vid_columns_to_convert_str = ['Video_Id', 'Video_Name']
                    vid_column_to_convert_date = ['PublishedAt']
            
                    for col in vid_columns_to_convert_int:
                        video_dataframe[col] = video_dataframe[col].astype(int)
                    for col in vid_columns_to_convert_str:
                        video_dataframe[col] = video_dataframe[col].astype(str)
                    for col in vid_column_to_convert_date:
                        video_dataframe[col] = pd.to_datetime(video_dataframe[col])
            
                    #Conversion to HH:MM:SS format for Duration
                    video_dataframe['Duration'] = pd.to_timedelta(video_dataframe['Duration'])
                    video_dataframe['Duration'] = video_dataframe['Duration'].dt.total_seconds().astype(int).apply(lambda x: f'{x // 3600:02}:{(x % 3600) // 60:02}:{x % 60:02}')
                    #insert channel_id
                    video_dataframe['channel_id'] = selected_channel_id
                    #duplicates removing
                    video_dataframe.drop_duplicates(subset=['Video_Id'], keep='first', inplace=True)
            return  video_dataframe   
        except Exception as e:
            return  pd.DataFrame(empty_list)
    def playlist_query(self,selected_channel_id):
        try:
            #function to retrieve playlist details of a channel from mongodb database
            playlist_query={'_id': selected_channel_id}
            playlist_projection={'_id': 1,
                                'channel_details.channel_id':1,
                                'channel_details.channel_title':1,
                                'playlist_details.playlist_id':1,
                                'playlist_details.playlist_title':1,
                                'playlist_details.playlist_published_date':1,
                                'playlist_details.playlist_description':1,
                                'playlist_details.playlist_item_count':1
                                }
            playlist_document = self.channel_details_collection.find_one(playlist_query, playlist_projection)
            if playlist_document:
                playlist_data=[]
                playlist_details=playlist_document.get('playlist_details',[])
                #to handle values when no playlist details available for particular channel
                if not playlist_details:
                    playlist_data.append({
                        'channel_id':selected_channel_id,
                        'Playlist_Id':'NA',
                        'Playlist_Title':'No Playlist',
                        'Playlist_Published_date':pd.NaT,
                        'Playlist_Description':'Playlist Not Available For This Channel',
                        'Playlist_Item_Count':0
                        })
                else:
                    for playlist in playlist_details:
                        published_date=pd.to_datetime(playlist['playlist_published_date'])
                        playlist_data.append({
                        'channel_id':selected_channel_id,
                        'Playlist_Id':playlist['playlist_id'],
                        'Playlist_Title':playlist['playlist_title'],
                        'Playlist_Published_date':published_date,
                        'Playlist_Description':playlist['playlist_description'],
                        'Playlist_Item_Count':playlist['playlist_item_count']
                        })
            if playlist_data:
                playlist_dataframe=pd.DataFrame(playlist_data)
                playlist_dataframe['Playlist_Item_Count']=playlist_dataframe['Playlist_Item_Count'].astype(int)
                playlist_dataframe['Playlist_Published_date']=pd.to_datetime(playlist_dataframe['Playlist_Published_date'])
                playlist_column_to_convert_str=['channel_id','Playlist_Id','Playlist_Title','Playlist_Description']
                for col in playlist_column_to_convert_str:
                    playlist_dataframe[col]=playlist_dataframe[col].astype(str)
            return playlist_dataframe
        except Exception as e:
            return None
                
    def comment_query(self,selected_channel_id):
        try:
            #function to retrieve comments details of a video from mongodb database
            comment_query = {'_id': selected_channel_id}
            comment_projection = {
                '_id': 1,
                'video_details.Video_Id': 1,  
                'video_details.Comments_Details.author_name': 1,
                'video_details.Comments_Details.author_id': 1,
                'video_details.Comments_Details.published_date': 1,
                'video_details.Comments_Details.comment_text': 1,
                'video_details.Comments_Details.like_count': 1
                }
            comment_document = self.channel_details_collection.find_one(comment_query, comment_projection)
            if comment_document:
                data = []
                for video in comment_document['video_details']:
                    video_id = video['Video_Id']
                    comments_details = video.get('Comments_Details', [])
                    #to handle values when no comments details available for particular video,bcoz for some videos comments disabled
                    if not comments_details: 
                        data.append({
                            'Video_Id': video_id,
                            'Author_Name': 'NA',
                            'Author_ID': 'NA',
                            'Published_Date': pd.NaT,
                            'Comment_Text': 'Comments Disabled/No comments For This Video',
                            'Like_Count': 0 
                            })
                    else:
                        for comment in comments_details:
                            published_date = pd.to_datetime(comment['published_date'])
                            data.append({
                            'Video_Id': video_id,
                            'Author_Name': comment['author_name'],
                            'Author_ID': comment['author_id'],
                            'Published_Date': published_date,
                            'Comment_Text': comment['comment_text'],
                            'Like_Count': comment['like_count']
                            })
            if data:
                comments_dataframe = pd.DataFrame(data)
                comments_dataframe['Like_Count']=comments_dataframe['Like_Count'].astype(int)
                comments_dataframe['Published_Date']=pd.to_datetime(comments_dataframe['Published_Date'])
                comments_column_to_convert_str=['Video_Id','Author_Name','Author_ID','Comment_Text']
                for col in comments_column_to_convert_str:
                    comments_dataframe[col]=comments_dataframe[col].astype(str)
            return comments_dataframe
        except Exception as e:
            #sometimes error occurs because of quota exhausting so pandas wrk also interupted
            return pd.DataFrame([])