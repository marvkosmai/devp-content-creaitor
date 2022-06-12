import os

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

from src.pipeline.PipelineElement import PipelineElement
import src.subtitle.videos_from_channel as vc
import src.subtitle.YoutubeDownloader as YD


class Pipeline:
    def __init__(self, data: pd.DataFrame = None):
        self.functions_queue = []
        self.data = pd.DataFrame(data)
        self.processed_data = self.data

    def get_last_videos_from_channel(self, channel_name: str, channel_id: str, max_nr_videos: int = 25):
        video_data = vc.videos_from_channel(channel_name, channel_id, max_nr_videos)
        subtitle_list = []
        duration_list = []
        view_count_list = []
        valid_video_data = pd.DataFrame()
        for index, video in video_data.iterrows():
            subtitles = YD.get_subtitles(video.loc['VideoID'])
            metadata = YD.get_metadata(video.loc['VideoID'])
            if subtitles is not None:
                valid_video_data = valid_video_data.append(video_data.iloc[index, :])
                subtitle_list.append(subtitles)
                duration_list.append(metadata['duration'])
                view_count_list.append(metadata['view_count'])

        valid_video_data['Subtitles'] = subtitle_list
        valid_video_data['Duration'] = duration_list
        valid_video_data['ViewCount'] = view_count_list

        self.data = self.data.append(valid_video_data, ignore_index=True)

    def read_data_from_csv(self, csv_file: str, **kwargs) -> None:
        if not isinstance(csv_file, str):
            raise TypeError(str(type(csv_file)) + ' is not a str')
        if not os.path.isfile(csv_file):
            raise FileNotFoundError(str(csv_file) + " is not a valid file")
        if len(kwargs) == 0:
            self.data = pd.read_csv(csv_file)
        self.data = pd.read_csv(csv_file, **kwargs)

    def batch_read_data_from_csv(self, csv_list: list, *, ignore_errors=False, **kwargs) -> None:
        if not isinstance(csv_list, list):
            raise TypeError(str(type(csv_list)) + ' is not a list')
        if len(csv_list) == 0:
            raise IndexError('List is empty')
        for index, file in enumerate(csv_list):
            if not os.path.isfile(file):
                if not ignore_errors:
                    raise FileNotFoundError(str(file) + " is not a valid file")
                else:
                    print(str(file) + " is not a valid file")
                    continue
            self.data = pd.concat([self.data, pd.read_csv(file, **kwargs)])
        self.data.reset_index(drop=True, inplace=True)

    def save_data_to_feather(self, file_name: str, target: str = 'data'):
        if target == 'data':
            self.data.to_feather(file_name)
        elif target == 'processed_data':
            self.processed_data.to_feather(file_name)
        else:
            raise ValueError('Invalid target input. Must be data or processed_data')

    def load_data_from_feather(self, file_name: str, target: str = 'data'):
        fdata = pd.read_feather(file_name)
        if target == 'data':
            self.data = self.data.append(fdata)
        elif target == 'processed_data':
            self.processed_data = self.processed_data.append(fdata)
        else:
            raise ValueError('Invalid target input. Must be data or processed_data')

    def add_step(self, PipelineElementSubclass) -> None:
        """
        Adds a PipelineElement to the process Pipline, Subclass must have process function,
        which must take a Pandas Dataframe as input and returns a pandas Dataframe
        """
        if not issubclass(type(PipelineElementSubclass), PipelineElement):
            raise TypeError(
                'Expected Subclass from PipelineElement function but got ' + str(type(PipelineElementSubclass)))
        self.functions_queue.append(PipelineElementSubclass.process)

    def remove_last_step(self) -> None:
        self.functions_queue = self.functions_queue[:-1]

    def run(self) -> None:
        """
        Runs the functions_queue in order on self.data, result written in self.processed_data
        """
        self.processed_data = self.data
        for function in self.functions_queue:
            self.processed_data = function(self.processed_data)


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    p = Pipeline()
    tom_scott_channel_id = 'UCBa659QWEk1AI4Tg--mrJ2A'
    minute_physics_channel_id = 'UCUHW94eEFW7hkUMVaZz4eDg'
    p.get_last_videos_from_channel('TomScott', tom_scott_channel_id, 5)
    # print(p.data)
    p.get_last_videos_from_channel('MinutePhysics', minute_physics_channel_id, 5)
    print(p.data)
    p.save_data_to_feather('test.feather')
    print('----------------------------------------------------------')
    p2 = Pipeline()
    p2.load_data_from_feather('test.feather', target='data')
    print(p2.data)
