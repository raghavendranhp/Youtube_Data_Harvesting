import googleapiclient
import googleapiclient.discovery
import googleapiclient.errors
class YoutubeHarvesting:
    def __init__(self):
        #youtube api 
        self.api_key = "AIzaSyDTVHYlhADlrOt5bJC1EiMqlLzKgDcQtPI "
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.youtube = googleapiclient.discovery.build(self.api_service_name, self.api_version, developerKey=self.api_key)

    def get_channel_details_using_channelname(self,search_query):
        try:
           # using search query getting channel details
            request = self.youtube.search().list(
                part="snippet",
                maxResults=1,
                q=search_query,
                type="channel"
            )
            response = request.execute()
            if 'items' in response:
                channel_id = response['items'][0]['snippet']['channelId']
                channel_request = self.youtube.channels().list(
                    part="snippet,statistics",
                    id=channel_id
                )
                channel_detail = channel_request.execute()

                if 'items' in channel_detail:
                    item = channel_detail['items'][0]
                    channel_details = {
                        'channel_id': item['id'],
                        'channel_title': item['snippet']['title'],
                        'channel_description': item['snippet']['description'],
                        'channel_published': item['snippet']['publishedAt'],
                        'channel_country': item['snippet']['country'],
                        'channel_viewcount': item['statistics']['viewCount'],
                        'channel_subscriber': item['statistics']['subscriberCount'],
                        'channel_videocount': item['statistics']['videoCount']
                    }
                    return channel_details
            else:
                return None
        except Exception as e:
            return None

    def get_video_ids_by_channel_id(self, channel_id):
        try:
            # getting video details using channelid
            video_ids = []
            next_page_token = None
            while True:
                video_ids_request = self.youtube.search().list(
                    part="id",
                    channelId=channel_id,
                    pageToken=next_page_token
                )
                video_ids_response = video_ids_request.execute()

                if "items" in video_ids_response:
                    for item in video_ids_response["items"]:
                        if item["id"]["kind"] == "youtube#video":
                            video_id = item["id"]["videoId"]
                            video_ids.append(video_id)
                # getting next page token
                next_page_token = video_ids_response.get("nextPageToken")
                if not next_page_token:
                    break

            return video_ids
        except Exception as e:
            return None

    def playlist_details_using_channelid(self, channel_id):
        try:
            # getting playlist details using chanelid
            playlists_details = []
            next_page_token = None
            while True:
                playlists_request = self.youtube.playlists().list(
                    part='snippet,contentDetails',
                    channelId=channel_id,
                    pageToken=next_page_token,
                    maxResults=50
                )

                playlists_response = playlists_request.execute()

                for playlist_item in playlists_response.get('items', []):
                    playlist_id = playlist_item['id']
                    playlist_title = playlist_item['snippet']['title']
                    playlist_published_date = playlist_item['snippet']['publishedAt']
                    playlist_description = playlist_item['snippet']['description']
                    playlist_item_count = playlist_item['contentDetails']['itemCount']
                    playlists_details.append({
                        'playlist_id': playlist_id,
                        'playlist_title': playlist_title,
                        'playlist_published_date': playlist_published_date,
                        'playlist_description': playlist_description,
                        'playlist_item_count': playlist_item_count
                    })
                # getting nextpagetoken
                next_page_token = playlists_response.get("nextPageToken")
                if not next_page_token:
                    break
            return playlists_details
        except Exception as e:
            return playlists_details
    def comments_details_using_videoid(self, video_id):
        comment_list = []
        comment_list.clear()
        
        try:
            comments_request = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=50
            )
            comments_response = comments_request.execute()
            
            if "items" in comments_response:
                comment_list = []
                for comment_item in comments_response.get('items', []):
                    comment_snippet = comment_item['snippet']['topLevelComment']['snippet']
                    comment_details = {
                        'author_name': comment_snippet['authorDisplayName'],
                        'author_id': comment_snippet['authorChannelId']['value'],
                        'published_date': comment_snippet['publishedAt'],
                        'comment_text': comment_snippet['textDisplay'],
                        'like_count': comment_snippet['likeCount']
                    }
                    comment_list.append(comment_details)
                    
                
            return comment_list
        except Exception as e:
            return []  # return an empty list if there is an error
    def get_videos_details_using_videoidslist(self,video_ids_list):
        try:
            videos_details = []
            
            for video_id in video_ids_list:
                videos_request = self.youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=video_id
                )
                videos_response = videos_request.execute()
                
                if "items" in videos_response:
                    for item in videos_response["items"]:
                        video_info = {
                            "Video_Id": item["id"],
                            "Video_Name": item["snippet"]["title"],
                            "Tags": item["snippet"].get("tags", []),
                            "PublishedAt": item["snippet"]["publishedAt"],
                            "View_Count": item["statistics"].get("viewCount", 0),
                            "Like_Count": item["statistics"].get("likeCount", 0),
                            "Dislike_Count": item["statistics"].get("dislikeCount", 0),
                            "Favorite_Count": item["statistics"].get("favoriteCount", 0),
                            "Comment_Count": item["statistics"].get("commentCount", 0),
                            "Duration": item["contentDetails"]["duration"],
                            "Thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                            "Caption_Status": item["contentDetails"].get("caption", "Not available"),
                            "Comments_Details": []
                        }
                        videos_details.append(video_info)
            # getting all the details regarding videos and then fetching comments details-bcoz sometimes quota exhausted
            for video_info in videos_details:
                comment_details_list = self.comments_details_using_videoid(video_info["Video_Id"])
                video_info["Comments_Details"] = comment_details_list
            
            return videos_details
        except Exception :
            return videos_details
            
    
    
    
    
    
    
    
    
    
    
    
    
