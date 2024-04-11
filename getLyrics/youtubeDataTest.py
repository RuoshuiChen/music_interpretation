from googleapiclient.discovery import build
import youtube_dl
#import json

api_key = 'AIzaSyAyrEqgYoHZf-Zn0aJtfD7TBo656Z8MAms'
youtube = build('youtube', 'v3', developerKey=api_key)

song_list = ["enter sandman backing track"]
for target in song_list:
    #target = "stairway to heaven led zepplin"

    request = youtube.search().list(
        part='id',
        q=target,
        type='video',
        maxResults=1
    )
    response = request.execute()
    print(response)

    video_id = response['items'][0]['id']['videoId']

    video_url = 'https://www.youtube.com/watch?v=' + video_id

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        #'outtmpl': '/rock',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])