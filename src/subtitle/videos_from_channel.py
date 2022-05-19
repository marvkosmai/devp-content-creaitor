# -*- coding: utf-8 -*-
import os

import googleapiclient.discovery
import httplib2
import pandas as pd

from src import apikeys


def videos_from_channel(channel_name: str, channel_id: str, max_results: int = 25) -> pd.DataFrame:
    """
    Gets the latest <max_results> video data from a given channel name and id.
    Raises Connection error, if connection fails.
    :param channel_name: does not have to match actual channel name. Only for Dataframe
    :param channel_id: Necessary for request. Mind case sensitivity.
    :param max_results: Maximum Results to be returned. Can be less if there are not enough videos
    :return: pandas Dataframe with ChannelName,ChannelID,Title,PublishDate,Description,VideoID fields
    """
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    try:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

        api_service_name = "youtube"
        api_version = "v3"
        api_key = apikeys.YOUTUBE_API_KEY

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key)

        video_data = pd.DataFrame()

        next_page_token = None
        while len(video_data) < max_results:
            request = youtube.activities().list(
                part="snippet,contentDetails",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            next_page_token = response.get('nextPageToken')

            for item in response['items']:
                if item['snippet']['type'] == 'upload':
                    title = item['snippet']['title']
                    publish_date = item['snippet']['publishedAt']
                    description = item['snippet']['description']
                    video_id = item['contentDetails']['upload']['videoId']
                    video_tmp_data = pd.DataFrame([channel_name, channel_id,
                                                   title, publish_date, description, video_id]).T
                    video_data = pd.concat([video_data, pd.DataFrame(video_tmp_data)], ignore_index=False)
                if len(video_data) == max_results:
                    break

            if next_page_token is None:
                break

        video_data.columns = ['ChannelName', 'ChannelID', 'Title', 'PublishDate', 'Description', 'VideoID']
        video_data.reset_index(drop=True, inplace=True)
        return video_data
    except httplib2.error.ServerNotFoundError as error:
        print(error)
        raise ConnectionError(error)


if __name__ == "__main__":
    """
    pd.set_option('display.max_columns', None)
    TomScottChannelID = 'UCBa659QWEk1AI4Tg--mrJ2A'
    TS_videos = videos_from_channel('TomScott', TomScottChannelID, 20)
    minute_physics_channel_id = 'UCUHW94eEFW7hkUMVaZz4eDg'
    MP_videos = videos_from_channel('minutephysics', minute_physics_channel_id, 20)
    if TS_videos is not None and MP_videos is not None:
        all_videos = pd.concat([TS_videos, MP_videos])
        all_videos.reset_index(drop=True, inplace=True)
        #print(all_videos)
        all_videos.to_feather('test.feather')
        test = pd.read_feather('test.feather')
        print(test)
    """

