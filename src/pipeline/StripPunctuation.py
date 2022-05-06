import string

import pandas as pd

from src.pipeline.PipelineElement import PipelineElement


class StripPunctuation(PipelineElement):
    def __init__(self):
        pass

    def process(self, data: pd.DataFrame):
        processed_data = data.__deepcopy__()
        subtitles = pd.DataFrame(processed_data['ProcessedSubtitles'])
        for index, element in enumerate(subtitles.values):
            subtitles.iloc[index, 0] = str(element).translate(str.maketrans('', '', string.punctuation))

        processed_data['ProcessedSubtitles'] = subtitles
        return processed_data
