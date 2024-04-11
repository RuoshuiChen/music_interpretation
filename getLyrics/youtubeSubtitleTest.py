from googleapiclient.discovery import build
import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import json

api_key = 'AIzaSyAyrEqgYoHZf-Zn0aJtfD7TBo656Z8MAms'
youtube = build('youtube', 'v3', developerKey=api_key)

song_list = ["good 4 u olivia rodrigo"]
for target in song_list:
    #target = "stairway to heaven led zepplin"

    request = youtube.search().list(
        part='id',
        q=target,
        type='video',
        maxResults=5
    )
    response = request.execute()
    print(response)

    video_id = response['items'][0]['id']['videoId']
    print(video_id)
    lyrics = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    print(lyrics)
    #
    # for i in range(len(lyrics)):
    #     curr_text = lyrics[i]['text']
    #     curr_start = str(lyrics[i]['start'])

    # transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    # transcript = transcript_list.find_transcript(['bg'])
    # translated_transcript = transcript.translate('en')
    # print(translated_transcript.fetch())
    #
    # formatter = TextFormatter()

    # .format_transcript(transcript) turns the transcript into a JSON string.
    #txt_formatted = formatter.format_transcript(translated_transcript.fetch())
    json_object = json.dumps(lyrics)
    with open('lyrics/pop/Good_4_u.json', "w") as outfile:
        outfile.write(json_object)
