# -*- coding: utf-8 -*-
import os

import googleapiclient.discovery
import googleapiclient.errors
import isodate
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter

import src.apikeys as keys

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_subtitles(video_id: str) -> str:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    try:
        manual_english_transcript = transcript_list.find_manually_created_transcript(['en'])
        transcript = manual_english_transcript.fetch()
        formatter = TextFormatter()
        formatted_subtitles = formatter.format_transcript(transcript)
        return formatted_subtitles
    except NoTranscriptFound:
        print(f'No english transcript found for {video_id}')
        return None


def get_metadata(video_id: str) -> dict:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = keys.YOUTUBE_API_KEY

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    publish_date = response['items'][0]['snippet']['publishedAt']
    title = response['items'][0]['snippet']['title']
    description = response['items'][0]['snippet']['description']
    duration = isodate.parse_duration(response['items'][0]['contentDetails']['duration'])
    view_count = response['items'][0]['statistics']['viewCount']
    return_dict = {'title': title, 'description': description, 'publish_date': publish_date, 'duration': duration,
                   'view_count': view_count}
    return return_dict


if __name__ == "__main__":
    TomScottChannelID = 'UCBa659QWEk1AI4Tg--mrJ2A'
    TomScottVideoID1 = 'mzAfich6mow'
    TomScottSubtitleID1 = '0WIYZsAZMKysdaBQX5FzKKcZTyJlT4t-'
    print(get_metadata(TomScottVideoID1))
