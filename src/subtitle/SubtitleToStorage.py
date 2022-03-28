#import os.path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


class SubtitlesToStorage:

    def __init__(self, source: str, video_id: str, storage_config):
        self.source = source
        self.video_id = video_id
        self.storage_config = storage_config

    def save(self):
        # download subtitles
        subtitles = None

        if 'youtube' == self.source:
            subtitles = self.__subtitles_from_youtube()

        # save to storage
        if 'file' == self.storage_config['type']:
            self.__save_to_file(subtitles)

    def __subtitles_from_youtube(self):
        transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
        manual_english_transcript = transcript_list.find_manually_created_transcript(['en'])
        transcript = manual_english_transcript.fetch()
        formatter = TextFormatter()
        subtitles = formatter.format_transcript(transcript)

        return subtitles

    def __save_to_file(self, subtitles):
        filename = self.video_id + '.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(subtitles)
