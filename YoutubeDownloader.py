import os
import io
from youtube_transcript_api import YouTubeTranscriptApi

"""
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaIoBaseDownload

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    with open(r'C:/temp/API_KEY.txt','r') as file:
        line = file.read()
        DEVELOPER_KEY=line

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=TomScottChannelID
    )
    response = request.execute()

    #print(response)
    for element in response:
        #print(element,response[element])
        pass
    for item in response['items']:
        for element in item:
            print(element,item[element])
        for element in item['statistics']:
            print(element,item['statistics'][element])

"""

TomScottChannelID='UCBa659QWEk1AI4Tg--mrJ2A'
TomScottVideoID1='mzAfich6mow'
TomScottSubtitleID1='0WIYZsAZMKysdaBQX5FzKKcZTyJlT4t-'

def get_subtitles(videoId:str)->str:
    transcript_list = YouTubeTranscriptApi.list_transcripts(TomScottVideoID1)
    manual_english_transcript = transcript_list.find_manually_created_transcript(['en'])
    subtitle_lines_dict = manual_english_transcript.fetch()
    subtitles = ''
    for line in subtitle_lines_dict:
        subtitles+=' '+line['text']
    return subtitles


if __name__ == "__main__":
    subtitles = get_subtitles(TomScottVideoID1)
    with open('Test.txt','w') as file:
        file.writelines(subtitles)